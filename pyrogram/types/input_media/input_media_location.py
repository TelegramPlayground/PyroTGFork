#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present <https://github.com/KurimuzonAkuma>
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

from typing import Callable, Optional, Union

from pyrogram import raw

from .input_media import InputMedia


class InputMediaLocation(InputMedia):
    """Represents a location to be sent.

    Parameters:
        latitude (``float``):
            Latitude of the location.

        longitude (``float``):
            Longitude of the location.

        accuracy_radius (``int``, *optional*):
            The estimated horizontal accuracy of the location, in meters as defined by the sender.

        address (``str``, *optional*):
            Textual description of the address (mandatory).

        live_period (``int``, *optional*):
            For live locations, the time relative to the message send date, for which the location can be updated, in seconds.

        heading (``int``, *optional*):
            For live locations, a direction in which the location moves, in degrees; 1-360.

        proximity_alert_radius (``int``, *optional*):
            For live locations, a maximum distance to another chat member for proximity alerts, in meters (0-100000).

    """

    def __init__(
        self,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        accuracy_radius: Optional[int] = None,
        address: Optional[str] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
    ):
        super().__init__()

        self.longitude = longitude
        self.latitude = latitude
        self.accuracy_radius = accuracy_radius
        self.address = address
        self.live_period = live_period
        self.heading = heading
        self.proximity_alert_radius = proximity_alert_radius

    async def write(
        self,
        client: "pyrogram.Client",
        chat_id: Optional[Union[int, str]] = None,
        business_connection_id: Optional[str] = None,
        progress: Optional[Callable] = None,
        progress_args: tuple = (),
    ) -> tuple[
        Union[
            "raw.types.InputMediaGeoPoint",
            "raw.types.InputMediaGeoLive"
        ],
        bool
    ]:
        media = None
        if self.live_period is not None:
            media = raw.types.InputMediaGeoLive(
                geo_point=raw.types.InputGeoPoint(
                    lat=self.latitude or 0,
                    long=self.longitude or 0,
                    accuracy_radius=self.accuracy_radius,
                ),
                heading=self.heading,
                period=self.live_period,
                proximity_notification_radius=self.proximity_alert_radius,
            )
        else:
            media = raw.types.InputMediaGeoPoint(
                geo_point=raw.types.InputGeoPoint(
                    lat=self.latitude or 0,
                    long=self.longitude or 0,
                    accuracy_radius=self.accuracy_radius,
                ),
            )
        return media, False
