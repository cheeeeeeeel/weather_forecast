

class AppError(Exception):
    pass


class InvalidApiResponseError(AppError):
    pass

class NetworkError(AppError):
    pass

class RequestError(AppError):
    pass

