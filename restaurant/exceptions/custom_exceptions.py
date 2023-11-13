class OwnerNotFoundException(Exception):
    def __init__(self, message="Owner not found"):
        self.message = message
        super().__init__(self.message)


class RestaurantNotFoundException(Exception):
    def __init__(self, message="Restaurant not found"):
        self.message = message
        super().__init__(self.message)
