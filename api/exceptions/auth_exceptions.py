class UnauthorizedToken(Exception):
    pass


class IncorrectEmail(Exception):
    pass


class IncorrectPassword(Exception):
    pass


class TokenBlocked(Exception):
    pass


class InvalidToken(Exception):
    pass


class JWTDecodeError(Exception):
    pass


class HashingError(Exception):
    pass


class TokenCreationError(Exception):
    pass


class DeleteTokenExpiredError(Exception):
    pass


class DeactivateTokenExpiredError(Exception):
    pass