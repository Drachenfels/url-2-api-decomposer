class BaseUrl4ApiException(Exception):
    pass


class InvalidUrlPattern(BaseUrl4ApiException):
    pass


class UnrecognisedProtocol(BaseUrl4ApiException):
    pass


class InvalidInputPattern(BaseUrl4ApiException):
    pass
