class RedditAPIError(Exception):
    pass


class RedditAuthorizationError(RedditAPIError):
    pass


class RedditConnectionError(RedditAPIError):
    pass


class RedditRequestError(RedditAPIError):
    pass


class RedditResponseError(RedditAPIError):
    pass


class RedditUnexpectedResponseError(RedditAPIError):
    pass


class RedditSearchError(Exception):
    pass


class RedditDatabaseAccessError(RedditSearchError):
    pass


class RedditValidationError(RedditSearchError):
    pass


class RedditResultsNotFound(Exception):
    pass


class CreateRedditSearchError(Exception):
    pass