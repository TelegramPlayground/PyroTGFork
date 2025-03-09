#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present <https://github.com/TelegramPlayGround>
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
from typing import Optional, Union

import pyrogram
from pyrogram import raw, types, utils
from .message import Str
from ..object import Object


class ReceivedGift(Object):
    """Represents a gift received by a user or a chat.

    Parameters:
        sender_user (:obj:`~pyrogram.types.User`, *optional*):
            Identifier of the user that sent the gift; None if unknown.

        text (``str``, *optional*):
            Message added to the gift.
        
        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date when the gift was sent.

        is_private (``bool``, *optional*):
            True, if the sender and gift text are shown only to the gift receiver; otherwise, everyone are able to see them.

        is_saved (``bool``, *optional*):
            True, if the gift is displayed on the user's profile page; may be False only for the receiver of the gift.

        is_pinned (``bool``, *optional*):
            True, if the gift is pinned to the top of the chat's profile page.

        gift (:obj:`~pyrogram.types.Gift` | :obj:`~pyrogram.types.UpgradedGift`, *optional*):
            Information about the gift.
        
        message_id (``int``, *optional*):
            Identifier of the message with the gift in the chat with the sender of the gift; can be None or an identifier of a deleted message; only for the gift receiver.

        sell_star_count (``int``, *optional*):
            Number of Telegram Stars that can be claimed by the receiver instead of the regular gift; 0 if the gift can't be sold by the current user.

        was_converted (``bool``, *optional*):
            True, if the gift was converted to Telegram Stars; only for the receiver of the gift.

        can_be_upgraded (``bool``, *optional*):
            True, if the gift is a regular gift that can be upgraded to a unique gift; only for the receiver of the gift.

        was_refunded (``bool``, *optional*):
            True, if the gift was refunded and isn't available anymore.

        prepaid_upgrade_star_count (``int``, *optional*):
            Number of Telegram Stars that were paid by the sender for the ability to upgrade the gift.

        can_be_transferred (``bool``, *optional*):
            True, if the gift is an upgraded gift that can be transferred to another user; only for the receiver of the gift.

        transfer_star_count (``int``, *optional*):
            Number of Telegram Stars that must be paid to transfer the upgraded gift; only for the receiver of the gift.

        export_date (:py:obj:`~datetime.datetime`, *optional*):
            Point in time (Unix timestamp) when the upgraded gift can be transferred to TON blockchain as an NFT; None if NFT export isn't possible; only for the receiver of the gift.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        sender_user: Optional["types.User"] = None,
        text: Optional[str] = None,
        entities: list["types.MessageEntity"] = None,
        date: datetime,
        is_private: Optional[bool] = None,
        is_saved: Optional[bool] = None,
        is_pinned: Optional[bool] = None,
        gift: Optional[Union["types.Gift", "types.UpgradedGift"]] = None,
        message_id: Optional[int] = None,
        sell_star_count: Optional[int] = None,
        was_converted: Optional[bool] = None,
        can_be_upgraded: Optional[bool] = None,
        was_refunded: Optional[bool] = None,
        prepaid_upgrade_star_count: Optional[int] = None,
        can_be_transferred: Optional[bool] = None,
        transfer_star_count: Optional[int] = None,
        export_date: datetime = None,
    ):
        super().__init__(client)

        self.sender_user = sender_user
        self.text = text
        self.entities = entities
        self.date = date
        self.is_private = is_private
        self.is_saved = is_saved
        self.is_pinned = is_pinned
        self.gift = gift
        self.message_id = message_id
        self.sell_star_count = sell_star_count
        self.was_converted = was_converted
        self.can_be_upgraded = can_be_upgraded
        self.was_refunded = was_refunded
        self.prepaid_upgrade_star_count = prepaid_upgrade_star_count
        self.can_be_transferred = can_be_transferred
        self.transfer_star_count = transfer_star_count
        self.export_date = export_date


    @staticmethod
    async def _parse(
        client,
        saved_star_gift: "raw.types.SavedStarGift",
        users: dict,
        chats: dict
    ) -> "ReceivedGift":
        text, entities = None, None
        if getattr(saved_star_gift, "message", None):
            text = saved_star_gift.message.text or None
            entities = [types.MessageEntity._parse(client, entity, users) for entity in saved_star_gift.message.entities]
            entities = types.List(filter(lambda x: x is not None, entities))
        sender_user = utils.get_raw_peer_id(saved_star_gift.from_id)
        return ReceivedGift(
            sender_user=types.User._parse(
                client,
                users.get(sender_user)
            ) if sender_user else None,
            text=Str(text).init(entities) if text else None,
            entities=entities,
            date=utils.timestamp_to_datetime(saved_star_gift.date),
            is_private=getattr(saved_star_gift, "name_hidden", None),
            is_saved=not saved_star_gift.unsaved if getattr(saved_star_gift, "unsaved", False) else None,
            is_pinned=saved_star_gift.pinned_to_top,
            gift=await types.Gift._parse(
                client,
                saved_star_gift.gift,
                users
            ),
            message_id=getattr(saved_star_gift, "msg_id", None),
            sell_star_count=getattr(saved_star_gift, "convert_stars", 0),
            was_converted=bool(getattr(saved_star_gift, "saved_id", None)),
            can_be_upgraded=getattr(saved_star_gift, "can_upgrade", None),
            was_refunded=getattr(saved_star_gift, "refunded", None),
            prepaid_upgrade_star_count=getattr(saved_star_gift, "upgrade_stars", None),
            can_be_transferred=bool(getattr(saved_star_gift, "transfer_stars", None)),
            transfer_star_count=getattr(saved_star_gift, "transfer_stars", None),
            export_date=utils.timestamp_to_datetime(saved_star_gift.can_export_at),
            client=client
        )

    @staticmethod
    async def _parse_action(
        client,
        message: "raw.base.Message",
        users: dict,
        chats: dict
    ) -> "ReceivedGift":
        action = message.action

        text, entities = None, None
        if getattr(action, "message", None):
            text = action.message.text or None
            entities = [types.MessageEntity._parse(client, entity, users) for entity in action.message.entities]
            entities = types.List(filter(lambda x: x is not None, entities))
        # TODO 
        if isinstance(action, raw.types.MessageActionStarGift):
            return ReceivedGift(
                gift=await types.Gift._parse(
                    client,
                    action.gift,
                    users
                ),
                date=utils.timestamp_to_datetime(message.date),
                is_private=getattr(action, "name_hidden", None),
                is_saved=getattr(action, "saved", None),
                sender_user=types.User._parse(client, users.get(utils.get_raw_peer_id(message.peer_id))),
                message_id=message.id,
                text=Str(text).init(entities) if text else None,
                entities=entities,
                sell_star_count=getattr(action, "convert_stars", None),
                was_converted=getattr(action, "converted", None),
                can_be_upgraded=getattr(action, "can_upgrade", None),
                was_refunded=getattr(action, "refunded", None),
                prepaid_upgrade_star_count=getattr(action, "upgrade_stars", None),
                client=client
            )

        if isinstance(action, raw.types.MessageActionStarGiftUnique):
            return ReceivedGift(
                gift=await types.Gift._parse(
                    client,
                    action.gift,
                    users
                ),
                date=utils.timestamp_to_datetime(message.date),
                sender_user=types.User._parse(client, users.get(utils.get_raw_peer_id(message.peer_id))),
                message_id=message.id,
                text=Str(text).init(entities) if text else None,
                entities=entities,
                can_be_transferred=getattr(action, "transferred", None),
                was_refunded=getattr(action, "refunded", None),
                prepaid_upgrade_star_count=getattr(action, "upgrade_stars", None),
                export_date=utils.timestamp_to_datetime(getattr(action, "can_export_at", None)),
                transfer_star_count=getattr(action, "transfer_stars", None),
                client=client
            )

    async def toggle(self, is_saved: bool) -> bool:
        """Bound method *toggle* of :obj:`~pyrogram.types.ReceivedGift`.

        Use as a shortcut for:

        .. code-block:: python

            await client.toggle_gift_is_saved(
                message_id=message_id
            )

        Parameters:
            is_saved (``bool``):
                Pass True to display the gift on the user's profile page; pass False to remove it from the profile page.

        Example:
            .. code-block:: python

                await received_gift.toggle(is_saved=False)

        Returns:
            ``bool``: On success, True is returned.

        """
        return await self._client.toggle_gift_is_saved(
            message_id=self.message_id,
            is_saved=is_saved
        )
