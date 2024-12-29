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

from typing import Optional

import pyrogram
from pyrogram import enums, raw, types, utils
from ..object import Object
from ..update import Update
from .message import Str


class PollAnswer(Object, Update):
    """This object represents an answer of a user in a non-anonymous poll.

    Parameters:
        poll_id (``str``):
            Unique poll identifier.

        voter_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            The chat that changed the answer to the poll, if the voter is anonymous.

        user (:obj:`~pyrogram.types.User`, *optional*):
            The user that changed the answer to the poll, if the voter isn't anonymous.

        option_ids (List of ``int``):
            0-based identifiers of chosen answer options. May be empty if the vote was retracted.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        poll_id: str,
        option_ids: list[int],
        user: Optional["types.User"] = None,
        voter_chat: Optional["types.Chat"] = None,
    ):
        super().__init__(client)

        self.poll_id = poll_id
        self.option_ids = option_ids
        self.user = user
        self.voter_chat = voter_chat

    @staticmethod
    def _parse_update(
        client,
        update: "raw.types.UpdateMessagePollVote",
        users: dict,
        chats: dict,
    ):
        if isinstance(update, raw.types.UpdateMessagePollVote):
            user = None
            voter_chat = None
            if isinstance(update.peer, raw.types.PeerUser):
                user = types.Chat._parse_user_chat(client, users[update.peer.user_id])

            elif isinstance(update.peer, raw.types.PeerChat):
                voter_chat = types.Chat._parse_chat_chat(client, chats[update.peer.chat_id])

            else:
                voter_chat = types.Chat._parse_channel_chat(client, chats[update.peer.channel_id])

            return PollAnswer(
                poll_id=str(update.poll_id),
                option_ids=[
                    "{:0>2x}".format(option[0])
                    for option in update.options
                ],
                user=user,
                voter_chat=voter_chat,
                client=client
            )
