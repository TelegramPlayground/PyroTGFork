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

from typing import List
from datetime import datetime

import pyrogram
from pyrogram import raw, types, utils

from ..object import Object


class BusinessOpeningHours(Object):
    """

    Parameters:
        time_zone_name (``str``):
            Unique name of the time zone for which the opening hours are defined

        opening_hours (List of :obj:`~pyrogram.types.BusinessOpeningHoursInterval`):
            List of time intervals describing business opening hours

    """

    def __init__(
        self,
        *,
        time_zone_name: str = None,
        opening_hours: List["types.BusinessOpeningHoursInterval"] = None,
        _raw: "raw.types.BusinessWorkHours" = None
    ):
        super().__init__()

        self.time_zone_name = time_zone_name
        self.opening_hours = opening_hours
        self._raw = _raw


    @staticmethod
    def _parse(
        client,
        business_work_hours: "raw.types.BusinessWorkHours"
    ) -> "BusinessOpeningHours":
        return BusinessOpeningHours(
            time_zone_name=getattr(business_work_hours, "timezone_id", None),
            opening_hours=types.List(
                [
                    types.BusinessOpeningHoursInterval._parse(
                        weekly_open_
                    ) for weekly_open_ in business_work_hours.weekly_open
                ]
            ) if getattr(business_work_hours, "weekly_open", None) else None,
            _raw=business_work_hours
        )
