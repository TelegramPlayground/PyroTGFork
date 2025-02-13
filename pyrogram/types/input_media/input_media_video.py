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
from typing import Optional, Union

from .input_media import InputMedia
from ..messages_and_media import MessageEntity
from ... import enums


class InputMediaVideo(InputMedia):
    """A video to be sent inside an album.
    It is intended to be used with :obj:`~pyrogram.Client.send_media_group`.

    Parameters:
        media (``str`` | :obj:`io.BytesIO`):
            Video to send.
            Pass a file_id as string to send a video that exists on the Telegram servers or
            pass a file path as string to upload a new video that exists on your local machine or
            pass a binary file-like object with its attribute “.name” set for in-memory uploads or
            pass an HTTP URL as a string for Telegram to get a video from the Internet.

        thumb (``str`` | :obj:`io.BytesIO`):
            Thumbnail of the video sent.
            The thumbnail should be in JPEG format and less than 200 KB in size.
            A thumbnail's width and height should not exceed 320 pixels.
            Thumbnails can't be reused and can be only uploaded as a new file.

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

        width (``int``, *optional*):
            Video width.

        height (``int``, *optional*):
            Video height.

        duration (``int``, *optional*):
            Video duration.

        file_name (``str``, *optional*):
            File name of the video sent.
            Defaults to file's path basename.

        supports_streaming (``bool``, *optional*):
            Pass True, if the uploaded video is suitable for streaming.

        has_spoiler (``bool``, *optional*):
            Pass True if the photo needs to be covered with a spoiler animation.

        disable_content_type_detection (``bool``, *optional*):
            Pass True, if the uploaded video is a video message with no sound.
            Disables automatic server-side content type detection for files uploaded using multipart/form-data. Always True, if the document is sent as part of an album.
        
        cover (``str`` | :obj:`io.BytesIO`, *optional*):
            Cover for the video in the message. pass None to skip cover uploading.
        
        start_timestamp (``int``, *optional*):
            Timestamp from which the video playing must start, in seconds.

    """

    def __init__(
        self,
        media: Union[str, "io.BytesIO"],
        thumb: Union[str, "io.BytesIO"] = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list[MessageEntity] = None,
        show_caption_above_media: bool = None,
        width: int = 0,
        height: int = 0,
        duration: int = 0,
        file_name: str = None,
        supports_streaming: bool = True,
        has_spoiler: bool = None,
        disable_content_type_detection: bool = None,
        cover: Optional[Union[str, "io.BytesIO"]] = None,
        start_timestamp: int = None
    ):
        super().__init__(media, caption, parse_mode, caption_entities)

        self.thumb = thumb
        self.show_caption_above_media = show_caption_above_media
        self.width = width
        self.height = height
        self.duration = duration
        self.file_name = file_name
        self.supports_streaming = supports_streaming
        self.has_spoiler = has_spoiler
        self.disable_content_type_detection = disable_content_type_detection
        self.cover = cover
        self.start_timestamp = start_timestamp
