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
from pyrogram import types, raw

from ..object import Object


class StoryArea(Object):
    """This object describes a clickable area on a story media.

    Parameters:
        position (:obj:`~pyrogram.types.StoryAreaPosition`):
            Position of the area.
        
        type (:obj:`~pyrogram.types.StoryAreaType`):
            Type of the area.

    """

    def __init__(
        self,
        position: "types.StoryAreaPosition" = None,
        type: "types.StoryAreaType" = None,
    ):
        super().__init__()

        self.position = position
        self.type = type

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        area: "raw.base.MediaArea",
    ) -> "StoryArea":
        story_area_type = None
        # if isinstance(area, raw.types.)
        # mediaAreaVenue#be82db9c coordinates:MediaAreaCoordinates geo:GeoPoint title:string address:string provider:string venue_id:string venue_type:string = MediaArea;
        # mediaAreaGeoPoint#cad5452d flags:# coordinates:MediaAreaCoordinates geo:GeoPoint address:flags.0?GeoPointAddress = MediaArea;
        # mediaAreaSuggestedReaction#14455871 flags:# dark:flags.0?true flipped:flags.1?true coordinates:MediaAreaCoordinates reaction:Reaction = MediaArea;
        # mediaAreaChannelPost#770416af coordinates:MediaAreaCoordinates channel_id:long msg_id:int = MediaArea;
        # mediaAreaUrl#37381085 coordinates:MediaAreaCoordinates url:string = MediaArea;
        # mediaAreaWeather#49a6549c coordinates:MediaAreaCoordinates emoji:string temperature_c:double color:int = MediaArea;
        # mediaAreaStarGift#5787686d coordinates:MediaAreaCoordinates slug:string = MediaArea;
        return StoryArea(
            position=types.StoryAreaPosition._parse(area.coordinates),
            type=story_area_type,
        )

    def write(self, client: "pyrogram.Client"):
        coordinates = self.position.write()
        return self.type.write(client, coordinates)
