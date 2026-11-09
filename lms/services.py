import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name: str):
    """Создаёт продукт в Stripe."""
    return stripe.Product.create(name=name)


def create_stripe_price(product_id: str, amount_kopecks: int):
    """Создаёт цену в Stripe (в копейках)."""
    return stripe.Price.create(
        product=product_id,
        unit_amount=amount_kopecks,
        currency='rub',
    )


def create_checkout_session(price_id: str, success_url: str, cancel_url: str):
    """Создаёт сессию для получения ссылки на оплату."""
    return stripe.checkout.Session.create(
        mode='payment',
        line_items=[{'price': price_id, 'quantity': 1}],
        success_url=success_url,
        cancel_url=cancel_url,
    )
