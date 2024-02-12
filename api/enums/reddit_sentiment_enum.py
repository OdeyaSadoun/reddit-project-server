from enum import Enum

class ModelRedditSentiment(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"