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

import logging
from datetime import datetime
from typing import Union

import pyrogram
from pyrogram import enums, raw, types, utils

log = logging.getLogger(__name__)


class CopyMediaGroup:
    async def copy_media_group(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        captions: Union[list[str], str] = None,
        disable_notification: bool = None,
        reply_parameters: "types.ReplyParameters" = None,
        message_thread_id: int = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        paid_message_star_count: int = None,
        message_effect_id: int = None,
        reply_to_message_id: int = None
    ) -> list["types.Message"]:
        """Copy a media group by providing one of the message ids.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            from_chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the source chat where the original media group was sent.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Message identifier in the chat specified in *from_chat_id*.

            captions (``str`` | List of ``str`` , *optional*):
                New caption for media, 0-1024 characters after entities parsing for each media.
                If not specified, the original caption is kept.
                Pass "" (empty string) to remove the caption.

                If a ``string`` is passed, it becomes a caption only for the first media.
                If a list of ``string`` passed, each element becomes caption for each media element.
                You can pass ``None`` in list to keep the original caption (see examples below).

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            message_thread_id (``int``, *optional*):
                If the message is in a thread, ID of the original message.
            
            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            paid_message_star_count (``int``, *optional*):
                The number of Telegram Stars the user agreed to pay to send the messages.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

        Returns:
            List of :obj:`~pyrogram.types.Message`: On success, a list of copied messages is returned.

        Example:
            .. code-block:: python

                # Copy a media group
                await app.copy_media_group(to_chat, from_chat, 123)

                await app.copy_media_group(to_chat, from_chat, 123, captions="single caption")
                
                await app.copy_media_group(to_chat, from_chat, 123,
                    captions=["caption 1", None, ""])
        """

        if reply_to_message_id and reply_parameters:
            raise ValueError(
                "Parameters `reply_to_message_id` and `reply_parameters` are mutually "
                "exclusive."
            )
        
        if reply_to_message_id is not None:
            log.warning(
                "This property is deprecated. "
                "Please use reply_parameters instead"
            )
            reply_parameters = types.ReplyParameters(message_id=reply_to_message_id)

        media_group = await self.get_media_group(from_chat_id, message_id)
        multi_media = []
        show_caption_above_media = []

        for i, message in enumerate(media_group):
            if message.photo:
                file_id = message.photo.file_id
            elif message.audio:
                file_id = message.audio.file_id
            elif message.document:
                file_id = message.document.file_id
            elif message.video:
                file_id = message.video.file_id
            else:
                raise ValueError("Message with this type can't be copied.")

            media = utils.get_input_media_from_file_id(file_id=file_id)

            sent_message, sent_entities = None, None
            if isinstance(captions, list) and i < len(captions) and isinstance(captions[i], str):
                sent_message, sent_entities = (await utils.parse_text_entities(self, captions[i], self.parse_mode, None)).values()
            elif isinstance(captions, str) and i == 0:
                sent_message, sent_entities = (await utils.parse_text_entities(self, captions, self.parse_mode, None)).values()
            elif message.caption and message.caption != "None" and not type(captions) is str:  # TODO
                sent_message, sent_entities = (await utils.parse_text_entities(self, message.caption, None, message.caption_entities)).values()
            else:
                sent_message, sent_entities = "", None

            multi_media.append(
                raw.types.InputSingleMedia(
                    media=media,
                    random_id=self.rnd_id(),
                    message=sent_message,
                    entities=sent_entities
                )
            )
            show_caption_above_media.append(message.show_caption_above_media)

        reply_to = await utils._get_reply_message_parameters(
            self,
            message_thread_id,
            reply_parameters
        )

        r = await self.invoke(
            raw.functions.messages.SendMultiMedia(
                peer=await self.resolve_peer(chat_id),
                multi_media=multi_media,
                silent=disable_notification or None,
                reply_to=reply_to,
                send_as=await self.resolve_peer(send_as) if send_as else None,
                schedule_date=utils.datetime_to_timestamp(schedule_date),
                noforwards=protect_content,
                allow_paid_floodskip=allow_paid_broadcast,
                allow_paid_stars=paid_message_star_count,
                effect=message_effect_id,
                invert_media=any(show_caption_above_media)
            ),
            sleep_threshold=60
        )

        return await utils.parse_messages(
            client=self,
            messages=None,
            r=r
        )
