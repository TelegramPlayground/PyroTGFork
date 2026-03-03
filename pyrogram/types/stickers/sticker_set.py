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

import pyrogram
from pyrogram import raw, types, utils
from ..object import Object


class StickerSet(Object):
    """A sticker set.

    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.

        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different accounts.
            Can't be used to download or reuse the file.


        width (``int``):
            Sticker width.

        height (``int``):
            Sticker height.

        is_animated (``bool``):
            True, if the sticker is animated

        is_video (``bool``):
            True, if the sticker is a video sticker

        thumbs (List of :obj:`~pyrogram.types.Thumbnail`, *optional*):
            Sticker thumbnails in the .webp or .jpg format.

        emoji (``str``, *optional*):
            Emoji associated with the sticker.
        
        set_name (``str``, *optional*):
            Name of the sticker set to which the sticker belongs.


        file_size (``int``, *optional*):
            File size in bytes.

        file_name (``str``, *optional*):
            Sticker file name.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the sticker was sent.

        emoji (``str``, *optional*):
            Emoji corresponding to the sticker; may be empty if unknown.

        set_name (``str``, *optional*):
            Name of the sticker set to which the sticker belongs.

        thumbs (List of :obj:`~pyrogram.types.Thumbnail`, *optional*):
            Sticker thumbnails in the .webp or .jpg format.

    """

stickerSet#2dd14edc flags:#
emojis:flags.7?true
masks:flags.3?true

archived:flags.1?true
official:flags.2?true


text_color:flags.9?true
channel_emoji_status:flags.10?true
creator:flags.11?true
installed_date:flags.0?int
id:long
access_hash:long
title:string
short_name:string
thumbs:flags.4?Vector<PhotoSize>
thumb_dc_id:flags.4?int
thumb_version:flags.4?int
thumb_document_id:flags.8?long
count:int
hash:int = StickerSet;


    # TODO: Add mask position

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        file_id: str,
        file_unique_id: str,
        width: int,
        height: int,
        is_animated: bool,
        is_video: bool,
        file_name: str = None,
        mime_type: str = None,
        file_size: int = None,
        date: datetime = None,
        emoji: str = None,
        set_name: str = None,
        thumbs: list["types.Thumbnail"] = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.width = width
        self.height = height
        self.is_animated = is_animated
        self.is_video = is_video
        self.emoji = emoji
        self.set_name = set_name
        self.thumbs = thumbs
        # self.mask_position = mask_position
