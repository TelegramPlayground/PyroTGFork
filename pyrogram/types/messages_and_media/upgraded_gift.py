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
from pyrogram import raw, utils
from ..object import Object


class UpgradedGift(Object):
    """Describes an upgraded gift that can be gifted to another user or transferred to TON blockchain as an NFT.

    Parameters:
        id (``int``):
            Unique identifier of the gift.

        title (``str``):
            The title of the upgraded gift.

        number (``int``):
            Unique number of the upgraded gift among gifts upgraded from the same gift.

        total_upgraded_count (``int``):
            Total number of gifts that were upgraded from the same gift.

        max_upgraded_count (``int``):
            The maximum number of gifts that can be upgraded from the same gift.

        owner_user_id (``int``, *optional*):
            User identifier of the user that owns the upgraded gift.

        owner_user_name (``str``, *optional*):
            User name of the user that owns the upgraded gift.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        title: str,
        number: int,
        total_upgraded_count: int,
        max_upgraded_count: int,
        owner_user_id: Optional[int] = None,
        owner_user_name: Optional[str] = None,
        _raw: "raw.types.StarGiftUnique" = None,
    ):
        super().__init__(client)

        self.id = id
        self.title = title
        self.number = number
        self.total_upgraded_count = total_upgraded_count
        self.max_upgraded_count = max_upgraded_count
        self.owner_user_id = owner_user_id
        self.owner_user_name = owner_user_name
        self._raw = _raw  # TODO


    @staticmethod
    def _parse(
        client,
        star_gift: "raw.types.StarGiftUnique"
    ) -> "UpgradedGift":
        return UpgradedGift(
            id=star_gift.id,
            title=star_gift.title,
            number=star_gift.num,
            total_upgraded_count=star_gift.availability_issued,
            max_upgraded_count=star_gift.availability_total,
            owner_user_id=utils.get_raw_peer_id(getattr(star_gift, "owner_id", None)),
            owner_user_name=getattr(star_gift, "owner_name", None),
            _raw=star_gift,
            client=client
        )
