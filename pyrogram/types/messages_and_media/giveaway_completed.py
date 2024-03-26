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
from typing import List

import pyrogram

from pyrogram import raw, types
from ..object import Object



class GiveawayCompleted(Object):
    """This object represents a service message about the completion of a giveaway without public winners.

    Parameters:
        winner_count (``int``):
            Number of winners in the giveaway
        
        unclaimed_prize_count (``int``, *optional*):
            Number of undistributed prizes

        giveaway_message (:obj:`~pyrogram.types.Message`, *optional*):
            Message with the giveaway that was completed, if it wasn't deleted

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        winner_count: int,
        unclaimed_prize_count: int = None,
        giveaway_message: "types.Message" = None
    ):
        super().__init__(client)

        self.winner_count = winner_count
        self.unclaimed_prize_count = unclaimed_prize_count
        self.giveaway_message = giveaway_message


    @staticmethod
    def _parse(
        client,
        giveaway_results: "raw.types.MessageActionGiveawayResults",
        message_id: int = None
    ) -> "GiveawayCompleted":
        if isinstance(giveaway_results, raw.types.MessageActionGiveawayResults):
            return GiveawayCompleted(
                client=client,
                winner_count=giveaway_results.winners_count,
                unclaimed_prize_count=getattr(giveaway_results, "unclaimed_count", None),
                giveaway_message=types.Message(
                    client=client,
                    id=message_id
                ) if message_id else None
            )
