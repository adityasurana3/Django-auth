from product.models import Product

PERMISSION_CONFIG = {
    "customer": {
        Product: ['view'],
        # Other models
    },
    "seller": {
        Product: ['add', 'view', 'change']
    },
}
