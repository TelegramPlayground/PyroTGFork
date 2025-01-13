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

from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types


class CreateGroup:
    async def create_group(
        self: "pyrogram.Client",
        title: str,
        users: Union[Union[int, str], list[Union[int, str]]] = None,
        message_auto_delete_time: int = 0
    ) -> "types.Chat":
        """Create a new basic group.

        .. note::

            If you want to create a new supergroup, use :meth:`~pyrogram.Client.create_supergroup` instead.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            title (``str``):
                The group title.

            users (``int`` | ``str`` | List of ``int`` or ``str``):
                Users to create a chat with.
                Multiple users can be invited by passing a list of IDs, usernames or phone numbers.
                Identifiers of users to be added to the basic group; may be empty to create a basic group without other members
            
            message_auto_delete_time (``int``, *optional*):
                Message auto-delete time value, in seconds; must be from 0 up to 365 * 86400 and be divisible by 86400. If 0, then messages aren't deleted automatically.

        Returns:
            :obj:`~pyrogram.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                await app.create_group("Group Title", user_id)
        """
        if users and not isinstance(users, list):
            users = [users]
        r = await self.invoke(
            raw.functions.messages.CreateChat(
                users=[await self.resolve_peer(u) for u in users] if users else [],
                title=title,
                ttl_period=message_auto_delete_time
            )
        )
        return types.Chat._parse_chat(self, r.updates.chats[0])
