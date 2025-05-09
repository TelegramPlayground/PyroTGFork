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

from datetime import datetime
from typing import Optional, Union

import pyrogram
from pyrogram import raw, types, utils


class ForwardStory:
    async def forward_story(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        story_poster_chat_id: Union[int, str],
        story_id: int,
        disable_notification: bool = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        paid_message_star_count: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        message_thread_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        schedule_date: datetime = None,
        message_effect_id: int = None,
        send_as: Union[int, str] = None,
    ) -> Optional["types.Message"]:
        """Forward story.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            story_poster_chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            story_id (``int``):
                Unique identifier of story.

            disable_notification (``bool``, *optional*):
                Sends the message with story silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            paid_message_star_count (``int``, *optional*):
                The number of Telegram Stars the user agreed to pay to send the messages.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum.
                For supergroups only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent story message is returned.

        Example:
            .. code-block:: python

                # Send your story to chat_id
                await app.forward_story(to_chat, from_chat, 123)
        """
        reply_to = await utils._get_reply_message_parameters(
            self,
            message_thread_id,
            reply_parameters
        )
        r = await self.invoke(
            raw.functions.messages.SendMedia(
                allow_paid_floodskip=allow_paid_broadcast,
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                noforwards=protect_content,
                send_as=send_as,
                effect=message_effect_id,
                peer=await self.resolve_peer(chat_id),
                media=raw.types.InputMediaStory(
                    peer=await self.resolve_peer(story_poster_chat_id),
                    id=story_id
                ),
                silent=disable_notification or None,
                random_id=self.rnd_id(),
                schedule_date=utils.datetime_to_timestamp(schedule_date),
                reply_to=reply_to,
                allow_paid_stars=paid_message_star_count,
                message=""
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
                    replies=self.fetch_replies
                )
