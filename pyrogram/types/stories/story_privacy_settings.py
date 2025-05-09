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
from pyrogram import raw, types, utils

from ..object import Object


class StoryPrivacySettings(Object):
    """This object describes privacy settings of a story.

    Currently, it can be one of:

    - :obj:`~pyrogram.types.StoryPrivacySettingsEveryone`
    - :obj:`~pyrogram.types.StoryPrivacySettingsContacts`
    - :obj:`~pyrogram.types.StoryPrivacySettingsCloseFriends`
    - :obj:`~pyrogram.types.StoryPrivacySettingsSelectedUsers`

    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        privacy_rules: list["raw.base.PrivacyRule"],
    ) -> "StoryPrivacySettings":
        ko = []
        for priv in privacy_rules:
            # privacyValueDisallowContacts#f888fa1a = PrivacyRule;
            # privacyValueDisallowAll#8b73e763 = PrivacyRule;
            # privacyValueDisallowUsers#e4621141 users:Vector<long> = PrivacyRule;
            # privacyValueDisallowChatParticipants#41c87565 chats:Vector<long> = PrivacyRule;
            # privacyValueAllowPremium#ece9814b = PrivacyRule;
            # privacyValueAllowBots#21461b5d = PrivacyRule;
            # privacyValueDisallowBots#f6a5f82f = PrivacyRule;
            if isinstance(priv, raw.types.PrivacyValueAllowAll):
                ko.append(types.StoryPrivacySettingsEveryone())
            if isinstance(priv, raw.types.PrivacyValueDisallowUsers):
                if types.StoryPrivacySettingsEveryone in ko:
                    ko.append(types.StoryPrivacySettingsEveryone(except_user_ids=priv.users))
                if types.StoryPrivacySettingsContacts in ko:
                    ko.append(types.StoryPrivacySettingsContacts(except_user_ids=priv.users))
            if isinstance(priv, raw.types.PrivacyValueAllowContacts):
                ko.append(types.StoryPrivacySettingsContacts())
            if isinstance(priv, raw.types.PrivacyValueAllowCloseFriends):
                ko.append(types.StoryPrivacySettingsCloseFriends())
            if isinstance(priv, raw.types.PrivacyValueAllowUsers):
                ko.append(types.StoryPrivacySettingsSelectedUsers(user_ids=priv.users))
            if isinstance(priv, raw.types.PrivacyValueAllowChatParticipants):
                ko.append(types.StoryPrivacySettingsSelectedUsers(user_ids=[utils.get_channel_id(chat_id) for chat_id in priv.chats]))
        return ko[-1] if len(ko) > 0 else None
