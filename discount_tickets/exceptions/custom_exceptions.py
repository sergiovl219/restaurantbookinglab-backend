class TicketNotFoundException(Exception):
    def __init__(self, message="Ticket not found"):
        self.message = message
        super().__init__(self.message)


class PurchaseNotFoundException(Exception):
    def __init__(self, message="Purchase not found"):
        self.message = message
        super().__init__(self.message)
