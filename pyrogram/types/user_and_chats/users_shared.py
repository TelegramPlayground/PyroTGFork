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

import pyrogram
from pyrogram import types
from ..object import Object


class UsersShared(Object):
    """This object contains information about the users whose identifiers were shared with the bot using a :obj:`~pyrogram.types.KeyboardButtonRequestUsers` button.

    Parameters:
        request_id (``int``):
            Identifier of the request.

        users (List of :obj:`~pyrogram.types.User`):
            Information about users shared with the bot.

    """

    def __init__(
        self,
        *,
        request_id: int,
        users: List["types.User"]
    ):
        super().__init__()

        self.request_id = request_id
        self.users = users
