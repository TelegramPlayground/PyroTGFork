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
from typing import Union, List, Optional

import pyrogram
from pyrogram import raw, enums, types, utils

log = logging.getLogger(__name__)


class EditCachedMedia:
    async def edit_cached_media(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        file_id: str,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        schedule_date: datetime = None,
        has_spoiler: bool = None,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> Optional["types.Message"]:
        """Edit a media stored on the Telegram servers using a file_id.

        This convenience method works with any valid file_id only.
        It does the same as calling the relevant method for editing media using a file_id, thus saving you from the
        hassle of using the correct :obj:`~pyrogram.types.InputMedia` for the media the file_id is pointing to.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Message identifier in the chat specified in chat_id.

            file_id (``str``):
                Media to send.
                Pass a file_id as string to send a media that exists on the Telegram servers.

            caption (``str``, *optional*):
                Media caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            has_spoiler (``bool``, *optional*):
                True, if the message media is covered by a spoiler animation.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the edited media message is returned.

        Example:
            .. code-block:: python

                await app.edit_cached_media(chat_id, message_id, file_id)
        """

        rpc = raw.functions.messages.EditMessage(
            peer=await self.resolve_peer(chat_id),
            id=message_id,
            media=utils.get_input_media_from_file_id(file_id, has_spoiler=has_spoiler),
            reply_markup=await reply_markup.write(self) if reply_markup else None,
            schedule_date=utils.datetime_to_timestamp(schedule_date),
            **await utils.parse_text_entities(self, caption, parse_mode, caption_entities)
        )
        r = await self.invoke(rpc)

        for i in r.updates:
            if isinstance(
                i,
                (
                    raw.types.UpdateEditMessage,
                    raw.types.UpdateEditChannelMessage,
                    raw.types.UpdateNewScheduledMessage
                )
            ):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage),
                    replies=0
                )
