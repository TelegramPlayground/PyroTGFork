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

from typing import Optional, Union

import pyrogram
from pyrogram import raw


class SetPersonalChat:
    async def set_personal_chat(
        self: "pyrogram.Client",
        chat_id: Optional[Union[int, str]] = None,
    ) -> bool:
        """Changes the personal chat of the current user

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str`, *optional*):
                Identifier of the new personal chat; pass None to remove the chat. Use :meth:`~pyrogram.Client.get_created_chats` with ``is_suitable_for_my_personal_chat`` to get suitable chats

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Update your personal chat
                await app.set_personal_chat(chat_id="@Pyrogram")

                # Hide your personal chat
                await app.set_personal_chat()
        """

        return bool(
            await self.invoke(
                raw.functions.account.UpdatePersonalChannel(
                    channel=await self.resolve_peer(
                        chat_id
                    ) if chat_id else raw.types.InputChannelEmpty()
                )
            )
        )
