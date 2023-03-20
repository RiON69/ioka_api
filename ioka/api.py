import logging
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4

import requests
from pydantic import BaseModel, Field, HttpUrl, SecretStr

logger = logging.getLogger("ioka")


class ISODatetime(str):
    """Datetime value in the UTC+0 time zone in the format described in RFC 3339.
    For example: "2019-08-24T14:15:22"
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            dt = datetime.fromisoformat(v.replace("Z", ""))
        elif isinstance(v, datetime):
            dt = v
        else:
            raise TypeError("Datetime string RFC 3339 or datetime required")

        return dt.replace(tzinfo=None).isoformat()


CAPTURE_METHOD_AUTO = "AUTO"
CAPTURE_METHOD_MANUAL = "MANUAL"


class CaptureMethodEnum(str, Enum):
    auto = CAPTURE_METHOD_AUTO
    manual = CAPTURE_METHOD_MANUAL


class OrderStatusEnum(str, Enum):
    expired = "EXPIRED"
    unpaid = "UNPAID"
    on_hold = "ON_HOLD"
    paid = "PAID"


CURRENCY_KZT = "KZT"
CURRENCY_USD = "USD"
CURRENCY_RUB = "RUB"


class CurrencyEnum(str, Enum):
    kzt = CURRENCY_KZT
    usd = CURRENCY_USD
    rub = CURRENCY_RUB


class CreateOrder(BaseModel):
    amount: int = Field(..., ge=100)
    currency: Optional[CurrencyEnum]
    capture_method: Optional[CaptureMethodEnum]
    external_id: str = Field(str(uuid4()), min_length=1)
    description: Optional[str]
    mcc: Optional[str] = Field(None, min_length=4, max_length=4)
    extra_info: Optional[dict]
    attempts: int = Field(10, ge=1, le=50)
    due_date: Optional[str]
    customer_id: Optional[str] = Field(None, min_length=1)
    card_id: Optional[str] = Field(None, min_length=1)
    back_url: Optional[HttpUrl]
    success_url: Optional[HttpUrl]
    failure_url: Optional[HttpUrl]
    template: Optional[str]

    class Config:
        use_enum_values = True


class CancelOrder(BaseModel):
    order_id: str
    reason: str = Field(..., max_length=255)


PAYMENT_STATUS_PENDING = "PENDING"
PAYMENT_STATUS_REQUIRES_ACTION = "REQUIRES_ACTION"
PAYMENT_STATUS_APPROVED = "APPROVED"
PAYMENT_STATUS_CAPTURED = "CAPTURED"
PAYMENT_STATUS_CANCELLED = "CANCELLED"
PAYMENT_STATUS_DECLINED = "DECLINED"


class PaymentStatusEnum(str, Enum):
    pending = PAYMENT_STATUS_PENDING
    requires_action = PAYMENT_STATUS_REQUIRES_ACTION
    approved = PAYMENT_STATUS_APPROVED
    captured = PAYMENT_STATUS_CAPTURED
    cancelled = PAYMENT_STATUS_CANCELLED
    declined = PAYMENT_STATUS_DECLINED


PAYER_TYPE_CARD = "CARD"
PAYER_TYPE_CARD_NO_CVC = "CARD_NO_CVC"
PAYER_TYPE_CARD_WITH_BINDING = "CARD_WITH_BINDING"
PAYER_TYPE_BINDING = "BINDING"
PAYER_TYPE_APPLE_PAY = "APPLE_PAY"
PAYER_TYPE_GOOGLE_PAY = "GOOGLE_PAY"
PAYER_TYPE_MASTERPASS = "MASTERPASS"


class PayerTypeEnum(str, Enum):
    card = PAYER_TYPE_CARD
    card_no_cvc = PAYER_TYPE_CARD_NO_CVC
    card_with_binding = PAYER_TYPE_CARD_WITH_BINDING
    binding = PAYER_TYPE_BINDING
    apple_pay = PAYER_TYPE_APPLE_PAY
    google_pay = PAYER_TYPE_GOOGLE_PAY
    masterpass = PAYER_TYPE_MASTERPASS


class Payer(BaseModel):
    type: PayerTypeEnum
    pan_masked: Optional[str]
    expiry_date: Optional[str]
    holder: Optional[str]
    payment_system: Optional[str]
    emitter: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    customer_id: Optional[str]
    card_id: Optional[str]


class Error(BaseModel):
    code: str
    message: str


class Acquirer(BaseModel):
    name: str
    reference: Optional[str]


class Action(BaseModel):
    url: str


class CancelOrderResponse(BaseModel):
    id: str
    order_id: str
    status: PaymentStatusEnum
    created_at: ISODatetime
    approved_amount: int
    captured_amount: int
    refunded_amount: int
    processing_fee: float
    payer: Optional[Payer]
    error: Optional[Error]
    acquirer: Optional[Acquirer]
    action: Optional[Action]


class CaptureOrder(BaseModel):
    amount: int = Field(..., ge=100)
    reason: str = Field(None, max_length=255)


class CaptureOrderResponse(CancelOrderResponse):
    ...


EVENT_NAME_ORDER_CREATED = "ORDER_CREATED"
EVENT_NAME_PAYMENT_CREATED = "PAYMENT_CREATED"
EVENT_NAME_REFUND_CREATED = "REFUND_CREATED"
EVENT_NAME_INSTALLMENT_CREATED = "INSTALLMENT_CREATED"
EVENT_NAME_SPLIT_CREATED = "SPLIT_CREATED"
EVENT_NAME_ORDER_ON_HOLD = "ORDER_ON_HOLD"
EVENT_NAME_ORDER_PAID = "ORDER_PAID"
EVENT_NAME_ORDER_EXPIRED = "ORDER_EXPIRED"
EVENT_NAME_PAYMENT_DECLINED = "PAYMENT_DECLINED"
EVENT_NAME_PAYMENT_ACTION_REQUIRED = "PAYMENT_ACTION_REQUIRED"
EVENT_NAME_PAYMENT_APPROVED = "PAYMENT_APPROVED"
EVENT_NAME_PAYMENT_CAPTURED = "PAYMENT_CAPTURED"
EVENT_NAME_CAPTURE_DECLINED = "CAPTURE_DECLINED"
EVENT_NAME_PAYMENT_CANCELLED = "PAYMENT_CANCELLED"
EVENT_NAME_CANCEL_DECLINED = "CANCEL_DECLINED"
EVENT_NAME_REFUND_APPROVED = "REFUND_APPROVED"
EVENT_NAME_REFUND_DECLINED = "REFUND_DECLINED"
EVENT_NAME_SPLIT_APPROVED = "SPLIT_APPROVED"
EVENT_NAME_SPLIT_DECLINED = "SPLIT_DECLINED"
EVENT_NAME_SPLIT_REFUND_APPROVED = "SPLIT_REFUND_APPROVED"
EVENT_NAME_SPLIT_REFUND_DECLINED = "SPLIT_REFUND_DECLINED"
EVENT_NAME_CHECK_APPROVED = "CHECK_APPROVED"
EVENT_NAME_CHECK_DECLINED = "CHECK_DECLINED"
EVENT_NAME_OTP_SENT = "OTP_SENT"
EVENT_NAME_SEND_OTP_DECLINED = "SEND_OTP_DECLINED"
EVENT_NAME_OTP_CONFIRMED = "OTP_CONFIRMED"
EVENT_NAME_CONFIRM_OTP_DECLINED = "CONFIRM_OTP_DECLINED"
EVENT_NAME_INSTALLMENT_ACTION_REQUIRED = "INSTALLMENT_ACTION_REQUIRED"
EVENT_NAME_INSTALLMENT_ISSUED = "INSTALLMENT_ISSUED"
EVENT_NAME_INSTALLMENT_REJECTED = "INSTALLMENT_REJECTED"
EVENT_NAME_INSTALLMENT_DECLINED = "INSTALLMENT_DECLINED"


class EventNameEnum(str, Enum):
    order_created = EVENT_NAME_ORDER_CREATED
    payment_created = EVENT_NAME_PAYMENT_CREATED
    refund_created = EVENT_NAME_REFUND_CREATED
    installment_created = EVENT_NAME_INSTALLMENT_CREATED
    split_created = EVENT_NAME_SPLIT_CREATED
    order_on_hold = EVENT_NAME_ORDER_ON_HOLD
    order_paid = EVENT_NAME_ORDER_PAID
    order_expired = EVENT_NAME_ORDER_EXPIRED
    payment_declined = EVENT_NAME_PAYMENT_DECLINED
    payment_action_required = EVENT_NAME_PAYMENT_ACTION_REQUIRED
    payment_approved = EVENT_NAME_PAYMENT_APPROVED
    payment_captured = EVENT_NAME_PAYMENT_CAPTURED
    capture_declined = EVENT_NAME_CAPTURE_DECLINED
    payment_cancelled = EVENT_NAME_PAYMENT_CANCELLED
    cancel_declined = EVENT_NAME_CANCEL_DECLINED
    refund_approved = EVENT_NAME_REFUND_APPROVED
    refund_declined = EVENT_NAME_REFUND_DECLINED
    split_approved = EVENT_NAME_SPLIT_APPROVED
    split_declined = EVENT_NAME_SPLIT_DECLINED
    split_refund_approved = EVENT_NAME_SPLIT_REFUND_APPROVED
    split_refund_declined = EVENT_NAME_SPLIT_REFUND_DECLINED
    check_approved = EVENT_NAME_CHECK_APPROVED
    check_declined = EVENT_NAME_CHECK_DECLINED
    otp_sent = EVENT_NAME_OTP_SENT
    send_otp_declined = EVENT_NAME_SEND_OTP_DECLINED
    otp_confirmed = EVENT_NAME_OTP_CONFIRMED
    confirm_otp_declined = EVENT_NAME_CONFIRM_OTP_DECLINED
    installment_action_required = EVENT_NAME_INSTALLMENT_ACTION_REQUIRED
    installment_issued = EVENT_NAME_INSTALLMENT_ISSUED
    installment_rejected = EVENT_NAME_INSTALLMENT_REJECTED
    installment_declined = EVENT_NAME_INSTALLMENT_DECLINED


class Event(BaseModel):
    id: str
    name: EventNameEnum
    created_at: ISODatetime
    order_id: str
    payment_id: Optional[str]
    refund_id: Optional[str]
    md: Optional[str]
    pa_req: Optional[str]
    acs_url: Optional[HttpUrl]
    term_url: Optional[HttpUrl]
    action_url: Optional[HttpUrl]
    code: Optional[str]
    message: Optional[str]

    class Config:
        use_enum_values = True


class RefundRule(BaseModel):
    account_id: str
    amount: int


OPERATION_TYPE_WITHOUT_VAT = 0
OPERATION_TYPE_WITH_VAT = 100


class OperationTypeEnum(int, Enum):
    without_vat = OPERATION_TYPE_WITHOUT_VAT
    with_vat = OPERATION_TYPE_WITH_VAT


class CheckPosition(BaseModel):
    name: str
    amount: int
    count: int
    section: Optional[int]
    tax_percent: Optional[int] = 0
    tax_type: Optional[OperationTypeEnum] = OPERATION_TYPE_WITHOUT_VAT
    tax_amount: Optional[int] = 0
    unit_code: Optional[int] = 0

    class Config:
        use_enum_values = True


class RefundOrder(BaseModel):
    amount: int = Field(..., ge=100)
    reason: Optional[str] = Field(None, max_length=255)
    rules: Optional[List[RefundRule]]
    positions: Optional[List[CheckPosition]]


REFUND_STATUS_PENDING = "PENDING"
REFUND_STATUS_APPROVED = "APPROVED"
REFUND_STATUS_DECLINED = "DECLINED"


class RefundStatusEnum(str, Enum):
    pending = REFUND_STATUS_PENDING
    approved = REFUND_STATUS_APPROVED
    declined = REFUND_STATUS_DECLINED


class Refund(BaseModel):
    id: str
    payment_id: str
    order_id: str
    status: RefundStatusEnum
    created_at: ISODatetime
    error: Optional[Error]
    acquirer: Optional[Acquirer]

    class Config:
        use_enum_values = True


class Order(BaseModel):
    id: str
    shop_id: str
    status: OrderStatusEnum
    created_at: ISODatetime
    amount: int
    currency: CurrencyEnum
    capture_method: CaptureMethodEnum
    external_id: Optional[str] = Field(None, min_length=1)
    description: Optional[str]
    extra_info: Optional[Dict]
    attempts: Optional[int] = Field(10, ge=0, le=50)
    due_date: Optional[str]
    customer_id: Optional[str] = Field(None, min_length=1)
    card_id: Optional[str] = Field(None, min_length=1)
    mcc: Optional[str] = Field(None, min_length=4, max_length=4)
    back_url: Optional[HttpUrl]
    success_url: Optional[HttpUrl]
    failure_url: Optional[HttpUrl]
    template: Optional[str]
    checkout_url: Optional[HttpUrl]
    access_token: Optional[str]

    class Config:
        use_enum_values = True

    @classmethod
    def set_api(cls, api: object) -> object:
        cls.api = api
        return cls

    @classmethod
    def create(cls, **data) -> object:
        """Создание нового заказа.
        https://ioka.kz/docs_v2.html#tag/orders/operation/CreateOrder

        Args:
            amount (int): >= 100. Стоимость предлагаемых товаров или услуг в минорных
            денежных единицах. Например, для создания заказа на сумму 500 тенге,
            необходимо ввести 50000 (1 тенге = 100 тиын)
            currency (CurrencyEnum): "KZT". Валюта платежа
            capture_method (CaptureMethodEnum): Способ списания платежа.
            AUTO - автоматический т.е. одностадийный платеж.
            MANUAL - двухстадийный платеж, где первая стадия - авторизация платежа,
            вторая - подтверждение списания платежа. Подробнее в документации.
            external_id	(str): non-empty. Внешний идентификатор заказа
            description	(str): Описание заказа
            mcc	(str): 4 characters. MCC Код
            extra_info (dict): Дополнительные данные, связанные с заказом
            attempts (int): [ 1 .. 50 ]. Количество разрешенных попыток оплаты для заказа.
            Defaults to 10.
            due_date (str): Срок действия заказа
            customer_id	(str): non-empty. Идентификатор плательщика. Для оплаты по
            сохраненной карте через форму оплаты с подтверждением CVC.
            card_id (str): non-empty. Идентификатор сохраненной карты плательщика.
            Для оплаты по сохраненной карте через форму оплаты с подтверждением CVC.
            back_url (str): <uri> [ 1 .. 2083 ] characters. Ссылка, служащая для
            перенаправления клиента на сайт мерчанта после проведения оплаты
            success_url (str): <uri> [ 1 .. 2083 ] characters. Ссылка, служащая для
            перенаправления клиента на сайт мерчанта после успешного проведения оплаты
            failure_url (str): <uri> [ 1 .. 2083 ] characters. Ссылка, служащая для
            перенаправления клиента на сайт мерчанта после неуспешного проведения оплаты
            template (str): Шаблон формы оплаты

        Returns:
            Order: Order
        """
        return cls(**cls.api.create_order(**data).get("order"))

    @classmethod
    def cancel(cls, **data) -> object:
        return CancelOrderResponse(**cls.api.cancel_order(**data))

    @classmethod
    def list(cls) -> List[object]:
        return [cls(**d) for d in cls.api.get_orders()]

    @classmethod
    def retrieve(cls, order_id: str) -> object:
        return cls(**cls.api.get_order_by_id(order_id))

    def capture(self, **data) -> object:
        return CaptureOrderResponse(**self.api.capture_order(order_id=self.id, **data))

    def get_events(self) -> List[object]:
        return [Event(**e) for e in self.api.get_order_events(order_id=self.id)]

    def refund(self, **data) -> object:
        return Refund(**self.api.refund_order(order_id=self.id, **data))

    def refund_list(self):
        return [Refund(**r) for r in self.api.get_refunds(order_id=self.id)]

    def refund_retrieve(self, refund_id: str):
        return Refund(**self.api.get_refund_by_id(self.id, refund_id))


class Payment(BaseModel):
    pass


class Card(BaseModel):
    pass


class Webhook(BaseModel):
    pass


class Api(BaseModel):
    api_host: HttpUrl = "https://stage-api.ioka.kz"
    api_key: SecretStr
    version: str = "v2"
    headers: dict = {}

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.headers = {"API-KEY": self.api_key, "Content-Type": "application/json"}

    def _request(
        self, method: str, url: str, params: dict = None, params_type: str = "json", headers: dict = None, raise_for_status: bool = True
    ) -> requests.Response | dict:
        """Отправка запроса

        Args:
            method (str): Метод запроса
            url (str): Урл
            params (dict): Параметры запроса
            params_type (str, optional): Тип параметров. Defaults to "json".
            headers (dict, optional): Заголовки. Defaults to self.headers.
            raise_for_status (bool, optional): Вызвать исключение при отрицательном статусе. Defaults to True.

        Returns:
            requests.Response | dict: Response
        """

        headers = headers or self.headers
        url = f"{self.api_host}/{self.version}/" + url

        logger.debug(
            f"Ioka api request with: method={method}, url={url}, params={params}, "
            f"params_type={params_type}, headers={headers}, raise_for_status={raise_for_status}"
        )

        headers["API-KEY"] = self.api_key.get_secret_value()

        if params:
            response = requests.request(method, url, headers=headers, **{params_type: params})
        else:
            response = requests.request(method, url, headers=headers)

        logger.debug(f"Ioka api response: response={response}, text={response.text}")

        if raise_for_status:
            response.raise_for_status()
            return response.json()

        return response

    # ORDER
    def create_order(self, **data) -> dict:
        """Создание нового заказа.
        https://ioka.kz/docs_v2.html#tag/orders/operation/CreateOrder
        """

        request_params = {
            "method": "post",
            "url": "orders",
            "params": CreateOrder(**data).dict(exclude_unset=True),
        }

        return self._request(**request_params)

    def cancel_order(self, order_id, **data) -> dict:
        """Отмена авторизованного платежа заказа.
        https://ioka.kz/docs_v2.html#tag/orders/operation/CancelOrder
        """

        request_params = {
            "method": "post",
            "url": f"orders/{order_id}/cancel",
            "params": CancelOrder(**data).dict(exclude_unset=True),
        }

        return self._request(**request_params)

    def get_orders(self) -> dict:
        """Поиск заказов по фильтрам.
        https://ioka.kz/docs_v2.html#tag/orders/operation/GetOrders
        """

        request_params = {
            "method": "get",
            "url": "orders",
        }

        return self._request(**request_params)

    def get_order_by_id(self, order_id: str) -> dict:
        """Получение заказа по ID.
        https://ioka.kz/docs_v2.html#tag/orders/operation/GetOrderByID
        """

        request_params = {
            "method": "get",
            "url": f"orders/{order_id}",
        }

        return self._request(**request_params)

    def capture_order(self, order_id: str, **data) -> dict:
        """Полное или частичное списание авторизованного платежа заказа.
        https://ioka.kz/docs_v2.html#tag/orders/operation/CaptureOrder
        """

        request_params = {
            "method": "post",
            "url": f"orders/{order_id}/capture",
            "params": CaptureOrder(**data).dict(exclude_unset=True),
        }

        return self._request(**request_params)

    def get_order_events(self, order_id: str) -> dict:
        """Получение истории событий по заказу.
        https://ioka.kz/docs_v2.html#tag/orders/operation/GetOrderEvents
        """

        request_params = {
            "method": "get",
            "url": f"orders/{order_id}/events",
        }

        return self._request(**request_params)

    def refund_order(self, order_id: str, **data) -> dict:
        """Создание нового возврата по списанному платежу.
        https://ioka.kz/docs_v2.html#tag/orders/operation/RefundOrder
        """
        request_params = {
            "method": "post",
            "url": f"orders/{order_id}/refunds",
            "params": RefundOrder(**data).dict(exclude_unset=True),
        }

        return self._request(**request_params)

    def get_refunds(self, order_id: str) -> dict:
        """Выдача возвратов.
        https://ioka.kz/docs_v2.html#tag/orders/operation/GetRefundByID
        """

        request_params = {
            "method": "get",
            "url": f"orders/{order_id}/refunds",
        }

        return self._request(**request_params)

    def get_refund_by_id(self, order_id: str, refund_id: str) -> dict:
        """Выдача возвратов по идентификатору.
        https://ioka.kz/docs_v2.html#tag/orders/operation/GetRefundByID
        """

        request_params = {
            "method": "get",
            "url": f"orders/{order_id}/refunds/{refund_id}",
        }

        return self._request(**request_params)


class Ioka(Api):
    @property
    def order(self):
        return Order.set_api(self)
