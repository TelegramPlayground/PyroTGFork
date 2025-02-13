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

import logging
from typing import Union

import pyrogram
from pyrogram import raw, types

log = logging.getLogger(__name__)


class SetReaction:
    async def set_reaction(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int = None,
        story_id: int = None,
        reaction: list["types.ReactionType"] = [],
        is_big: bool = False,
        add_to_recent: bool = True
    ) -> "types.MessageReactions":
        """Use this method to change the chosen reactions on a message.
        Service messages of some types can't be reacted to. Use :obj:`~pyrogram.types.Message._raw.reactions_are_possible` to check if it is possible to react to the message.
        Automatically forwarded messages from a channel to its discussion group have the same available reactions as messages in the channel.
        Bots can't use paid reactions.

        You must use exactly one of ``message_id`` OR ``story_id``.

            If you specify, ``message_id``

                .. include:: /_includes/usable-by/users-bots.rst

            If you specify, ``story_id``

                .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``, *optional*):
                Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.

            story_id (``int``, *optional*):
                Identifier of the story.

            reaction (List of :obj:`~pyrogram.types.ReactionType`, *optional*):
                New list of reaction types to set on the message.
                Pass None as emoji (default) to retract the reaction.
                Use :meth:`~pyrogram.Client.add_paid_message_reaction` instead to add a paid reaction.

            is_big (``bool``, *optional*):
                Pass True to set the reaction with a big animation.
                Defaults to False.

            add_to_recent (``bool``, *optional*):
                Pass True if the reaction should appear in the recently used reactions.
                This option is applicable only for users.
                Defaults to True.

        Returns:
            On success, :obj:`~pyrogram.types.MessageReactions`: is returned.

        Example:
            .. code-block:: python

                # Send a reaction as a bot
                await app.set_reaction(chat_id, message_id, [ReactionTypeEmoji(emoji="👍")])

                # Send multiple reaction as a premium user
                await app.set_reaction(chat_id, message_id, [ReactionTypeEmoji(emoji="👍"),ReactionTypeEmoji(emoji="😍")],True)

                # Retract a reaction
                await app.set_reaction(chat_id, message_id=message_id)
        """

        raw_reactions = []
        if not reaction:
            raw_reactions = [raw.types.ReactionEmpty()]
        else:
            for r in reaction:
                if isinstance(r, types.ReactionTypePaid):
                    raise ValueError("This type of reaction is not supported using this method")
                else:
                    raw_reactions.append(r.write(self))

        if message_id is not None:
            r = await self.invoke(
                raw.functions.messages.SendReaction(
                    peer=await self.resolve_peer(chat_id),
                    msg_id=message_id,
                    reaction=raw_reactions,
                    big=is_big,
                    add_to_recent=add_to_recent
                )
            )
            for i in r.updates:
                if isinstance(i, raw.types.UpdateMessageReactions):
                    return types.MessageReactions._parse(self, i.reactions)
            # TODO
            return r

        elif story_id is not None:
            r = await self.invoke(
                raw.functions.stories.SendReaction(
                    peer=await self.resolve_peer(chat_id),
                    story_id=story_id,
                    reaction=raw_reactions[0],
                    add_to_recent=add_to_recent
                )
            )
            # TODO
            return r

        else:
            raise ValueError("You need to pass one of message_id OR story_id!")


    async def send_reaction(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        emoji: str = "",
        big: bool = False,
        add_to_recent: bool = True
    ) -> bool:
        log.warning(
            "This property is deprecated. "
            "Please use set_reaction instead"
        )
        return bool(
            await self.invoke(
                raw.functions.messages.SendReaction(
                    reaction=[raw.types.ReactionEmoji(emoticon=emoji)] if emoji else None,
                    big=big,
                    peer=await self.resolve_peer(chat_id),
                    msg_id=message_id,
                    add_to_recent=add_to_recent
                )
            )
        )
