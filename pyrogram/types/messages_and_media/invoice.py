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

from typing import Optional

from pyrogram import raw
from ..object import Object


class Invoice(Object):
    """This object contains basic information about an invoice.

    Parameters:
        title (``str``):
            Product name.

        description (``str``):
            Product description.

        start_parameter (``str``):
            Unique bot deep-linking parameter that can be used to generate this invoice.

        currency (``str``):
            Three-letter ISO 4217 `currency <https://core.telegram.org/bots/payments#supported-currencies>`_ code.

        total_amount (``int``):
            Total price in the smallest units of the currency (integer, **not** float/double). For example, for a price of ``US$ 1.45`` pass ``amount = 145``. See the exp parameter in `currencies.json <https://core.telegram.org/bots/payments/currencies.json>`_, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).

        is_shipping_address_requested (``bool``, *optional*):
            True, if the shipping address should be specified.

        is_test (``bool``, *optional*):
            True, if the invoice is a test invoice.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        title: str,
        description: str,
        currency: str,
        total_amount: int,
        start_parameter: Optional[str] = None,
        is_shipping_address_requested: Optional[bool] = None,
        is_test: Optional[bool] = None
    ):
        super().__init__(client)

        self.title = title
        self.description = description
        self.is_shipping_address_requested = is_shipping_address_requested
        self.currency = currency
        self.start_parameter = start_parameter
        self.total_amount = total_amount
        self.is_test = is_test

    @staticmethod
    def _parse(client, invoice: "raw.types.MessageMediaInvoice") -> "Invoice":
        return Invoice(
            title=invoice.title,
            description=invoice.description,
            currency=invoice.currency,
            total_amount=invoice.total_amount,
            start_parameter=invoice.start_param or None,
            is_shipping_address_requested=getattr(invoice, "shipping_address_requested", None),
            is_test=getattr(invoice, "test", None),
            client=client
            # TODO: Add photo and extended media
        )
