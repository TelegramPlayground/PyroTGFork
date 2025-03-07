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

from datetime import datetime
from typing import Optional

import pyrogram
from pyrogram import raw, utils
from pyrogram import types
from pyrogram.file_id import FileId, FileType, FileUniqueId, FileUniqueType, ThumbnailSource
from ..object import Object


class Video(Object):
    """A video file.

    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.

        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different accounts.
            Can't be used to download or reuse the file.

        width (``int``):
            Video width as defined by sender.

        height (``int``):
            Video height as defined by sender.

        duration (``int``):
            Duration of the video in seconds as defined by sender.

        file_name (``str``, *optional*):
            Video file name.

        mime_type (``str``, *optional*):
            Mime type of a file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        supports_streaming (``bool``, *optional*):
            True, if the video was uploaded with streaming support.

        ttl_seconds (``int``. *optional*):
            Time-to-live seconds, for secret photos.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the video was sent.

        thumbs (List of :obj:`~pyrogram.types.Thumbnail`, *optional*):
            Video thumbnails.

        cover (:obj:`~pyrogram.types.Photo`, *optional*):
            Cover of the video available in the message.

        start_timestamp (``int``. *optional*):
            Timestamp from which the video playing must start, in seconds.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        file_id: str,
        file_unique_id: str,
        width: int,
        height: int,
        duration: int,
        file_name: str = None,
        mime_type: str = None,
        file_size: int = None,
        supports_streaming: bool = None,
        ttl_seconds: int = None,
        date: datetime = None,
        thumbs: list["types.Thumbnail"] = None,
        cover: Optional["types.Photo"] = None,
        start_timestamp: Optional[int] = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.duration = duration
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.supports_streaming = supports_streaming
        self.ttl_seconds = ttl_seconds
        self.date = date
        self.thumbs = thumbs
        self.cover = cover
        self.start_timestamp = start_timestamp

    @staticmethod
    def _parse(
        client,
        media: "raw.types.MessageMediaDocument",
        video_attributes: "raw.types.DocumentAttributeVideo",
        file_name: str,
        ttl_seconds: int = None,
        video: "raw.types.Document" = None
    ) -> "Video":
        if not video:
            video = media.document  # "raw.types.Document"
        return Video(
            file_id=FileId(
                file_type=FileType.VIDEO,
                dc_id=video.dc_id,
                media_id=video.id,
                access_hash=video.access_hash,
                file_reference=video.file_reference
            ).encode() if video else None,
            file_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=video.id
            ).encode() if video else None,
            width=video_attributes.w if video_attributes else None,
            height=video_attributes.h if video_attributes else None,
            duration=video_attributes.duration if video_attributes else None,
            file_name=file_name,
            mime_type=video.mime_type if video else None,
            supports_streaming=video_attributes.supports_streaming if video_attributes else None,
            file_size=video.size if video else None,
            date=utils.timestamp_to_datetime(video.date) if video else None,
            ttl_seconds=ttl_seconds,
            thumbs=types.Thumbnail._parse(client, video) if video else None,
            cover=types.Photo._parse(
                client,
                media.video_cover
            ) if media and media.video_cover else None,
            start_timestamp=media.video_timestamp if media else None,
            client=client
        )
