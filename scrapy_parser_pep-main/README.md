# scrapy_parser_pep
Проект сделан на базе фреймворка Scrapy и предназначен для парсинга информации о PEP.
Информацию которую парсит проект: номер, название, текущий статус.

Результаты сохраняются в два файла .csv.

Запуск проекта:

1) Клонируйте проект
git clone https://github.com/SergeyGusev1/scrapy_parser_pep.git

2) Установите виртуальное окружение и запустите его
python -m venv venv
source venv/Scripts/activate

3) Установите зависимости
pip install -r requirements.txt

4) Запустите проект

scrapy crawl pep
