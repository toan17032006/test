import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from routes import cart, orders, payment, state, webhooks  # noqa: E402


class ImmediateRequest:
    def __init__(self, user_id="2", payload=None):
        self.headers = {"x-user-id": user_id}
        self.query_params = {}
        self.cookies = {}
        self.payload = payload or {}

    async def json(self):
        return self.payload


def run_immediate(coroutine):
    """Drive these in-memory handlers without opening a platform event loop."""
    try:
        coroutine.send(None)
    except StopIteration as result:
        return result.value
    raise AssertionError("Handler unexpectedly yielded while running its in-memory path")


class StoreWorkflowTests(unittest.TestCase):
    def setUp(self):
        state.carts.clear()
        state.orders.clear()
        state.orders.update({
            1001: {"id": 1001, "user_id": "2", "status": "pending", "payment_status": "pending", "shipping_status": "not_fulfilled", "total": 20, "items": []}
        })
        state.payments.clear()
        webhooks.received_events.clear()

    def test_cart_checkout_payment_and_webhook_flow_uses_lab_state(self):
        request = ImmediateRequest()
        added = run_immediate(cart.add_item(cart.AddItem(product_id=1, quantity=2, unit_price=10), request))
        self.assertEqual(added["total"], 20)

        created = run_immediate(orders.create_order(orders.CreateOrder(total=17), request))
        order_id = created["order_id"]
        self.assertEqual(created["order"]["total"], 17)
        self.assertEqual(state.carts["2"], [])

        paid = run_immediate(payment.process_payment(payment.PaymentRequest(order_id=order_id)))
        self.assertEqual(paid["order"]["payment_status"], "paid")

        webhook_request = ImmediateRequest(payload={"order_id": order_id, "status": "paid"})
        first = run_immediate(webhooks.payment_webhook(webhook_request))
        second = run_immediate(webhooks.payment_webhook(ImmediateRequest(payload={"order_id": order_id, "status": "paid"})))
        self.assertEqual(first["duplicate_count"], 1)
        self.assertEqual(second["duplicate_count"], 2)


if __name__ == "__main__":
    unittest.main()
