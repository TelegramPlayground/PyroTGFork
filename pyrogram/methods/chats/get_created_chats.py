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

from typing import List, Union

import pyrogram
from pyrogram import raw
from pyrogram import types


class GetCreatedChats:
    async def get_created_chats(
        self: "pyrogram.Client",
        # TODO: find a better name?
        is_inactive_chat: bool = False,
        is_my_public_has_username: bool = True,
        is_my_public_location_based: bool = False,
        check_created_my_public_chat_limit: bool = False,
        is_suitable_for_my_personal_chat: bool = False,
    ) -> List["types.Chat"]:
        """Get a list of chats of the specified type of the current user account

        .. include:: /_includes/usable-by/users.rst

        Exactly one of ``is_inactive_chat`` OR ``is_my_public_has_username`` should be passed.

        Parameters:
            is_inactive_chat (``bool``, *optional*):
                True, to return a list of recently inactive supergroups and channels. Can be used when user reaches limit on the number of joined supergroups and channels and receives CHANNELS_TOO_MUCH error. Also, the limit can be increased with Telegram Premium. Defaults to False.

            is_my_public_has_username (``bool``, *optional*):
                True, if the chat is public, because it has an active username. Defaults to True.
            
            is_my_public_location_based (``bool``, *optional*):
                True, if the chat is public, because it is a location-based supergroup. Defaults to False.

            check_created_my_public_chat_limit (``bool``, *optional*):
                Checks whether the maximum number of owned public chats has been reached. The limit can be increased with Telegram Premium. Defaults to False.

            is_suitable_for_my_personal_chat (``bool``, *optional*):
                True, if the chat can be used as a personal chat. Defaults to False.

        Returns:
            List[:obj:`~pyrogram.types.Chat`]: The list of chats.

        Example:
            .. code-block:: python

                chats = await app.get_created_chats()
                print(chats)
        """
        if is_inactive_chat:
            r = await self.invoke(
                raw.functions.channels.GetInactiveChannels()
            )
        else:
            r = await self.invoke(
                raw.functions.channels.GetAdminedPublicChannels(
                    by_location=is_my_public_location_based,
                    check_limit=check_created_my_public_chat_limit,
                    for_personal=is_suitable_for_my_personal_chat
                )
            )
        # TODO: fix inconsistency
        return types.List([
            types.Chat._parse_chat(self, x)
            for x in getattr(r, "chats", [])
        ])
