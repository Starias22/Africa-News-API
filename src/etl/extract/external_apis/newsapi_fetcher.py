from news_api_fetching import NewsAPIFetcher
news_producer=NewsAPIFetcher(source='newsapi')

news_producer.run()