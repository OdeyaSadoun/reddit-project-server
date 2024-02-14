from enum import Enum  


class ModelRedditCategory(str, Enum):
    hot = "hot"
    rising = "rising"
    top = "top"
    new = "new"
