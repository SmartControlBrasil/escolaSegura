class ProductPricingService:
    @staticmethod
    def margin_percent(product):
        if not product.sale_price:
            return 0
        return round(((product.sale_price - product.cost_price) / product.sale_price) * 100, 2)
