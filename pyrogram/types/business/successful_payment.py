#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from typing import Union

import pyrogram
from pyrogram import raw, types, utils

from ..object import Object


class SuccessfulPayment(Object):
    """This object contains basic information about a successful payment. Note that if the buyer initiates a chargeback with the relevant payment provider following this transaction, the funds may be debited from your balance. This is outside of Telegram's control.

    Parameters:
        currency (``str``):
            Three-letter ISO 4217 `currency <https://core.telegram.org/bots/payments#supported-currencies>`_ code, or ``XTR`` for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

        total_amount (``int``):
            Total price in the smallest units of the currency (integer, **not** float/double). For example, for a price of ``US$ 1.45`` pass ``amount = 145``. See the __exp__ parameter in `currencies.json <https://core.telegram.org/bots/payments/currencies.json>`_, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).

        invoice_payload (``str``):
            Bot specified invoice payload. Only available to the bot that received the payment.

        subscription_expiration_date (:py:obj:`~datetime.datetime`, *optional*):
            Expiration date of the subscription, in Unix time; for recurring payments only.

        is_recurring (``bool``, *optional*):
            True, if the payment is a recurring payment for a subscription.

        is_first_recurring (``bool``, *optional*):
            True, if the payment is the first payment for a subscription.

        shipping_option_id (``str``, *optional*):
            Identifier of the shipping option chosen by the user. Only available to the bot that received the payment.

        order_info (:obj:`~pyrogram.types.OrderInfo`, *optional*):
            Order information provided by the user. Only available to the bot that received the payment.

        telegram_payment_charge_id (``str``):
            Telegram payment identifier. Only available to the bot that received the payment.

        provider_payment_charge_id (``str``):
            Provider payment identifier. Only available to the bot that received the payment.

        invoice_name (``str``, *optional*):
            Name of the invoice; may be empty if unknown

    """

    def __init__(
        self,
        *,
        currency: str,
        total_amount: str,
        invoice_payload: str,
        subscription_expiration_date: datetime = None,
        is_recurring: bool = None,
        is_first_recurring: bool = None,
        shipping_option_id: str = None,
        order_info: "types.OrderInfo" = None,
        telegram_payment_charge_id: str,
        provider_payment_charge_id: str,
        invoice_name: str = None
    ):
        super().__init__()

        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.subscription_expiration_date = subscription_expiration_date
        self.is_recurring = is_recurring
        self.is_first_recurring = is_first_recurring
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info
        self.telegram_payment_charge_id = telegram_payment_charge_id
        self.provider_payment_charge_id = provider_payment_charge_id
        self.invoice_name = invoice_name

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        successful_payment: Union[
            "raw.types.MessageActionPaymentSent",
            "raw.types.MessageActionPaymentSentMe"
        ]
    ) -> "SuccessfulPayment":
        invoice_payload = None
        telegram_payment_charge_id = None
        provider_payment_charge_id = None
        shipping_option_id = None
        order_info = None

        if isinstance(successful_payment, raw.types.MessageActionPaymentSentMe):
            # Try to decode invoice payload into string. If that fails, fallback to bytes instead of decoding by
            # ignoring/replacing errors, this way, button clicks will still work.
            try:
                invoice_payload = successful_payment.payload.decode()
            except (UnicodeDecodeError, AttributeError):
                invoice_payload = successful_payment.payload

            telegram_payment_charge_id = successful_payment.charge.id
            provider_payment_charge_id = successful_payment.charge.provider_charge_id
            shipping_option_id = getattr(successful_payment, "shipping_option_id", None)

            if successful_payment.info:
                payment_info = successful_payment.info
                order_info = types.OrderInfo(
                    name=getattr(payment_info, "name", None),
                    phone_number=getattr(payment_info, "phone", None),
                    email=getattr(payment_info, "email", None),
                    shipping_address=types.ShippingAddress(
                        country_code=payment_info.shipping_address.country_iso2,
                        state=payment_info.shipping_address.state,
                        city=payment_info.shipping_address.city,
                        street_line1=payment_info.shipping_address.street_line1,
                        street_line2=payment_info.shipping_address.street_line2,
                        post_code=payment_info.shipping_address.post_code
                    )
                )

        return SuccessfulPayment(
            currency=successful_payment.currency,
            total_amount=successful_payment.total_amount,
            invoice_payload=invoice_payload,
            telegram_payment_charge_id=telegram_payment_charge_id,
            provider_payment_charge_id=provider_payment_charge_id,
            shipping_option_id=shipping_option_id,
            order_info=order_info,
            is_recurring=getattr(successful_payment, "recurring_used", None),
            is_first_recurring=getattr(successful_payment, "recurring_init", None),
            invoice_name=getattr(successful_payment, "invoice_slug", None),
            subscription_expiration_date=utils.timestamp_to_datetime(successful_payment.subscription_until_date),
        )
