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
from pyrogram import raw
from ..object import Object


class Contact(Object):
    """A phone contact.

    Parameters:
        phone_number (``str``):
            Phone number of the user.

        first_name (``str``):
            First name of the user; 1-64 characters.

        last_name (``str``, *optional*):
            Last name of the user; 0-64 characters.

        user_id (``int``, *optional*):
            Contact's user identifier in Telegram.

        vcard (``str``, *optional*):
            Additional data about the user in a form of `vCard <https://en.wikipedia.org/wiki/VCard>`_; 0-2048 bytes in length.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        phone_number: str,
        first_name: str,
        last_name: str = None,
        user_id: int = None,
        vcard: str = None
    ):
        super().__init__(client)

        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.vcard = vcard

    @staticmethod
    def _parse(client: "pyrogram.Client", contact: "raw.types.MessageMediaContact") -> "Contact":
        return Contact(
            phone_number=contact.phone_number,
            first_name=contact.first_name,
            last_name=contact.last_name or None,
            vcard=contact.vcard or None,
            user_id=contact.user_id or None,
            client=client
        )
