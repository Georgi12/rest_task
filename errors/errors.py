

class ServiceException(Exception):
    description = ''
    status = 500

    def __init__(self, description: str | None = None):
        if description:
            self.description = description


class UnknownError(ServiceException):
    description = 'Unknown Error'
    status = 500


class UserWrongDbSaveError(ServiceException):
    description = 'Saving data has been failed'
    status = 400


class DeleteNotExistsObjectError(ServiceException):
    description = 'Object in not exists'
    status = 400
