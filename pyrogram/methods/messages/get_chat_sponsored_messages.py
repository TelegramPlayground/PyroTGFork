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
from pyrogram import raw, types


class GetChatSponsoredMessages:
    async def get_chat_sponsored_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
    ) -> Optional[list["types.SponsoredMessage"]]:
        """Returns sponsored messages to be shown in a chat; for channel chats only.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns:
            List of :obj:`~pyrogram.types.SponsoredMessage`: a list of sponsored messages is returned.

        Example:
            .. code-block:: python

                # Get a sponsored messages
                sm = await app.get_chat_sponsored_messages(chat_id)
                print(sm)

        """
        r = await self.invoke(
            raw.functions.messages.GetSponsoredMessages(
                peer=await self.resolve_peer(chat_id)
            )
        )

        if isinstance(r, raw.types.messages.SponsoredMessagesEmpty):
            return None

        return types.List([
            types.SponsoredMessage._parse(self, sm)
            for sm in r.messages
        ])
