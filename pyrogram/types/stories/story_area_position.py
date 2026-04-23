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

from typing import Optional

import pyrogram
from pyrogram import raw

from ..object import Object


class StoryAreaPosition(Object):
    """This object describes the position of a clickable area within a story.

    Parameters:
        x_percentage (``float``):
            The abscissa of the area's center, as a percentage of the media width.

        y_percentage (``float``):
            The ordinate of the area's center, as a percentage of the media height.

        width_percentage (``float``):
            The width of the area's rectangle, as a percentage of the media width.
        
        height_percentage (``float``):
            The height of the area's rectangle, as a percentage of the media height.
        
        rotation_angle (``float``):
            The clockwise rotation angle of the rectangle, in degrees; 0-360.
        
        corner_radius_percentage (``float``, *optional*):
            The radius of the rectangle corner rounding, as a percentage of the media width.

    """

    def __init__(
        self,
        x_percentage: float = None,
        y_percentage: float = None,
        width_percentage: float = None,
        height_percentage: float = None,
        rotation_angle: float = None,
        corner_radius_percentage: Optional[float] = None,
    ):
        super().__init__()

        self.x_percentage = x_percentage
        self.y_percentage = y_percentage
        self.width_percentage = width_percentage
        self.height_percentage = height_percentage
        self.rotation_angle = rotation_angle
        self.corner_radius_percentage = corner_radius_percentage

    @staticmethod
    def _parse(coordinates: "raw.types.MediaAreaCoordinates") -> "StoryAreaPosition":
        return StoryAreaPosition(
            x_percentage=coordinates.x,
            y_percentage=coordinates.y,
            width_percentage=coordinates.w,
            height_percentage=coordinates.h,
            rotation_angle=coordinates.rotation,
            corner_radius_percentage=coordinates.radius
        )

    def write(self):
        return raw.types.MediaAreaCoordinates(
            x=self.x_percentage,
            y=self.y_percentage,
            w=self.width_percentage,
            h=self.height_percentage,
            rotation=self.rotation_angle,
            radius=self.corner_radius_percentage
        )
