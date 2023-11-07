class TicketNotFoundException(Exception):
    def __init__(self, message="Ticket not found"):
        self.message = message
        super().__init__(self.message)


class PurchaseNotFoundException(Exception):
    def __init__(self, message="Purchase not found"):
        self.message = message
        super().__init__(self.message)


class TicketNotAvailableException(Exception):
    def __init__(self, message="Ticket not available"):
        self.message = message
        super().__init__(self.message)


class QuantityExceedsMaxPurchaseException(Exception):
    def __init__(self, message="Quantity exceeds maximum purchase"):
        self.message = message
        super().__init__(self.message)
