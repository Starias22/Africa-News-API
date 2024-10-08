from news_api_fetching import NewsAPIFetcher
news_producer=NewsAPIFetcher(extractor='newsapi')

news_producer.run()