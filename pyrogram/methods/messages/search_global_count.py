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
from pyrogram import raw, enums


class SearchGlobalCount:
    async def search_global_count(
        self: "pyrogram.Client",
        query: str = "",
        filter: "enums.MessagesFilter" = enums.MessagesFilter.EMPTY,
        chat_list: int = 0,
        chat_type_filter: "enums.ChatType" = None,
    ) -> int:
        """Get the count of messages resulting from a global search.

        If you want to get the actual messages, see :meth:`~pyrogram.Client.search_global`.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            query (``str``, *optional*):
                Text query string.
                Use "@" to search for mentions.

            filter (:obj:`~pyrogram.enums.MessagesFilter`, *optional*):
                Pass a filter in order to search for specific kind of messages only:

            chat_list (``int``, *optional*):
                Chat list in which to search messages; Only Main (0) and Archive (1) chat lists are supported. Defaults to (0) Main chat list.

            chat_type_filter (:obj:`~pyrogram.enums.ChatType`, *optional*):
                Additional filter for type of the chat (:obj:`~pyrogram.enums.ChatType.PRIVATE`, :obj:`~pyrogram.enums.ChatType.GROUP`, :obj:`~pyrogram.enums.ChatType.CHANNEL`) of the searched messages; pass None to search for messages in all chats.

        Returns:
            ``int``: On success, the messages count is returned.
        """
        r = await self.invoke(
            raw.functions.messages.SearchGlobal(
                q=query,
                filter=filter.value(),
                min_date=0,
                max_date=0,
                offset_rate=0,
                offset_peer=raw.types.InputPeerEmpty(),
                offset_id=0,
                limit=1,
                folder_id=chat_list,
                broadcasts_only=(chat_type_filter == enums.ChatType.CHANNEL) if chat_type_filter else None,
                groups_only=(chat_type_filter == enums.ChatType.GROUP) if chat_type_filter else None,
                users_only=(chat_type_filter == enums.ChatType.PRIVATE) if chat_type_filter else None,
            )
        )

        if hasattr(r, "count"):
            return r.count
        else:
            return len(r.messages)
