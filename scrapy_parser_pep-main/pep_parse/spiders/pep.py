import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_pep_tables = response.css('table.pep-zero-table')
        self.logger.info(f'Found {len(all_pep_tables)} PEP tables on page')
        for table in all_pep_tables:
            rows = table.css('tbody tr')
            for row in rows:
                link = row.css('a.pep.reference.internal::attr(href)').get()
                if link:
                    full_link = link if link.endswith('/') else link + '/'
                    yield response.follow(full_link, callback=self.parse_pep)

    def parse_pep(self, response):
        data = {
            'number': response.css('h1.page-title::text').get().split(' ')[1],
            'name': ''.join(
                response.css('h1.page-title::text').get()
            ).strip(),
            'status': response.css('abbr::text').get(),
        }
        yield PepParseItem(data)
