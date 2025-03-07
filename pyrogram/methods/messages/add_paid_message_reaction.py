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
from pyrogram import raw, types


class AddPaidMessageReaction:
    async def add_paid_message_reaction(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        star_count: int = None,
        paid_reaction_type: "types.PaidReactionType" = None
    ) -> "types.MessageReactions":
        """Adds the paid message reaction to a message.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``):
                Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.

            star_count (``int``, *optional*):
                Number of Telegram Stars to be used for the reaction; 1-2500.

            paid_reaction_type (:obj:`~pyrogram.types.PaidReactionType`, *optional*):
                Type of the paid reaction; pass None if the user didn't choose reaction type explicitly, for example, the reaction is set from the message bubble.

        Returns:
            On success, :obj:`~pyrogram.types.MessageReactions`: is returned.

        Example:
            .. code-block:: python

                # Add a paid reaction to a message
                await app.add_paid_message_reaction(chat_id, message_id, 1)

        """

        r = await self.invoke(
            raw.functions.messages.SendPaidReaction(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                random_id=self.rnd_id(),
                count=star_count,
                private=await paid_reaction_type.write(self) if paid_reaction_type else None
            )
        )
        for i in r.updates:
            if isinstance(i, raw.types.UpdateMessageReactions):
                return types.MessageReactions._parse(self, i.reactions)
        # TODO
        return r
