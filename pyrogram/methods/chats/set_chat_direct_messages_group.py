#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present <https://github.com/KurimuzonAkuma>
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

from typing import Optional, Union

import pyrogram
from pyrogram import types, raw


class SetChatDirectMessagesGroup:
    async def set_chat_direct_messages_group(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        is_enabled: bool = Optional[None],
        paid_message_star_count: int = 0,
    ) -> Union["types.Message", bool]:
        """Change direct messages group settings for a channel chat.

        .. include:: /_includes/usable-by/users.rst

        Requires owner privileges in the chat.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            is_enabled (``bool``, *optional*):
                Pass True if the direct messages group is enabled for the channel chat. Pass False otherwise.

            paid_message_star_count (``bool``):
                The new number of Telegram Stars that must be paid for each message that is sent to the direct messages chat unless the sender is an administrator of the channel chat, 0-``stars_paid_message_amount_max``.

        Returns:
            :obj:`~pyrogram.types.Message` | ``bool``: On success, a service message will be returned (when applicable),
            otherwise, in case a message object couldn't be returned, True is returned.
        
        Raises:
            RPCError: In case of a Telegram RPC error.

        Example:
            .. code-block:: python

                # Enable direct messages
                await app.set_chat_direct_messages_group(chat_id, is_enabled=True)

        """

        r = await self.invoke(
            raw.functions.channels.UpdatePaidMessagesPrice(
                channel=await self.resolve_peer(chat_id),
                send_paid_messages_stars=paid_message_star_count,
                broadcast_messages_allowed=is_enabled
            )
        )
        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}
        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage, raw.types.UpdateNewChannelMessage)):
                return await types.Message._parse(
                    self,
                    i.message,
                    users,
                    chats,
                    replies=self.fetch_replies
                )
        else:
            return True
