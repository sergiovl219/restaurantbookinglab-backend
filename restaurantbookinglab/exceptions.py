from rest_framework.exceptions import APIException


class BadRequestAPIException(APIException):
    status_code = 400
    default_detail = 'Bad Request.'
    default_code = 'bad_request'


class TaskNotFoundAPIException(APIException):
    status_code = 400
    default_detail = 'Task Not Found.'
    default_code = 'task_not_found'
