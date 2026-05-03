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


from typing import Optional, Union

import pyrogram
from pyrogram import raw

from ..object import Object


class Location(Object):
    """A point on the map.

    Parameters:
        longitude (``float``):
            Longitude as defined by sender.

        latitude (``float``):
            Latitude as defined by sender.

        accuracy_radius (``int``, *optional*):
            The estimated horizontal accuracy of the location, in meters as defined by the sender.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        longitude: float,
        latitude: float,
        accuracy_radius: Optional[int] = None,
    ):
        super().__init__(client)

        self.longitude = longitude
        self.latitude = latitude
        self.accuracy_radius = accuracy_radius

    @staticmethod
    def _parse(client, geo_point: "raw.base.GeoPoint") -> "Location":
        if isinstance(geo_point, raw.types.GeoPoint):
            return Location(
                longitude=geo_point.long,
                latitude=geo_point.lat,
                accuracy_radius=geo_point.accuracy_radius,
                client=client
            )

    async def write(self) -> "raw.types.InputMediaGeoPoint":
        return raw.types.InputMediaGeoPoint(
            geo_point=raw.types.InputGeoPoint(
                lat=self.latitude,
                long=self.longitude,
                accuracy_radius=self.accuracy_radius,
            ),
        )


class ChatLocation(Object):
    """Represents a location to which a chat is connected.
    
    Parameters:
        location (:obj:`~pyrogram.types.Location`):
            The location to which the supergroup is connected. Can't be a live location.
        
        address (``string``):
            Location address; 1-64 characters, as defined by the chat owner.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        location: "Location",
        address: str
    ):
        super().__init__(client)

        self.location = location
        self.address = address
