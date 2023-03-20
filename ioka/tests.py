import unittest
from unittest.mock import MagicMock

from api import Event, Order


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.order_data = {
            "id": "1",
            "shop_id": "123",
            "status": "UNPAID",
            "created_at": "2022-03-18T12:00:00Z",
            "amount": 50000,
            "currency": "KZT",
            "capture_method": "AUTO",
            "external_id": "1234",
            "description": "Test order",
            "extra_info": {"key": "value"},
            "attempts": 10,
            "due_date": "2022-03-19T12:00:00Z",
            "customer_id": "5678",
            "card_id": "91011",
            "mcc": "1234",
            "back_url": "http://example.com/back",
            "success_url": "http://example.com/success",
            "failure_url": "http://example.com/failure",
            "template": "default",
            "checkout_url": "http://example.com/checkout",
            "access_token": "1234",
        }
        self.api_mock = MagicMock()
        self.order = Order.set_api(self.api_mock)

    def test_create(self):
        expected_order = Order(**self.order_data)
        self.api_mock.create_order.return_value = {"order": self.order_data}
        result = Order.create(**self.order_data)
        self.api_mock.create_order.assert_called_once_with(**self.order_data)
        self.assertEqual(result, expected_order)

    def test_cancel(self):
        response_data = {
            "id": "string",
            "order_id": "string",
            "status": "PENDING",
            "created_at": "2019-08-24T14:15:22Z",
            "approved_amount": 0,
            "captured_amount": 0,
            "refunded_amount": 0,
            "processing_fee": 0,
            "payer": {
                "type": "CARD",
                "pan_masked": "string",
                "expiry_date": "string",
                "holder": "string",
                "payment_system": "string",
                "emitter": "string",
                "email": "user@example.com",
                "phone": "string",
                "customer_id": "string",
                "card_id": "string",
            },
            "error": {"code": "string", "message": "string"},
            "acquirer": {"name": "string", "reference": "string"},
            "action": {"url": "string"},
        }
        self.api_mock.cancel_order.return_value = response_data
        result = Order.cancel(order_id="1")
        self.api_mock.cancel_order.assert_called_once_with(order_id="1")
        self.assertEqual(result.status, response_data["status"])

    def test_list(self):
        orders_data = [self.order_data]
        self.api_mock.get_orders.return_value = orders_data
        expected_orders = [Order(**d) for d in orders_data]
        result = Order.list()
        self.api_mock.get_orders.assert_called_once_with()
        self.assertEqual(result, expected_orders)

    def test_retrieve(self):
        expected_order = Order(**self.order_data)
        self.api_mock.get_order_by_id.return_value = self.order_data
        result = Order.retrieve(order_id="1")
        self.api_mock.get_order_by_id.assert_called_once_with("1")
        self.assertEqual(result, expected_order)

    def test_capture(self):
        expected_order = Order(**self.order_data)
        response_data = {
            "id": "string",
            "order_id": "string",
            "status": "PENDING",
            "created_at": "2019-08-24T14:15:22Z",
            "approved_amount": 0,
            "captured_amount": 0,
            "refunded_amount": 0,
            "processing_fee": 0,
            "payer": {
                "type": "CARD",
                "pan_masked": "string",
                "expiry_date": "string",
                "holder": "string",
                "payment_system": "string",
                "emitter": "string",
                "email": "user@example.com",
                "phone": "string",
                "customer_id": "string",
                "card_id": "string",
            },
            "error": {"code": "string", "message": "string"},
            "acquirer": {"name": "string", "reference": "string"},
            "action": {"url": "string"},
        }
        self.api_mock.capture_order.return_value = response_data
        result = expected_order.capture()
        self.api_mock.capture_order.assert_called_once_with(order_id="1")
        self.assertEqual(result.status, response_data["status"])

    def test_get_events(self):
        expected_order = Order(**self.order_data)
        response_data = [
            {
                "id": "string",
                "name": "ORDER_CREATED",
                "created_at": "2022-03-18T12:00:00",
                "order_id": "1",
                "payment_id": "1",
                "refund_id": "1",
                "md": "123",
                "pa_req": "123",
                "acs_url": "https://ioka.kz",
                "term_url": "https://ioka.kz",
                "action_url": "https://ioka.kz",
                "code": "213",
                "message": "message",
            }
        ]
        self.api_mock.get_order_events.return_value = response_data
        expected_events = [Event(**e) for e in response_data]
        result = expected_order.get_events()
        self.api_mock.get_order_events.assert_called_once_with(order_id="1")
        self.assertEqual(result, expected_events)


if __name__ == "__main__":
    unittest.main()
