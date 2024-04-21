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

from json import dumps
from random import randint
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
        business_connection_id: str = None,
        emoji: str = None,
        emoji_message_id: int = None,
        emoji_message_interaction: "raw.types.DataJSON" = None
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

            emoji (``str``, *optional*):
                The animated emoji. Only supported for :obj:`~pyrogram.enums.ChatAction.TRIGGER_EMOJI_ANIMATION` and :obj:`~pyrogram.enums.ChatAction.WATCH_EMOJI_ANIMATION`.

            emoji_message_id (``int``, *optional*):
                Message identifier of the message containing the animated emoji. Only supported for :obj:`~pyrogram.enums.ChatAction.TRIGGER_EMOJI_ANIMATION`.

            emoji_message_interaction (:obj:`raw.types.DataJSON`, *optional*):
                Only supported for :obj:`~pyrogram.enums.ChatAction.TRIGGER_EMOJI_ANIMATION`.

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
        elif "watch_emoji" in action_name:
            if emoji is None:
                raise ValueError(
                    "Invalid Argument Provided"
                )
            action = action.value(emoticon=emoji)
        elif "trigger_emoji" in action_name:
            if (
                emoji is None or
                emoji_message_id is None
            ):
                raise ValueError(
                    "Invalid Argument Provided"
                )
            if emoji_message_interaction is None:
                _, sticker_set = await self._get_raw_stickers(
                    raw.types.InputStickerSetAnimatedEmojiAnimations()
                )
                emoji_message_interaction = raw.types.DataJSON(
                    data=dumps(
                        {
                            "v": 1,
                            "a":[
                                {
                                    "t": 0,
                                    "i": randint(
                                        1,
                                        sticker_set.count
                                    )
                                }
                            ]
                        }
                    )
                )
            action = action.value(
                emoticon=emoji,
                msg_id=emoji_message_id,
                interaction=emoji_message_interaction
            )
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
