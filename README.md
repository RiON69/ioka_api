# Ioka API SDK
This is a Python SDK for the Ioka payment system API.

## Usage
To use the SDK, you first need to create an instance of the `Ioka` class, passing in your `api_key`:

```python
from ioka.api import Ioka

ioka = Ioka(api_key="your_api_key")
```

By default, API host is used for testing: https://stage-api.ioka.kz

Then, you can use the `order` property to access the Order class, which provides methods for working with orders:

```python
# Create order
order = ioka.order.create(
    shop_id="your_shop_id",
    amount=1000,
    currency="KZT",
    description="Test order",
    back_url="https://yourapp.com/back",
    success_url="https://yourapp.com/success",
    failure_url="https://yourapp.com/failure",
)
print("Created order", order.id)

# list orders
orders = ioka.order.list()

# print the first order's ID
print("First order:", orders[0].id)

# retrieve specific Order
order = ioka.order.retrieve("ord_fSS8SYis1P")

# print that order's amount
print("Order amount:", order.amount)

# order refund list
event_list = order.get_events()
print("First event name:", event_list[0].name)
```

### The Order class provides the following methods:

- `create(**data)`: creates a new order
- `cancel(**data)`: cancels an order
- `list()`: returns a list of all orders
- `retrieve(order_id)`: retrieves an order by ID
- `capture(**data)`: captures an authorized order
- `get_events(order_id)`: returns a list of events for an order
- `refund(**data)`: refunds an order
- `refund_list(order_id)`: returns a list of refunds for an order
- `refund_retrieve(order_id, refund_id)`: retrieves a refund by ID for an order

All of these methods return an instance of the `Order` class or one of its subclasses (`CancelOrderResponse`, `CaptureOrderResponse`, `Refund`). You can access the properties of these objects to get information about the order or refund.

## Data Types
The SDK provides several data types that you can use in your code:

- `Order`: represents an order
- `OrderStatusEnum`: an enumeration of order statuses
- `CurrencyEnum`: an enumeration of currencies
- `CaptureMethodEnum`: an enumeration of capture methods
- `Event`: represents an event for an order
- `Refund`: represents a refund

All of these data types are implemented as `Pydantic` models, which means they have built-in validation and can be easily serialized to and deserialized from JSON.

## Logging
The SDK uses the Python `logging` module for logging. You can configure logging by setting up a logger for the `ioka` namespace:


```python
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("ioka")
```