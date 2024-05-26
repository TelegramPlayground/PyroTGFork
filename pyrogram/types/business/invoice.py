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

import pyrogram
from pyrogram import raw, types
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

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        title: str,
        description: str,
        start_parameter: str,
        currency: str,
        total_amount: int
    ):
        super().__init__(client)

        self.title = title
        self.description = description
        self.start_parameter = start_parameter
        self.currency = currency
        self.total_amount = total_amount

    @staticmethod
    def _parse(client, invoice: "raw.types.MessageMediaInvoice") -> "Invoice":
        return Invoice(
            title=invoice.title,
            description=invoice.description,
            start_parameter=invoice.start_param,
            currency=invoice.currency,
            total_amount=invoice.total_amount,
            # TODO
            client=client
        )
