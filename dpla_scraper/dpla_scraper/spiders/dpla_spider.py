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
        docs = data.get("docs", [])

        # yield the entire dict for each doc
        for doc in docs:
            yield doc
