#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present <https://github.com/TelegramPlayGround>
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


class PaidMessagePriceChanged(Object):
    """Describes a service message about a change in the price of paid messages within a chat.

    Parameters:
        paid_message_star_count (``int``):
            The new number of Telegram Stars that must be paid by non-administrator users of the supergroup chat for each sent message.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        paid_message_star_count: int = None
    ):
        super().__init__(client)

        self.paid_message_star_count = paid_message_star_count


    @staticmethod
    def _parse_action(
        client,
        action: "raw.types.MessageActionPaidMessagesPrice"
    ) -> "PaidMessagePriceChanged":
        if isinstance(action, raw.types.MessageActionPaidMessagesPrice):
            return PaidMessagePriceChanged(
                client=client,
                paid_message_star_count=action.stars
            )
