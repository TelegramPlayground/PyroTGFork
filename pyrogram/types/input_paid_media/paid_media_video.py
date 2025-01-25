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

from typing import Optional

import pyrogram
from pyrogram import types

from ..object import Object
from .paid_media import PaidMedia


class PaidMediaVideo(PaidMedia):
    """The paid media is a video.

    Parameters:
        video (:obj:`~pyrogram.types.Video`):
            The video.

        cover (:obj:`~pyrogram.types.Photo`, *optional*):
            Cover of the video.
        
        start_timestamp (``int``, *optional*):
            Timestamp from which the video playing must start, in seconds.

    """

    def __init__(
        self,
        *,
        video: "types.Video" = None,
        cover: Optional["types.Photo"] = None,
        start_timestamp: Optional[int] = None
    ):
        super().__init__()

        self.video = video
        self.cover = cover
        self.start_timestamp = start_timestamp
