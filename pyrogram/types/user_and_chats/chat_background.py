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
from typing import Union

import pyrogram
from pyrogram import raw, utils
from pyrogram import types
from pyrogram.file_id import (
    FileId,
    FileType,
    FileUniqueId,
    FileUniqueType,
    ThumbnailSource,
)
from ..object import Object


class ChatBackground(Object):
    """Describes a background set for a specific chat.

    Parameters:
        file_id (``str``, *optional*):
            Identifier for this file, which can be used to download the file.

        file_unique_id (``str``, *optional*):
            Unique identifier for this file, which is supposed to be the same over time and for different accounts.
            Can't be used to download or reuse the file.

        file_size (``int``, *optional*):
            File size.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the background was setted.

        slug (``str``, *optional*):
            Identifier of the background code.

        thumbs (List of :obj:`~pyrogram.types.Thumbnail`, *optional*):
            Available thumbnails of this background.

        link (``str``, *property*):
            Generate a link to this background code.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        file_id: str = None,
        file_unique_id: str = None,
        file_size: int = None,
        date: datetime = None,
        slug: str = None,
        thumbs: list["types.Thumbnail"] = None,
        _raw: "raw.base.WallPaper" = None,
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self.date = date
        self.slug = slug
        self.thumbs = thumbs
        self._raw = _raw

    @property
    def link(self) -> str:
        return f"https://t.me/bg/{self.slug}" if self.slug else None

    @staticmethod
    def _parse(
        client,
        wallpaper: "raw.base.WallPaper",
    ) -> "ChatBackground":
        if isinstance(wallpaper, raw.types.WallPaperNoFile):
            return ChatBackground(
                _raw=wallpaper,
                client=client,
            )
        if isinstance(wallpaper, raw.types.WallPaper):
            return ChatBackground(
                file_id=FileId(
                    dc_id=wallpaper.document.dc_id,
                    file_reference=wallpaper.document.file_reference,
                    access_hash=wallpaper.document.access_hash,
                    file_type=FileType.BACKGROUND,
                    media_id=wallpaper.document.id,
                    volume_id=0,
                    local_id=0,
                    thumbnail_source=ThumbnailSource.THUMBNAIL,
                    thumbnail_file_type=FileType.BACKGROUND,
                ).encode(),
                file_unique_id=FileUniqueId(
                    file_unique_type=FileUniqueType.DOCUMENT, media_id=wallpaper.document.id
                ).encode(),
                file_size=wallpaper.document.size,
                slug=wallpaper.slug,
                date=utils.timestamp_to_datetime(wallpaper.document.date),
                thumbs=types.Thumbnail._parse(client, wallpaper.document),
                _raw=wallpaper,
                client=client,
            )
