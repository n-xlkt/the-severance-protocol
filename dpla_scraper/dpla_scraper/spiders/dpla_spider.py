import scrapy
import os


class DPLASpider(scrapy.Spider):
    name = "dpla"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = os.environ.get("DPLA_API")
        if not self.api_key:
            raise ValueError("DPLA_API environment variable is not set")

    async def start(self):
        url = f"https://api.dp.la/v2/items?api_key={self.api_key}&page=1"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # parse JSON data from the response body
        data = response.json()

        # docs are in a list under the "docs" key
        # process docs on current page
        docs = data.get("docs", [])
        # yield the entire dict for each doc
        for doc in docs:
            yield doc

        # determine if there is a next page
        start_index = data.get("start", 0)
        items_per_page = data.get("limit", 10)
        total_items = data.get("count", 0)

        if start_index + items_per_page < total_items:
            next_page_number = (start_index // items_per_page) + 2
            next_page_url = f"https://api.dp.la/v2/items?api_key={self.api_key}&page={next_page_number}"

            self.logger.info(f"Paginating to next page: {next_page_url}")
            yield scrapy.Request(url=next_page_url, callback=self.parse)
