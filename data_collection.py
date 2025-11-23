import snscrape.modules.twitter as sntwitter
from datetime import datetime
from datetime import timedelta

def fetch_twitter_posts(keyword, limit=50):
    posts = []
    try:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(keyword).get_items()):
            if i >= limit:
                break
            posts.append({
                "text": tweet.content,
                "timestamp": tweet.date
            })
        return posts
    except:
        return None


def load_mock_data(keyword, limit=50):
    mock_posts = [
        {"text": f"I feel great about {keyword} today!", "timestamp": datetime.now() - timedelta(hours=1)},
        {"text": f"{keyword} is becoming expensive and stressful", "timestamp": datetime.now() - timedelta(hours=2)},
        {"text": f"I think {keyword} services are improving slowly.", "timestamp": datetime.now() - timedelta(hours=3)}
    ]
    return mock_posts[:limit]
