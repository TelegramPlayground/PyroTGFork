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
from typing import Union, AsyncGenerator

import pyrogram
from pyrogram import types, raw


class LoadGroupCallParticipants:
    async def load_group_call_participants(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        limit: int = 0
    ) -> AsyncGenerator["types.GroupCallParticipant", None]:
        """Loads participants list in a group call of a chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat. A chat can be either a basic group or a supergroup.

            limit (``int``, *optional*):
                Limits the number of participants to be retrieved. By default, no limit is applied and all participants are returned.

        Returns:
            ``Generator``: On success, a generator yielding :obj:`~pyrogram.types.GroupCallParticipant` object is returned.

        Example:
            .. code-block:: python

                # Get participants
                async for participant in app.load_group_call_participants(chat_id):
                    print(participant)

        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(raw.functions.channels.GetFullChannel(channel=peer))
        elif isinstance(peer, raw.types.InputPeerChat):
            r = await self.invoke(raw.functions.messages.GetFullChat(chat_id=peer.chat_id))
        else:
            raise ValueError("Target chat should be group, supergroup or channel.")

        full_chat = r.full_chat

        if not getattr(full_chat, "call", None):
            raise ValueError("There is no active call in this chat.")

        current = 0
        offset = ""
        total = abs(limit) or (1 << 31) - 1
        limit = min(20, total)

        while True:
            r = await self.invoke(
                raw.functions.phone.GetGroupParticipants(
                    call=full_chat.call,
                    ids=[],
                    sources=[],
                    offset=offset,
                    limit=limit
                ),
                sleep_threshold=60
            )

            users = {u.id: u for u in r.users}
            chats = {c.id: c for c in r.chats}
            participants = [
                types.GroupCallParticipant._parse(
                    self, participant, users, chats
                ) for participant in r.participants
            ]

            if not participants:
                return

            offset = r.next_offset

            for participant in participants:
                await sleep(0)
                yield participant

                current += 1

                if current >= total:
                    return
