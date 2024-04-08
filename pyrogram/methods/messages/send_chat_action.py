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
from pyrogram import raw, enums


class SendChatAction:
    async def send_chat_action(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        action: "enums.ChatAction",
        progress: int = 0,
        message_thread_id: int = None,
        business_connection_id: str = None
    ) -> bool:
        """Use this method when you need to tell the user that something is happening on the bot's side.
        The status is set for 5 seconds or less (when a message arrives from your bot, Telegram clients clear its typing status).

        .. include:: /_includes/usable-by/users-bots.rst

        We only recommend using this method when a response from the bot will take a **noticeable** amount of time to arrive.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            action (:obj:`~pyrogram.enums.ChatAction`):
                Type of action to broadcast.

            progress (``int``, *optional*):
                Upload progress, as a percentage.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread; for supergroups only

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the action will be sent

        Returns:
            ``bool``: On success, True is returned.

        Raises:
            ValueError: In case the provided string is not a valid chat action.

        Example:
            .. code-block:: python

                from pyrogram import enums

                # Send "typing" chat action
                await app.send_chat_action(chat_id, enums.ChatAction.TYPING)

                # Send "upload_video" chat action
                await app.send_chat_action(chat_id, enums.ChatAction.UPLOAD_VIDEO)

                # Send "playing" chat action
                await app.send_chat_action(chat_id, enums.ChatAction.PLAYING)

                # Cancel any current chat action
                await app.send_chat_action(chat_id, enums.ChatAction.CANCEL)
        """

        action_name = action.name.lower()

        if (
            "upload" in action_name or
            "import" in action_name
        ):
            action = action.value(progress=progress)
        else:
            action = action.value()

        rpc = raw.functions.messages.SetTyping(
            peer=await self.resolve_peer(chat_id),
            action=action,
            top_msg_id=message_thread_id
        )
        if business_connection_id:
            return await self.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    query=rpc,
                    connection_id=business_connection_id
                )
            )
        else:
            return await self.invoke(rpc)
