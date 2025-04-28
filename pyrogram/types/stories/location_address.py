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


from ..object import Object


class LocationAddress(Object):
    """This object describes the physical address of a location.

    Parameters:
        country_code (``float``):
            The two-letter ISO 3166-1 alpha-2 country code of the country where the location is located.

        state (``float``, *optional*):
            State of the location.

        city (``float``, *optional*):
            City of the location.
        
        street (``float``, *optional*):
            Street address of the location.

    """

    def __init__(
        self,
        country_code: float = None,
        state: float = None,
        city: float = None,
        street: float = None,
    ):
        super().__init__()

        self.country_code = country_code
        self.state = state
        self.city = city
        self.street = street
