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

from datetime import datetime

import pyrogram
from pyrogram import types

from ..object import Object


class PollOption(Object):
    """Contains information about one answer option in a poll.

    Parameters:
        persistent_id (``str``):
            Unique identifier of the option, persistent on option addition and deletion.

        text (:obj:`~pyrogram.types.FormattedText`):
            Option text, 1-100 characters.

        voter_count (``int``):
            Number of users that voted for this option.
            Equals to 0 until you vote.

        added_by_user (:obj:`~pyrogram.types.User`, *optional*):
            User who added the option; omitted if the option wasn't added by a user after poll creation.
        
        added_by_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Chat that added the option; omitted if the option wasn't added by a chat after poll creation.
        
        addition_date (:py:obj:`~datetime.datetime`, *optional*):
            Date the message was last edited.

        data (``bytes``):
            The data this poll option is holding.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        persistent_id: str,
        text: "types.FormattedText",
        voter_count: int,
        data: bytes,
        added_by_user: "types.User" = None,
        added_by_chat: "types.Chat" = None,
        addition_date: datetime = None,
    ):
        super().__init__(client)

        self.persistent_id = persistent_id
        self.text = text
        self.voter_count = voter_count
        self.data = data
        self.added_by_user = added_by_user
        self.added_by_chat = added_by_chat
        self.addition_date = addition_date
