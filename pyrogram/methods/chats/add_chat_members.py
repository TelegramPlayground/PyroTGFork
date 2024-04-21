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

from typing import Union, List

import pyrogram
from pyrogram import raw, types


class AddChatMembers:
    async def add_chat_members(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        user_ids: Union[Union[int, str], List[Union[int, str]]],
        forward_limit: int = 100
    ) -> Union[List["types.Message"], "types.Message", bool]:
        """Add new chat members to a group, supergroup or channel

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                The group, supergroup or channel id

            user_ids (``int`` | ``str`` | List of ``int`` or ``str``):
                Users to add in the chat
                You can pass an ID (int), username (str) or phone number (str).
                Multiple users can be added by passing a list of IDs, usernames or phone numbers.

            forward_limit (``int``, *optional*):
                How many of the latest messages you want to forward to the new members. Pass 0 to forward none of them.
                Only applicable to basic groups (the argument is ignored for supergroups or channels).
                Defaults to 100 (max amount).

        Returns:
            List[:obj:`~pyrogram.types.Message`] | :obj:`~pyrogram.types.Message` | ``bool``: On success, a service message will be returned (when applicable),
            otherwise, in case a message object couldn't be returned, True is returned.

        Example:
            .. code-block:: python

                # Add one member to a group or channel
                await app.add_chat_members(chat_id, user_id)

                # Add multiple members to a group or channel
                await app.add_chat_members(chat_id, [user_id1, user_id2, user_id3])

                # Change forward_limit (for basic groups only)
                await app.add_chat_members(chat_id, user_id, forward_limit=25)
        """
        peer = await self.resolve_peer(chat_id)

        if not isinstance(user_ids, list):
            user_ids = [user_ids]

        r = []

        if isinstance(peer, raw.types.InputPeerChat):
            for user_id in user_ids:
                r.append(
                    await self.invoke(
                        raw.functions.messages.AddChatUser(
                            chat_id=peer.chat_id,
                            user_id=await self.resolve_peer(user_id),
                            fwd_limit=forward_limit
                        )
                    )
                )
        else:
            r.append(
                await self.invoke(
                    raw.functions.channels.InviteToChannel(
                        channel=peer,
                        users=[
                            await self.resolve_peer(user_id)
                            for user_id in user_ids
                        ]
                    )
                )
            )

        _rc = []
        for rr in r:
            for i in rr.updates.updates:
                if isinstance(
                    i,
                    (
                        raw.types.UpdateNewMessage,
                        raw.types.UpdateNewChannelMessage
                    )
                ):
                    _rc.append(
                        await types.Message._parse(
                            self, i.message,
                            {i.id: i for i in rr.updates.users},
                            {i.id: i for i in rr.updates.chats},
                        )
                    )
                    break

        if len(_rc) > 0:
            if len(_rc) == 1:
                return _rc[0]
            else:
                return types.List(_rc)
        else:
            return True
