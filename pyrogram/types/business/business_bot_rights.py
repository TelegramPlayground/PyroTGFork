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

import pyrogram
from pyrogram import raw

from ..object import Object


class BusinessBotRights(Object):
    """TODO.

    Parameters:
        can_reply (``bool``):
            True, if the bot can act on behalf of the business account in chats that were active in the last 24 hours.

        can_read_messages (``bool``):

        can_delete_sent_messages (``bool``):

        can_delete_all_messages (``bool``):

        can_edit_name (``bool``):

        can_edit_bio (``bool``):

        can_edit_profile_photo (``bool``):
        can_edit_username (``bool``):
        can_view_gifts_and_stars (``bool``):
        can_convert_gifts_to_stars (``bool``):
        can_change_gift_settings (``bool``):
        can_transfer_and_upgrade_gifts (``bool``):
        can_transfer_stars (``bool``):
        can_manage_stories (``bool``):

    """

    def __init__(
        self,
        *,
        can_reply: bool = None,
        can_read_messages: bool = None,
        can_delete_sent_messages: bool = None,
        can_delete_all_messages: bool = None,
        can_edit_name: bool = None,
        can_edit_bio: bool = None,
        can_edit_profile_photo: bool = None,
        can_edit_username: bool = None,
        can_view_gifts_and_stars: bool = None,
        can_convert_gifts_to_stars: bool = None,
        can_change_gift_settings: bool = None,
        can_transfer_and_upgrade_gifts: bool = None,
        can_transfer_stars: bool = None,
        can_manage_stories: bool = None,
    ):
        super().__init__()

        self.can_reply = can_reply
        self.can_read_messages = can_read_messages
        self.can_delete_sent_messages = can_delete_sent_messages
        self.can_delete_all_messages = can_delete_all_messages
        self.can_edit_name = can_edit_name
        self.can_edit_bio = can_edit_bio
        self.can_edit_profile_photo = can_edit_profile_photo
        self.can_edit_username = can_edit_username
        self.can_view_gifts_and_stars = can_view_gifts_and_stars
        self.can_convert_gifts_to_stars = can_convert_gifts_to_stars
        self.can_change_gift_settings = can_change_gift_settings
        self.can_transfer_and_upgrade_gifts = can_transfer_and_upgrade_gifts
        self.can_transfer_stars = can_transfer_stars
        self.can_manage_stories = can_manage_stories


    @staticmethod
    def _parse(
        client,
        business_bot_rights: "raw.types.BusinessBotRights"
    ) -> "BusinessBotRights":
        if not business_bot_rights:
            return None
        return BusinessBotRights(
            can_reply=business_bot_rights.reply,
            can_read_messages=business_bot_rights.read_messages,
            can_delete_sent_messages=business_bot_rights.delete_sent_messages,
            can_delete_all_messages=business_bot_rights.delete_received_messages,
            can_edit_name=business_bot_rights.edit_name,
            can_edit_bio=business_bot_rights.edit_bio,
            can_edit_profile_photo=business_bot_rights.edit_profile_photo,
            can_edit_username=business_bot_rights.edit_username,
            can_view_gifts_and_stars=business_bot_rights.view_gifts,
            can_convert_gifts_to_stars=business_bot_rights.sell_gifts,
            can_change_gift_settings=business_bot_rights.change_gift_settings,
            can_transfer_and_upgrade_gifts=business_bot_rights.transfer_and_upgrade_gifts,
            can_transfer_stars=business_bot_rights.transfer_stars,
            can_manage_stories=business_bot_rights.manage_stories,
        )
