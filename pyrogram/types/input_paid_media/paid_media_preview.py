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
from pyrogram import types

from ..object import Object
from .paid_media import PaidMedia


class PaidMediaPreview(PaidMedia):
    """The paid media isn't available before the payment.

    Parameters:
        width (``int``, *optional*):
            Media width as defined by the sender.

        height (``int``, *optional*):
            Media height as defined by the sender.

        duration (``int``, *optional*):
            Duration of the media in seconds as defined by the sender.

        minithumbnail (:obj:`~pyrogram.types.StrippedThumbnail`, *optional*):
            Media minithumbnail; may be None.

    """

    def __init__(
        self,
        *,
        width: int = None,
        height: int = None,
        duration: int = None,
        minithumbnail: "types.StrippedThumbnail" = None
    ):
        super().__init__()

        self.width = width
        self.height = height
        self.duration = duration
        self.minithumbnail = minithumbnail
