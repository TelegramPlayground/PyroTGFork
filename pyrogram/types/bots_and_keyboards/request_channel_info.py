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

from ..object import Object


class RequestChannelInfo(Object):
    """Contains information about a channel peer type.

    Parameters:
        button_id (``int``):
            Identifier of button.

        is_creator (``bool``, *optional*):
            If True, returns the list of chats where this user is a channel creator.

        has_username (``bool``, *optional*):
            If True, returns the list of chats where chat has username.

        max_quantity(``int``, *optional*):
            Max quantity of peers.
    """

    def __init__(
        self, *,
        button_id: int,
        is_creator: bool = None,
        has_username: bool = None,
        max_quantity: int = None,
    ):
        super().__init__()

        self.button_id = button_id
        self.is_creator = is_creator
        self.has_username = has_username
        self.max_quantity = max_quantity
