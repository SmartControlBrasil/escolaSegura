class InventoryPolicy:
    @staticmethod
    def can_reserve(quantity_available, quantity_requested):
        return quantity_available >= quantity_requested
