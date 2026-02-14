import datetime
from collections import defaultdict

from pep_parse.settings import BASE_DIR, DATETIME_FORMAT, RESULTS_DIR


class PepParsePipeline:
    def open_spider(self, spider):
        self.peps = defaultdict(int)
        self.results_dir = BASE_DIR / RESULTS_DIR
        self.results_dir.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        self.status = item['status']
        self.peps[self.status] += 1
        return item

    def close_spider(self, spider):
        time_now = datetime.datetime.now()
        time_format = time_now.strftime(DATETIME_FORMAT)
        name_file = f'status_summary_{time_format}.csv'
        file_path = self.results_dir / name_file
        result = self.peps.items()
        total = sum(self.peps.values())
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines([
                'Статус, Количество\n',
                *[f'{status}, {amount}\n' for status, amount in result],
                f'Total, {total}\n'
            ])
