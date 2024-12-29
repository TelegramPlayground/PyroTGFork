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

from typing import Union

import pyrogram
from pyrogram import raw, types


class SendPaymentForm:
    async def send_payment_form(
        self: "pyrogram.Client",
        *,
        chat_id: Union[int, str] = None,
        message_id: int = None,
        invoice_link: str = None
    ) -> Union[
        bool,
        list["types.PaidMediaPhoto"],
        list["types.PaidMediaVideo"]
    ]:
        """Pay an invoice.

        .. note::

            For now only stars invoices are supported.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                of the target channel/supergroup (in the format @username).

            message_id (``int``):
                Pass a message identifier or to get the invoice from message.

            invoice_link (``str``):
                Pass a invoice link in form of a *t.me/$...* link or slug itself to pay this invoice.

        Returns:
            ``bool`` | List of :obj:`~pyrogram.types.PaidMediaPhoto` | List of :obj:`~pyrogram.types.PaidMediaVideo`: On success, the list of bought photos and videos is returned.

        Example:
            .. code-block:: python

                # Pay invoice from message
                app.send_payment_form(chat_id=chat_id, message_id=123)

                # Pay invoice form from link
                app.send_payment_form(invoice_link="https://t.me/$xvbzUtt5sUlJCAAATqZrWRy9Yzk")
        """
        if not any((all((chat_id, message_id)), invoice_link)):
            raise ValueError("You should pass at least one parameter to this method.")

        form = None
        invoice = None

        if message_id:
            invoice = raw.types.InputInvoiceMessage(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id
            )
        elif invoice_link:
            match = self.INVOICE_LINK_RE.match(invoice_link)
            if match:
                slug = match.group(1)
            else:
                slug = invoice_link

            invoice = raw.types.InputInvoiceSlug(
                slug=slug
            )

        form = await self.get_payment_form(chat_id=chat_id, message_id=message_id, invoice_link=invoice_link)

        # if form.invoice.currency == "XTR":
        r = await self.invoke(
            raw.functions.payments.SendStarsForm(
                form_id=form.id,
                invoice=invoice
            )
        )
        # TODO: Add support for regular invoices (credentials)
        # else:
        #     r = await self.invoke(
        #         raw.functions.payments.SendPaymentForm(
        #             form_id=form.id,
        #             invoice=invoice,
        #             credentials=raw.types.InputPaymentCredentials(data=raw.types.DataJSON(data={}))
        #         )
        #     )

        medias = []
        if isinstance(r, raw.types.payments.PaymentResult):
            for i in r.updates.updates:
                if isinstance(i, raw.types.UpdateMessageExtendedMedia):
                    for ext_media in i.extended_media:
                        paid_media = types.PaidMedia._parse(
                            self,
                            ext_media
                        )
                        if paid_media:
                            medias.append(paid_media)

        return types.List(medias) if medias else True
