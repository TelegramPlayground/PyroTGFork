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

from pyrogram import raw
from ..object import Object


class ChatBoostAdded(Object):
    """This object represents a service message about a user boosting a chat.

    Parameters:
        boost_count (``int``):
            Number of boosts added by the user

    """

    def __init__(
        self,
        *,
        boost_count: int,
    ):
        super().__init__()

        self.boost_count = boost_count

    @staticmethod
    def _parse(action: "raw.types.MessageActionBoostApply"):
        return ChatBoostAdded(
            boost_count=action.boosts
        )
