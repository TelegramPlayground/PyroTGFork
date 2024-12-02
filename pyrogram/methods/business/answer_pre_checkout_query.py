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
from pyrogram import raw


class AnswerPreCheckoutQuery:
    async def answer_pre_checkout_query(
        self: "pyrogram.Client",
        pre_checkout_query_id: str,
        ok: bool,
        error_message: str = None
    ):
        """Once the user has confirmed their payment and shipping details, the API sends the final confirmation in the form of an :obj:`~pyrogram.handlers.PreCheckoutQueryHandler`.
        
        Use this method to respond to such pre-checkout queries.

        .. note::

            The API must receive an answer within 10 seconds after the pre-checkout query was sent.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            pre_checkout_query_id (``str``):
                Unique identifier for the query to be answered.

            ok (``bool``):
                Specify True if everything is alright (goods are available, etc.) and the bot is ready to proceed with the order. Use False if there are any problems.

            error_message (``str``, *optional*):
                Required if ok is False. Error message in human readable form that explains the reason for failure to proceed with the checkout (e.g. "Sorry, somebody just bought the last of our amazing black T-shirts while you were busy filling out your payment details. Please choose a different color or garment!"). Telegram will display this message to the user.

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                # Proceed with the order
                await app.answer_pre_checkout_query(query_id, ok=True)

                # Answer with error message
                await app.answer_pre_checkout_query(query_id, ok=False, error_message="Error Message displayed to the user")

        """
        return await self.invoke(
            raw.functions.messages.SetBotPrecheckoutResults(
                query_id=int(pre_checkout_query_id),
                success=ok or None,
                error=error_message or None
            )
        )
