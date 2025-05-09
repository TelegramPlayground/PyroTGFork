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
from pyrogram import types, raw

from .story_area_type import StoryAreaType


class StoryAreaTypeLocation(StoryAreaType):
    """This object describes a story area pointing to a location. Currently, a story can have up to 10 location areas.

    Parameters:
        latitude (``float``):
            Location latitude in degrees.

        longitude (``float``):
            Location longitude in degrees.

        horizontal_accuracy (``float``, *optional*):
            The radius of uncertainty for the location, measured in meters; 0-1500.

        address (:obj:`~pyrogram.types.LocationAddress`, *optional*):
            Address of the location.

    """

    def __init__(
        self,
        latitude: float = None,
        longitude: float = None,
        horizontal_accuracy: float = 0,
        address: Optional["types.LocationAddress"] = None,
    ):
        super().__init__()

        self.latitude = latitude
        self.longitude = longitude
        self.horizontal_accuracy = horizontal_accuracy
        self.address = address

    async def write(
        self,
        client: "pyrogram.Client",
        coordinates: "raw.types.MediaAreaCoordinates"
    ):
        return raw.types.MediaAreaGeoPoint(
            coordinates=coordinates,
            geo=raw.types.GeoPoint(
                long=self.longitude,
                lat=self.latitude,
                access_hash=0,
                accuracy_radius=self.horizontal_accuracy
            ),
            address=raw.types.GeoPointAddress(
                country_iso2=self.address.country_code,
                state=self.address.state,
                city=self.address.city,
                street=self.address.street
            ) if self.address else None
        )
