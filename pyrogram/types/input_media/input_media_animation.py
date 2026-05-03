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

import io
import os
import re
from typing import Callable, Optional, Union

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.file_id import FileType

from .input_media import InputMedia


class InputMediaAnimation(InputMedia):
    """An animation file (GIF or H.264/MPEG-4 AVC video without sound) to be sent inside an album.

    Parameters:
        media (``str`` | :obj:`io.BytesIO`):
            Animation to send.
            Pass a file_id as string to send a file that exists on the Telegram servers or
            pass a file path as string to upload a new file that exists on your local machine or
            pass a binary file-like object with its attribute “.name” set for in-memory uploads or
            pass an HTTP URL as a string for Telegram to get an animation from the Internet.

        thumb (``str`` | :obj:`io.BytesIO`, *optional*):
            Thumbnail of the animation file sent.
            The thumbnail should be in JPEG format and less than 200 KB in size.
            A thumbnail's width and height should not exceed 320 pixels.
            Thumbnails can't be reused and can be only uploaded as a new file.

        caption (``str``, *optional*):
            Caption of the animation to be sent, 0-1024 characters.
            If not specified, the original caption is kept. Pass "" (empty string) to remove the caption.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        show_caption_above_media (``bool``, *optional*):
            Pass True, if the caption must be shown above the message media.

        width (``int``, *optional*):
            Animation width.

        height (``int``, *optional*):
            Animation height.

        duration (``int``, *optional*):
            Animation duration.

        has_spoiler (``bool``, *optional*):
            Pass True if the photo needs to be covered with a spoiler animation.
    """

    def __init__(
        self,
        media: Union[str, "io.BytesIO"],
        thumb: Union[str, "io.BytesIO"] = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        show_caption_above_media: bool = None,
        width: int = 0,
        height: int = 0,
        duration: int = 0,
        has_spoiler: bool = None
    ):
        super().__init__(media, caption, parse_mode, caption_entities)

        self.thumb = thumb
        self.show_caption_above_media = show_caption_above_media
        self.width = width
        self.height = height
        self.duration = duration
        self.has_spoiler = has_spoiler

    async def write(
        self,
        client: "pyrogram.Client",
        chat_id: Optional[Union[int, str]] = None,
        business_connection_id: Optional[str] = None,
        progress: Optional[Callable] = None,
        progress_args: tuple = (),
    ) -> tuple[
        Union[
            "InputMediaDocument",
            "InputMediaDocumentExternal",
        ],
        bool
    ]:
        is_bytes_io = isinstance(self.media, io.BytesIO)
        is_uploaded_file = is_bytes_io or os.path.isfile(self.media)
        is_external_url = not is_uploaded_file and re.match("^https?://", self.media)

        if is_bytes_io and not hasattr(self.media, "name"):
            self.media.name = self.file_name or "media"

        if is_uploaded_file:
            filename_attribute = [
                raw.types.DocumentAttributeFilename(
                    file_name=None or (self.media.name if is_bytes_io else os.path.basename(self.media))
                )
            ]
        else:
            filename_attribute = []

        if is_uploaded_file:
            uploaded_media = await client.invoke(
                raw.functions.messages.UploadMedia(
                    business_connection_id=None,  # TODO
                    peer=await client.resolve_peer(chat_id),
                    media=raw.types.InputMediaUploadedDocument(
                        mime_type=(None if is_bytes_io else self.guess_mime_type(self.media)) or "video/mp4",
                        thumb=await client.save_file(self.thumb),
                        spoiler=media.has_spoiler,
                        file=await client.save_file(self.media),
                        attributes=[
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=True,
                                duration=self.duration,
                                w=self.width,
                                h=self.height
                            ),
                            raw.types.DocumentAttributeAnimated(),
                        ] + filename_attribute,
                    )
                )
            )

            media = raw.types.InputMediaDocument(
                id=raw.types.InputDocument(
                    id=uploaded_media.document.id,
                    access_hash=uploaded_media.document.access_hash,
                    file_reference=uploaded_media.document.file_reference
                ),
                spoiler=self.has_spoiler
            )
        elif is_external_url:
            media = raw.types.InputMediaDocumentExternal(
                url=self.media,
                spoiler=self.has_spoiler
            )
        else:
            media = utils.get_input_media_from_file_id(self.media, FileType.ANIMATION, has_spoiler=self.has_spoiler)

        return media, self.show_caption_above_media
