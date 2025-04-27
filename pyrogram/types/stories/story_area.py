#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present <https://github.com/TelegramPlayGround>
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


class StoryArea(Object):
    """This object describes a clickable area on a story media..

    Parameters:
        position (:obj:`~pyrogram.types.StoryAreaPosition`):
            Position of the area.
        
        type (:obj:`~pyrogram.types.StoryAreaType`):
            Type of the area.

    """

    def __init__(
        self,
        client: "pyrogram.Client" = None,
        position: "types.StoryAreaPosition" = None,
        type: "types.StoryAreaType" = None,
    ):
        super().__init__(client)

        self.position = position
        self.type = type
