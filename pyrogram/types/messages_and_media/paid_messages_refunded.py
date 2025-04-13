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


class PaidMessagesRefunded(Object):
    """Describes a service message about refunded paid messages.

    Parameters:
        message_count (``int``):
            The number of refunded messages.

        star_count (``int``):
            The number of refunded Telegram Stars.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        message_count: int = None,
        star_count: int = None
    ):
        super().__init__(client)

        self.message_count = message_count
        self.star_count = star_count


    @staticmethod
    def _parse_action(
        client,
        action: "raw.types.MessageActionPaidMessagesRefunded"
    ) -> "PaidMessagesRefunded":
        if isinstance(action, raw.types.MessageActionPaidMessagesRefunded):
            return PaidMessagesRefunded(
                client=client,
                message_count=action.count,
                star_count=action.stars
            )
