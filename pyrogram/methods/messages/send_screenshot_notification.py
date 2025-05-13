#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present <https://github.com/TelegramPlayground>
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
from pyrogram import types, raw, utils


class SendScreenshotNotification:
    async def send_screenshot_notification(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_thread_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
    ) -> "types.Message":
        """Notify the other user in a chat that screenshot of the chat was taken.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_thread_id (``int``, *optional*):
                If the message is in a thread, ID of the original message.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent service message is returned.

        """

        reply_to = await utils._get_reply_message_parameters(
            self,
            message_thread_id,
            reply_parameters
        )
        r = await self.invoke(
            raw.functions.messages.SendScreenshotNotification(
                peer=await self.resolve_peer(chat_id),
                reply_to=reply_to,
                random_id=self.rnd_id()
            )
        )

        for i in r.updates:
            if isinstance(
                i,
                (
                    raw.types.UpdateNewMessage,
                    raw.types.UpdateNewChannelMessage
                )
            ):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )
