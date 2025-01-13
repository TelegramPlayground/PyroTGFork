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


class GroupCallParticipant(Object):
    """Represents a group call participant

    Parameters:
        participant (:obj:`~pyrogram.types.Chat`, *optional*):
            Identifier of the group call participant

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date when this participant join this group call.

        active_date (:py:obj:`~datetime.datetime`, *optional*):
            Date when this participant last active in this group call.
        
        volume_level (``int``, *optional*):
            Participant's volume level, if not set the volume is set to 100%.

        can_unmute_self (``bool``, *optional*):
            True, if the participant is muted for all users, but can unmute themselves

        is_muted_for_all_users (``bool``, *optional*):
            True, if the participant is muted for all users

        is_current_user (``bool``, *optional*):
            True, if the participant is the current user

        is_left (``bool``, *optional*):
            Whether the participant has left.

        is_just_joined (``bool``, *optional*):
            Whether the participant has just joined.

        is_muted_by_you (``bool``, *optional*):
            Whether this participant was muted by the current user.

        is_volume_by_admin (``bool``, *optional*):
            Whether our volume can only changed by an admin.

        is_video_joined (``bool``, *optional*):
            Whether this participant is currently broadcasting video.

        is_hand_raised (``bool``, *optional*):
            True, if the participant hand is raised

        is_video_enabled (``bool``, *optional*):
            Whether this participant is currently broadcasting video.

        is_screen_sharing_enabled (``bool``, *optional*):
            Whether this participant is currently shared screen.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        participant: "types.Chat" = None,
        date: datetime = None,
        active_date: datetime = None,
        volume_level: int = None,
        can_unmute_self: bool = None,
        is_muted_for_all_users: bool = None,
        is_current_user: bool = None,
        is_left: bool = None,
        is_just_joined: bool = None,
        is_muted_by_you: bool = None,
        is_volume_by_admin: bool = None,
        is_video_joined: bool = None,
        is_hand_raised: bool = None,
        is_video_enabled: bool = None,
        is_screen_sharing_enabled: bool = None,
        _raw: "raw.types.GroupCallParticipant" = None
    ):
        super().__init__(client)

        self.participant = participant
        self.date = date
        self.active_date = active_date
        self.volume_level = volume_level
        self.can_unmute_self = can_unmute_self
        self.is_muted_for_all_users = is_muted_for_all_users
        self.is_current_user = is_current_user
        self.is_left = is_left
        self.is_just_joined = is_just_joined
        self.is_muted_by_you = is_muted_by_you
        self.is_volume_by_admin = is_volume_by_admin
        self.is_video_joined = is_video_joined
        self.is_hand_raised = is_hand_raised
        self.is_video_enabled = is_video_enabled
        self.is_screen_sharing_enabled = is_screen_sharing_enabled
        self._raw = _raw

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        participant: "raw.types.GroupCallParticipant",
        users: dict[int, "raw.base.User"],
        chats: dict[int, "raw.base.Chat"]
    ) -> "GroupCallParticipant":
        peer = participant.peer
        peer_id = utils.get_raw_peer_id(peer)

        parsed_chat = types.Chat._parse_chat(
            client,
            users[peer_id] if isinstance(peer, raw.types.PeerUser) else chats[peer_id],
        )

        parsed_chat.bio = getattr(participant, "about", None)

        return GroupCallParticipant(
            participant=parsed_chat,
            date=utils.timestamp_to_datetime(participant.date),
            active_date=utils.timestamp_to_datetime(participant.active_date),
            volume_level=getattr(participant, "volume", None),
            can_unmute_self=participant.can_self_unmute,
            is_muted_for_all_users=participant.muted,
            is_current_user=participant.is_self,
            is_left=participant.left,
            is_just_joined=participant.just_joined,
            is_muted_by_you=participant.muted_by_you,
            is_volume_by_admin=participant.volume_by_admin,
            is_video_joined=participant.video_joined,
            is_hand_raised=bool(getattr(participant, "raise_hand_rating", None)),
            is_video_enabled=bool(getattr(participant, "video", None)),
            is_screen_sharing_enabled=bool(getattr(participant, "presentation", None)),
            _raw=participant,
            client=client
        )
