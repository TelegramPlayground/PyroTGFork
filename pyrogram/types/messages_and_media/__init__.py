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

from .animation import Animation
from .audio import Audio
from .contact import Contact
from .contact_registered import ContactRegistered
from .dice import Dice
from .direct_messages_topic import DirectMessagesTopic
from .document import Document
from .game import Game
from .location import ChatLocation, Location
from .message import Message
from .message_entity import MessageEntity
from .photo import Photo
from .poll import Poll
from .poll_answer import PollAnswer
from .poll_option import PollOption
from .reaction import (
    Reaction,
    ReactionType,
    ReactionTypeEmoji,
    ReactionTypeCustomEmoji,
    ReactionTypePaid,
    ReactionCount
)
from .sponsored_message import SponsoredMessage
from .gift import Gift
from .upgraded_gift import UpgradedGift
from .sticker import Sticker
from .stripped_thumbnail import StrippedThumbnail
from .thumbnail import Thumbnail
from .venue import Venue
from .video import Video
from .video_quality import VideoQuality
from .video_note import VideoNote
from .voice import Voice
from .web_app_data import WebAppData
from .web_page import WebPage
from .message_reactions import MessageReactions
from .message_reaction_updated import MessageReactionUpdated
from .message_reaction_count_updated import MessageReactionCountUpdated
from .chat_boost_added import ChatBoostAdded
from .payment_form import PaymentForm
from .giveaway import Giveaway
from .giveaway_created import GiveawayCreated
from .giveaway_completed import GiveawayCompleted
from .giveaway_winners import GiveawayWinners
from .gift_code import GiftCode
from .gifted_premium import GiftedPremium
from .gifted_stars import GiftedStars
from .message_effect import MessageEffect
from .screenshot_taken import ScreenshotTaken
from .formatted_text import FormattedText
from .message_auto_delete_timer_changed import MessageAutoDeleteTimerChanged
from .write_access_allowed import WriteAccessAllowed
from .paid_message_price_changed import PaidMessagePriceChanged
from .paid_messages_refunded import PaidMessagesRefunded
from .checklist import Checklist
from .checklist_task import ChecklistTask
from .checklist_tasks_added import ChecklistTasksAdded
from .checklist_tasks_done import ChecklistTasksDone
from .direct_message_price_changed import DirectMessagePriceChanged
from .chat_owner_left import ChatOwnerLeft
from .chat_owner_changed import ChatOwnerChanged
from .chat_has_protected_content_toggled import ChatHasProtectedContentToggled
from .chat_has_protected_content_disable_requested import ChatHasProtectedContentDisableRequested
from .poll_option_added import PollOptionAdded
from .poll_option_deleted import PollOptionDeleted

__all__ = [
    "Animation",
    "Audio",
    "ChatBoostAdded",
    "Contact",
    "ContactRegistered",
    "Dice",
    "Document",
    "Game",
    "PaymentForm",
    "GiftCode",
    "GiftedPremium",
    "GiftedStars",
    "Giveaway",
    "GiveawayCreated",
    "GiveawayCompleted",
    "GiveawayWinners",
    "ChatLocation",
    "Location",
    "Message",  # TODO
    "MessageAutoDeleteTimerChanged",
    "MessageEffect",
    "MessageEntity",
    "MessageReactionCountUpdated",
    "MessageReactionUpdated",
    "MessageReactions",
    "Photo",
    "Reaction",
    "ReactionCount",
    "ReactionType",
    "ReactionTypeEmoji",
    "ReactionTypeCustomEmoji",
    "ReactionTypePaid",
    "Thumbnail",
    "StrippedThumbnail",
    "Poll",
    "PollAnswer",
    "PollOption",
    "SponsoredMessage",
    "Gift",
    "UpgradedGift",
    "Sticker",
    "Venue",
    "Video",
    "VideoNote",
    "VideoQuality",
    "Voice",
    "WebAppData",
    "WebPage",
    "WriteAccessAllowed",
    "ScreenshotTaken",
    "FormattedText",
    "PaidMessagePriceChanged",
    "PaidMessagesRefunded",
    "Checklist",
    "ChecklistTask",
    "ChecklistTasksAdded",
    "ChecklistTasksDone",
    "DirectMessagePriceChanged",
    "DirectMessagesTopic",
    "ChatOwnerLeft",
    "ChatOwnerChanged",
    "ChatHasProtectedContentToggled",
    "ChatHasProtectedContentDisableRequested",
    "PollOptionAdded",
    "PollOptionDeleted",
]
