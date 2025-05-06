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

from asyncio import sleep
from typing import Union, Optional, AsyncGenerator

import pyrogram
from pyrogram import raw, types


class GetReceivedGifts:
    async def get_received_gifts(
        self: "pyrogram.Client",
        owner_id: Union[int, str],
        offset: str = "",
        limit: int = 0,
        exclude_unsaved: bool = None,
        exclude_saved: bool = None,
        exclude_unlimited: bool = None,
        exclude_limited: bool = None,
        exclude_upgraded: bool = None,
        sort_by_price: bool = None
    ) -> Optional[AsyncGenerator["types.ReceivedGift", None]]:
        """Returns gifts received by the given user or chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            owner_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            offset (``str``, *optional*):
                Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results.

            limit (``int``, *optional*):
                The maximum number of gifts to be returned; must be positive and can't be greater than 100. For optimal performance, the number of returned objects is chosen by Telegram Server and can be smaller than the specified limit.

            exclude_unsaved (``bool``, *optional*):
                Pass True to exclude gifts that aren't saved to the chat's profile page. Always True for gifts received by other users and channel chats without ``can_post_messages`` administrator right.

            exclude_saved (``bool``, *optional*):
                Pass True to exclude gifts that are saved to the chat's profile page. Always False for gifts received by other users and channel chats without ``can_post_messages`` administrator right.

            exclude_unlimited (``bool``, *optional*):
                Pass True to exclude gifts that can be purchased unlimited number of times.

            exclude_limited (``bool``, *optional*):
                Pass True to exclude gifts that can be purchased limited number of times.

            exclude_upgraded (``bool``, *optional*):
                Pass True to exclude upgraded gifts.

            sort_by_price (``bool``, *optional*):
                Pass True to sort results by gift price instead of send date.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.ReceivedGift` objects.

        Example:
            .. code-block:: python

                async for received_gift in app.get_received_gifts(owner_id):
                    print(received_gift)
        """
        peer = await self.resolve_peer(owner_id)

        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        while True:
            r = await self.invoke(
                raw.functions.payments.GetSavedStarGifts(
                    peer=peer,
                    offset=offset,
                    limit=limit,
                    exclude_unsaved=exclude_unsaved,
                    exclude_saved=exclude_saved,
                    exclude_unlimited=exclude_unlimited,
                    exclude_limited=exclude_limited,
                    exclude_unique=exclude_upgraded,
                    sort_by_value=sort_by_price
                ),
                sleep_threshold=60
            )

            users = {u.id: u for u in r.users}
            chats = {c.id: c for c in r.chats}

            received_gifts = [
                await types.ReceivedGift._parse(self, gift, users, chats)
                for gift in r.gifts
            ]

            if not received_gifts:
                return

            for received_gift in received_gifts:
                await sleep(0)
                yield received_gift

                current += 1

                if current >= total:
                    return

            offset = r.next_offset

            if not offset:
                return
