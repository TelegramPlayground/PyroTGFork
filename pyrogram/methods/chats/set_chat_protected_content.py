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


class SetChatProtectedContent:
    async def set_chat_protected_content(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        enabled: bool
    ) -> Union["types.Message", bool]:
        """Set the chat protected content setting.

        .. include:: /_includes/usable-by/users.rst

        Changes the ability of users to save, forward, or copy chat content.
        
        Requires owner privileges in basic groups, supergroups and channels.
        Requires Telegram Premium to enable protected content in private chats. Not available in Saved Messages and private chats with bots or support accounts.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            enabled (``bool``):
                Pass True to enable the protected content setting, False to disable.

        Returns:
            :obj:`~pyrogram.types.Message` | ``bool``: On success, a service message will be returned (when applicable),
            otherwise, in case a message object couldn't be returned, True is returned.

        Raises:
            RPCError: In case of a Telegram RPCError.

        """
        r = await self.invoke(
            raw.functions.messages.ToggleNoForwards(
                peer=await self.resolve_peer(chat_id),
                enabled=enabled
            )
        )
        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage, raw.types.UpdateNewChannelMessage)):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    replies=self.fetch_replies
                )
        return True


    async def process_chat_protected_content_disable_request(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        request_message_id: int,
        enabled: bool
    ) -> Union["types.Message", bool]:
        """Processes request to disable ``has_protected_content`` in a chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            request_message_id (``int``):
                Identifier of the message with the request. The message must be incoming and has ``message.service`` of the type :obj:`~pyrogram.types.ChatHasProtectedContentToggled`.

            enabled (``bool``):
                Pass True to approve the request; pass False to reject the request.

        Returns:
            :obj:`~pyrogram.types.Message` | ``bool``: On success, a service message will be returned (when applicable),
            otherwise, in case a message object couldn't be returned, True is returned.

        Raises:
            RPCError: In case of a Telegram RPCError.
        
        """
        r = await self.invoke(
            raw.functions.messages.ToggleNoForwards(
                peer=await self.resolve_peer(chat_id),
                enabled=enabled,
                request_msg_id=request_message_id
            )
        )
        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage, raw.types.UpdateNewChannelMessage)):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    replies=self.fetch_replies
                )
        return True
