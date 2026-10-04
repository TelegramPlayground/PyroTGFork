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
import pathlib
import re
from typing import Callable, Optional, Union

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.file_id import FileType

from .input_media import InputMedia


class InputMediaLivePhoto(InputMedia):
    """Represents a live photo to be sent.

    Parameters:
        media (``str`` | :obj:`io.BytesIO`):
            Video of the live photo to send.
            Pass a file_id as string to send a video that exists on the Telegram servers or
            pass a file path as string to upload a new video that exists on your local machine or
            pass a binary file-like object with its attribute “.name” set for in-memory uploads
            Sending live photos by a URL is currently unsupported.

        photo (``str`` | :obj:`io.BytesIO`):
            The static photo to send.
            Pass a file_id as string to send a video that exists on the Telegram servers or
            pass a file path as string to upload a new video that exists on your local machine or
            pass a binary file-like object with its attribute “.name” set for in-memory uploads
            Sending live photos by a URL is currently unsupported.

        caption (``str``, *optional*):
            Caption of the video to be sent, 0-1024 characters.
            If not specified, the original caption is kept. Pass "" (empty string) to remove the caption.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        show_caption_above_media (``bool``, *optional*):
            Pass True, if the caption must be shown above the message media.

        has_spoiler (``bool``, *optional*):
            Pass True if the photo needs to be covered with a spoiler animation.
    """

    def __init__(
        self,
        media: Union[str, "io.BytesIO"],
        photo: Union[str, "io.BytesIO"],
        thumb: Optional[str] = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: Optional[list["types.MessageEntity"]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,

    ):
        super().__init__(media, caption, parse_mode, caption_entities)

        self.photo = photo
        self.thumb = thumb
        self.show_caption_above_media = show_caption_above_media
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
            "InputMediaPhoto",
            "InputMediaPhotoExternal",
        ],
        bool
    ]:
        duration: int = 0
        width: int = 0
        height: int = 0

        peer = await client.resolve_peer(chat_id or "me")

        is_bytes_io = isinstance(self.media, io.BytesIO)
        is_uploaded_file = is_bytes_io or pathlib.Path(self.media).is_file()
        # is_external_url = not is_uploaded_file and re.match("^https?://", self.media)
        is_bytes_io_sp = isinstance(self.photo, io.BytesIO)
        is_uploaded_file_sp = is_bytes_io_sp or pathlib.Path(self.photo).is_file()

        if is_bytes_io and not hasattr(self.media, "name"):
            self.media.name = "media"
        
        if is_bytes_io_sp and not hasattr(self.photo, "name"):
            self.photo.name = "media"

        # 1. Resolve uploaded_media
        if is_uploaded_file:
            uploaded_media = await client.invoke(
                raw.functions.messages.UploadMedia(
                    peer=peer,
                    media=raw.types.InputMediaUploadedDocument(
                        mime_type=client.guess_mime_type(self.media) or "video/mp4",
                        file=await client.save_file(
                            self.media, progress=progress, progress_args=progress_args
                        ),
                        spoiler=self.has_spoiler,
                        attributes=[
                            raw.types.DocumentAttributeVideo(
                                duration=duration,
                                w=width,
                                h=height,
                            ),
                        ],
                    ),
                ),
            )
        else:
            uploaded_media = utils.get_input_media_from_file_id(
                self.media,
                FileType.VIDEO,
                has_spoiler=self.has_spoiler,
            )

        # 2. Resolve uploaded_photo
        if is_uploaded_file_sp:
            uploaded_photo = await client.invoke(
                raw.functions.messages.UploadMedia(
                    peer=peer,
                    media=raw.types.InputMediaUploadedPhoto(
                        video=await client.save_file(
                            self.photo, progress=progress, progress_args=progress_args
                        ),
                        file=await client.save_file(
                            self.photo, progress=progress, progress_args=progress_args
                        ),
                        live_photo=True,
                        spoiler=self.has_spoiler,
                    ),
                )
            )
        else:
            uploaded_photo = utils.get_input_media_from_file_id(
                self.photo,
                FileType.PHOTO,
                has_spoiler=self.has_spoiler,
            )

        media = raw.types.InputMediaPhoto(
            id=raw.types.InputPhoto(
                id=uploaded_photo.photo.id,
                access_hash=uploaded_photo.photo.access_hash,
                file_reference=uploaded_photo.photo.file_reference,
            ),
            live_photo=True,
            spoiler=self.has_spoiler,
            video=raw.types.InputDocument(
                id=uploaded_media.document.id,
                access_hash=uploaded_media.document.access_hash,
                file_reference=uploaded_media.document.file_reference,
            )
        )
        
        return media, self.show_caption_above_media
