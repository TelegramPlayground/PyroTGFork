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
from pyrogram import raw, utils

from ..object import Object


class StoryStealthMode(Object):
    """Story stealth mode.

    Parameters:
        active_until_date (``int``):
            Point in time (Unix timestamp) until stealth mode is active; None if it is disabled.

        cooldown_until_date (``int``):
            Point in time (Unix timestamp) when stealth mode can be enabled again; None if there is no active cooldown.

    """

    def __init__(
        self,
        *,
        active_until_date: int = None,
        cooldown_until_date: int = None,
    ):
        super().__init__()

        self.active_until_date = active_until_date
        self.cooldown_until_date = cooldown_until_date

    @staticmethod
    def _parse(ssm: "raw.types.StoriesStealthMode") -> "StoryStealthMode":
        return StoryStealthMode(
            active_until_date=utils.timestamp_to_datetime(getattr(ssm, "active_until_date", 0)),
            cooldown_until_date=utils.timestamp_to_datetime(getattr(ssm, "cooldown_until_date", 0)),
        )
