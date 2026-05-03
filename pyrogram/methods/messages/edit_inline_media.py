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

import asyncio
import io
import os
import re

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.errors import RPCError, MediaEmpty
from pyrogram.file_id import FileType

from .inline_session import get_session


class EditInlineMedia:
    MAX_RETRIES = 3

    async def edit_inline_media(
        self: "pyrogram.Client",
        inline_message_id: str,
        media: "types.InputMedia",
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> bool:
        """Edit inline animation, audio, document, photo or video messages, or to add media to text messages.

        When an inline message is edited, a new file can't be uploaded; use a previously uploaded file via its file_id or specify a URL.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            inline_message_id (``str``):
                Required if *chat_id* and *message_id* are not specified.
                Identifier of the inline message.

            media (:obj:`~pyrogram.types.InputMedia`):
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio

                # Bots only

                # Replace the current media with a local photo
                await app.edit_inline_media(inline_message_id, InputMediaPhoto("new_photo.jpg"))

                # Replace the current media with a local video
                await app.edit_inline_media(inline_message_id, InputMediaVideo("new_video.mp4"))

                # Replace the current media with a local audio
                await app.edit_inline_media(inline_message_id, InputMediaAudio("new_audio.mp3"))
        """
        caption = media.caption
        parse_mode = media.parse_mode
        caption_entities = media.caption_entities

        message, entities = None, None

        if caption is not None:
            message, entities = (await utils.parse_text_entities(self, caption, parse_mode, caption_entities)).values()

        if not isinstance(
            media,
            (
                types.InputMediaPhoto,
                types.InputMediaVideo,
                types.InputMediaAudio,
                types.InputMediaAnimation,
                types.InputMediaDocument,
            ),
        ):
            raise ValueError(f"Unsupported media type {type(media)}")

        raw_media, _show_caption_above_media = await media.write(client=self)

        unpacked = utils.unpack_inline_message_id(inline_message_id)
        dc_id = unpacked.dc_id
        session = await get_session(self, dc_id)

        for i in range(self.MAX_RETRIES):
            try:
                return await session.invoke(
                    raw.functions.messages.EditInlineBotMessage(
                        id=unpacked,
                        media=raw_media,
                        invert_media=_show_caption_above_media,
                        reply_markup=await reply_markup.write(self) if reply_markup else None,
                        message=message,
                        entities=entities,
                    ),
                    sleep_threshold=self.sleep_threshold
                )
            except RPCError as e:
                if i == self.MAX_RETRIES - 1:
                    raise

                if isinstance(e, MediaEmpty):
                    # Must wait due to a server race condition
                    await asyncio.sleep(1)
