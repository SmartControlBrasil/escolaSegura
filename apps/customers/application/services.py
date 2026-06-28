class CustomerQualificationService:
    @staticmethod
    def is_complete(customer) -> bool:
        return bool(customer.name and (customer.email or customer.phone))
