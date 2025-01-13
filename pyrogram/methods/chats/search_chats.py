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
from pyrogram import raw, types, utils


class SearchChats:
    async def search_chats(
        self: "pyrogram.Client",
        query: str,
        limit: int = 10,
        personalize_result: bool = False
    ) -> list["types.Chat"]:
        """Searches for the specified query in the title and username of already known chats via request to the server.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            query (``str``):
                Query to search for.

            limit (``int``, *optional*):
                The maximum number of chats to be returned. Defaults to 10.

            personalize_result (``bool``, *optional*):
                True, if should return personalized results, else would return all found user identifiers. Defaults to False.

        Returns:
            List of :obj:`~pyrogram.types.Chat`: Returns chats in the order seen in the main chat list

        Example:
            .. code-block:: python

                chats = await app.search_chats("Pyrogram")

        """
        r = await self.invoke(
            raw.functions.contacts.Search(
                q=query,
                limit=limit
            )
        )
        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}
        c = []
        attr = "my_results" if personalize_result else "results"
        m = getattr(r, attr, [])
        for o in m:
            id = utils.get_raw_peer_id(o)
            if isinstance(o, raw.types.PeerUser):
                c.append(
                    types.Chat._parse_chat(
                        self,
                        users[id]
                    )
                )
            else:
                c.append(
                    types.Chat._parse_chat(
                        self,
                        chats[id]
                    )
                )
        return types.List(c)
