import scrapy


class BeninwebtvSpider(scrapy.Spider):
    name = "beninwebtv_spider"
    allowed_domains = ["beninwebtv.com"]
    
    def __init__(self, max_pages=1, region="afrique-de-louest", country="benin", *args, **kwargs):
        super().__init__(*args, **kwargs)  # Correct super call
        self.max_pages = int(max_pages)
        self.current_page = 1
        self.country = country
        self.start_urls = [f"https://beninwebtv.com/pays/afrique/{region}/{country}/?tdb-loop-page=1"]

    def parse(self, response):
        # Retrieve all the news articles using the response
        news_items = response.css("#tdi_58 > *")  # Adjust the selector based on the actual structure

        for news_item in news_items:
            news_item = news_item.css("div.tdc-row")
            # Extract the news article URL
            url = news_item.css("a::attr(href)").get()
            print("***************", url)

            if not news_item:  # Check if news_item exists
                return

            # Assuming that the news item is the first child
            news_item = news_item[0].css("div.tdc-row")

            image_url = news_item.css("img::attr(src)").get()  # Get image URL

            # Extracting relevant news details
            news_details = news_item.css("div.wpb_wrapper")[1]
            country = news_details.css("a[data-taxonomy='pays']::text").get()
            title_url = news_details.css("h3 a")

            title = title_url.attrib.get("title")
            url = title_url.attrib.get("href")

            description_content = news_details.css("div.td_block_wrap.tdb_module_excerpt.tdb_module_excerpt_0::text").getall()
            description = " ".join(description_content).strip() 

            category = news_details.css("a[data-taxonomy='category']::text").get()

            author = news_details.css("div.td_block_wrap.tdb_module_author_name.tdb_module_author_name_0 a")
            author_url = author.xpath("./@href").get()
            author_name = author.xpath("./text()").get()

            publication_date = news_details.css("time::text").getall()[-1] if news_details.css("time::text").getall() else None

            yield {
                "title": title,
                "author_name": author_name,
                "author_url": author_url,
                "publication_date": publication_date,
                "description": description,
                "category": category,
                "image_url": image_url,
                "url": url,
                "country": country
            }

        # Increment the current page count
        self.current_page += 1

        # Handle pagination if the current page is less than the max_pages
        if self.current_page <= self.max_pages:
            next_page_url = f"https://beninwebtv.com/pays/afrique/afrique-de-louest/{self.country}/?tdb-loop-page={self.current_page}"
            yield response.follow(next_page_url, callback=self.parse)
