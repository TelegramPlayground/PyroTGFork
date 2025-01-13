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

from pyrogram import raw, types, utils
from ..object import Object



class Giveaway(Object):
    """This object represents a message about a scheduled giveaway.

    Parameters:
        chats (:obj:`~pyrogram.types.Chat`):
            The list of chats which the user must join to participate in the giveaway

        winners_selection_date (:py:obj:`~datetime.datetime`):
            Point in time (Unix timestamp) when winners of the giveaway will be selected
        
        winner_count (``int``):
            The number of users which are supposed to be selected as winners of the giveaway
        
        only_new_members (``bool``, *optional*):
            True, if only users who join the chats after the giveaway started should be eligible to win

        has_public_winners (``bool``, *optional*):
            True, if the list of giveaway winners will be visible to everyone
        
        prize_description (``str``, *optional*):
            Description of additional giveaway prize
        
        country_codes (``str``, *optional*):
            A list of two-letter `ISO 3166-1 alpha-2 <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`_ country codes indicating the countries from which eligible users for the giveaway must come. If empty, then all users can participate in the giveaway. Users with a phone number that was bought on Fragment can always participate in giveaways.

        prize_star_count (``int``, *optional*):
            The number of Telegram Stars to be split between giveaway winners; for Telegram Star giveaways only

        premium_subscription_month_count (``int``, *optional*):
            The number of months the Telegram Premium subscription won from the giveaway will be active for

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chats: list["types.Chat"],
        winners_selection_date: datetime,
        winner_count: int,
        only_new_members: bool = None,
        has_public_winners: bool = None,
        prize_description: str = None,
        country_codes: list[str] = None,
        prize_star_count: int = None,
        premium_subscription_month_count: int = None
    ):
        super().__init__(client)

        self.chats = chats
        self.winners_selection_date = winners_selection_date
        self.winner_count = winner_count
        self.only_new_members = only_new_members
        self.has_public_winners = has_public_winners
        self.prize_description = prize_description
        self.country_codes = country_codes
        self.prize_star_count = prize_star_count
        self.premium_subscription_month_count = premium_subscription_month_count


    @staticmethod
    def _parse(
        client,
        chats: dict,
        giveaway_media: "raw.types.MessageMediaGiveaway"
    ) -> "Giveaway":
        if isinstance(giveaway_media, raw.types.MessageMediaGiveaway):
            return Giveaway(
                client=client,
                chats=types.List(
                    types.Chat._parse_channel_chat(client, chats.get(channel))
                    for channel in giveaway_media.channels
                ),
                winners_selection_date=utils.timestamp_to_datetime(giveaway_media.until_date),
                winner_count=giveaway_media.quantity,
                only_new_members=getattr(giveaway_media, "only_new_subscribers", None),
                has_public_winners=getattr(giveaway_media, "winners_are_visible", None),
                prize_description=getattr(giveaway_media, "prize_description", None),
                country_codes=giveaway_media.countries_iso2 or None,
                prize_star_count=giveaway_media.stars,
                premium_subscription_month_count=giveaway_media.months
            )
