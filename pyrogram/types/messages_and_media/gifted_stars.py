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

from random import choice

from pyrogram import raw, types
from ..object import Object


class GiftedStars(Object):
    """Telegram Stars were gifted to a user

    Parameters:
        gifter_user_id (``int``):
            The identifier of a user that gifted Telegram Stars; 0 if the gift was anonymous or is outgoing

        receiver_user_id (``int``):
            The identifier of a user that received Telegram Stars; 0 if the gift is incoming

        currency (``str``):
            Currency for the paid amount

        amount (``int``):
            The paid amount, in the smallest units of the currency

        cryptocurrency (``str``):
            Cryptocurrency used to pay for the gift; may be empty if none

        cryptocurrency_amount (``int``):
            The paid amount, in the smallest units of the cryptocurrency; 0 if none

        star_count (``int``):
            Number of Telegram Stars that were gifted

        transaction_id (``str``):
            Identifier of the transaction for Telegram Stars purchase; for receiver only

        sticker (:obj:`~pyrogram.types.Sticker`):
            A sticker to be shown in the transaction information; may be None if unknown

    """

    def __init__(
        self,
        *,
        gifter_user_id: int = None,
        receiver_user_id: int = None,
        currency: str = None,
        amount: int = None,
        cryptocurrency: str = None,
        cryptocurrency_amount: int = None,
        star_count: int = None,
        transaction_id: str = None,
        sticker: "types.Sticker" = None,
    ):
        super().__init__()

        self.gifter_user_id = gifter_user_id
        self.receiver_user_id = receiver_user_id
        self.currency = currency
        self.amount = amount
        self.cryptocurrency = cryptocurrency
        self.cryptocurrency_amount = cryptocurrency_amount
        self.star_count = star_count
        self.transaction_id = transaction_id
        self.sticker = sticker

    @staticmethod
    async def _parse(
        client,
        gifted_stars: "raw.types.MessageActionGiftStars",
        gifter_user_id: int,
        receiver_user_id: int
    ) -> "GiftedStars":
        sticker = None
        stickers, _ = await client._get_raw_stickers(
            raw.types.InputStickerSetPremiumGifts()
        )
        sticker = choice(stickers)
        return GiftedStars(
            gifter_user_id=gifter_user_id,
            receiver_user_id=receiver_user_id,
            currency=gifted_stars.currency,
            amount=gifted_stars.amount,
            cryptocurrency=getattr(gifted_stars, "crypto_currency", None),
            cryptocurrency_amount=getattr(gifted_stars, "crypto_amount", None),
            star_count=gifted_stars.stars,
            transaction_id=getattr(gifted_stars, "transaction_id", None),
            sticker=sticker
        )
