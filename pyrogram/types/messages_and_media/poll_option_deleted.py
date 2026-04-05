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

from pyrogram import raw, types
from ..object import Object


class PollOptionDeleted(Object):
    """This object represents a service message about an option deleted from a poll.

    Parameters:
        poll_message (:obj:`~pyrogram.types.Message`, *optional*):
            Message containing the poll to which the option was added, if known.
        
        option_persistent_id (``str``):
            Unique identifier of the added option.
        
        option_text (:obj:`~pyrogram.types.FormattedText`):
            Option text.

    """

    def __init__(
        self,
        *,
        option_persistent_id: str,
        poll_message: "types.Message" = None,
        option_text: "types.FormattedText" = None,
    ):
        super().__init__()

        self.option_persistent_id = option_persistent_id
        self.poll_message = poll_message
        self.option_text = option_text

    @staticmethod
    def _parse(
        client,
        message: "raw.types.MessageService",
    ) -> "PollOptionDeleted":
        action: "raw.types.MessageActionPollDeleteAnswer" = message.action
        answer: "raw.types.PollAnswer" = action.answer
        return PollOptionDeleted(
            option_persistent_id=answer.option.decode("UTF-8"),
            poll_message=None,
            option_text=types.FormattedText._parse(client, answer.text)
        )
