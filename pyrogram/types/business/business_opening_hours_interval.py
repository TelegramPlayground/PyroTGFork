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

from datetime import datetime

import pyrogram
from pyrogram import raw, types, utils

from ..object import Object


class BusinessOpeningHoursInterval(Object):
    """

    Parameters:
        opening_minute (``int``):
            The minute's sequence number in a week, starting on Monday, marking the start of the time interval during which the business is open; 0 - 7 * 24 * 60

        closing_minute (``int``):
            The minute's sequence number in a week, starting on Monday, marking the end of the time interval during which the business is open; 0 - 8 * 24 * 60

    """

    def __init__(
        self,
        *,
        opening_minute: int = None,
        closing_minute: int = None
    ):
        super().__init__()

        self.opening_minute = opening_minute
        self.closing_minute = closing_minute


    @staticmethod
    def _parse(
        weekly_open_: "raw.types.BusinessWeeklyOpen"
    ) -> "BusinessOpeningHoursInterval":
        return BusinessOpeningHoursInterval(
            opening_minute=weekly_open_.start_minute,
            closing_minute=weekly_open_.end_minute
        )
