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


class DirectMessagePriceChanged(Object):
    """Describes a service message about a change in the price of direct messages sent to a channel chat.

    Parameters:
        are_direct_messages_enabled (``bool``):
            True, if direct messages are enabled for the channel chat; False otherwise.

        direct_message_star_count (``int``, *optional*):
            The new number of Telegram Stars that must be paid by users for each direct message sent to the channel. Does not apply to users who have been exempted by administrators. Defaults to 0.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        are_direct_messages_enabled: bool = None,
        direct_message_star_count: int = 0,
    ):
        super().__init__(client)

        self.are_direct_messages_enabled = are_direct_messages_enabled
        self.direct_message_star_count = direct_message_star_count


    @staticmethod
    def _parse_action(
        client,
        action: "raw.types.MessageActionPaidMessagesPrice"
    ) -> "DirectMessagePriceChanged":
        if isinstance(action, raw.types.MessageActionPaidMessagesPrice):
            return DirectMessagePriceChanged(
                client=client,
                are_direct_messages_enabled=True, #action.broadcast_messages_allowed,
                direct_message_star_count=action.stars,
            )
