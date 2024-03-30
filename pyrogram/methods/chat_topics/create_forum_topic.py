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
from typing import Union, List

import pyrogram
from pyrogram import types, utils, raw


class CreateForumTopic:
    async def create_forum_topic(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        name: str,
        icon_color: int = None,
        icon_custom_emoji_id: str = None,
        send_as: Union[int, str] = None,
    ) -> "types.Message":
        """Use this method to create a topic in a forum supergroup chat.
        The bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            name (``str``):
                Topic name, 1-128 characters

            icon_color (``int``, *optional*):
                Color of the topic icon in RGB format.
                Currently, must be one of 7322096 (0x6FB9F0), 16766590 (0xFFD67E), 13338331 (0xCB86DB), 9367192 (0x8EEE98), 16749490 (0xFF93B2), or 16478047 (0xFB6F5F)

            icon_custom_emoji_id (``str``, *optional*):
                Unique identifier of the custom emoji shown as the topic icon. Use :meth:`~pyrogram.Client.getForumTopicIconStickers` to get all allowed custom emoji identifiers.

            send_as (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the as chat.
                For your personal cloud (Saved Messages) you can simply use "me".
                Use :meth:`~pyrogram.Client.get_send_as_chats` to get allowed values.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent text message is returned.

        Example:
            .. code-block:: python

                # Create a new Topic
                await app.create_forum_topic(chat, "Topic Title")
        """

        r = await self.invoke(
            raw.functions.channels.CreateForumTopic(
                channel=await self.resolve_peer(chat_id),
                title=name,
                icon_color=icon_color,
                icon_emoji_id=icon_custom_emoji_id,
                send_as=await self.resolve_peer(send_as) if send_as else None,
                random_id=self.rnd_id()
            )
        )

        for i in r.updates:
            if isinstance(
                i,
                (
                    raw.types.UpdateNewMessage,
                    raw.types.UpdateNewChannelMessage,
                    raw.types.UpdateNewScheduledMessage
                )
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage),
                    replies=2
                )
