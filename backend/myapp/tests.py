from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='d7ce122de0f84c77b35121f97ac2259f')

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='corona',
                                          language='en',
                                          )
print(top_headlines)

# # /v2/sources
# sources = newsapi.get_sources()
