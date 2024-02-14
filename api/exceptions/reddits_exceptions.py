class RedditAPIError(Exception):
    pass

class RedditAuthorizationError(RedditAPIError):
    pass

class RedditConnectionError(RedditAPIError):
    pass

class RedditRequestError(RedditAPIError):
    pass

class RedditUnexpectedResponseError(RedditAPIError):
    pass