from news_api_fetching import NewsAPIFetcher
print('Producing news')
news_producer=NewsAPIFetcher(source='google_news')

news_producer.run()
