from rest_framework.exceptions import APIException


class OwnerNotFoundAPIException(APIException):
    status_code = 404
    default_detail = 'Owner not found.'
    default_code = 'owner_not_found'


class RestaurantNotFoundAPIException(APIException):
    status_code = 404
    default_detail = 'Restaurant not found.'
    default_code = 'restaurant_not_found'
