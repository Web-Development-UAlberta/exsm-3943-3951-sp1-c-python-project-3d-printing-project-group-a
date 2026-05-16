import os
import stripe

stripe.api_key = os.getenv("sk_test_51TSkkhBPtnrt6kzSDrBFzzyssPG8uQ4R2VycbrNzDHCJ3SYTISiCWUpaLVbp423FKLooLabjTbq2A5V37jOawwlz00Q0b5r4Cx")


def create_payment_intent(amount_dollars, currency="cad", metadata=None):
    amount_cents = int(round(amount_dollars * 100))
    intent = stripe.PaymentIntent.create(
        amount=amount_cents,
        currency=currency,
        metadata=metadata or {},
        automatic_payment_methods={"enabled": True}
    )
    return intent


def retrieve_payment_intent(payment_intent_id):
    return stripe.PaymentIntent.retrieve(payment_intent_id)


def construct_webhook_event(payload, sig_header, webhook_secret):
    return stripe.Webhook.construct_event(payload, sig_header, webhook_secret)