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
from pyrogram import types, raw
from ..object import Object


class Birthdate(Object):
    """

    Parameters:
        day (``int``):
            Day of the user's birth; 1-31

        month (``int``):
            Month of the user's birth; 1-12

        year (``int``, *optional*):
            Year of the user's birth

    """

    def __init__(
        self,
        *,
        day: int,
        month: int,
        year: int = None
    ):
        super().__init__()

        self.day = day
        self.month = month
        self.year = year

    @staticmethod
    def _parse(
        birthday: "raw.types.Birthday"
    ) -> "Birthdate":
        return Birthdate(
            day=birthday.day,
            month=birthday.month,
            year=getattr(birthday, "year", None)
        )

    def write(self):
        return raw.types.Birthday(
            day=self.day,
            month=self.month,
            year=self.year
        )
