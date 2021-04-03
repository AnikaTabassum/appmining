from google_play_scraper import app

result = app(
    'com.facebook.lite',
    lang='en', # defaults to 'en'
    country='us' # defaults to 'us'
)

print("score",result['score'])
print("histogram", result['histogram'])
print("ratings", result['ratings'])
print("reviews ", result['reviews'])