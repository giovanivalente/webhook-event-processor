from rest_framework import status
from rest_framework.exceptions import APIException


class RealmateAPIError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A business error occurred.'
    default_code = 'ERROR'

    def __init__(self, detail=None, code=None, status_code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        if status_code and status_code != self.status_code:
            self.status_code = status_code

        super().__init__(detail=detail, code=code)


class ObjectNotFound(RealmateAPIError):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'The requested appeal was not found.'
    default_code = 'OBJECT_NOT_FOUND'
