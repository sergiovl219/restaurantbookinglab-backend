from rest_framework.exceptions import APIException


class TicketNotFoundAPIException(APIException):
    status_code = 404
    default_detail = 'Ticket not found.'
    default_code = 'ticket_not_found'


class PurchaseNotFoundAPIException(APIException):
    status_code = 404
    default_detail = 'Purchase not found.'
    default_code = 'purchase_not_found'
