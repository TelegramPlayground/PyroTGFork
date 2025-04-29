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

from .alternative_video import AlternativeVideo
from .animation import Animation
from .audio import Audio
from .chat_boost_added import ChatBoostAdded
from .contact import Contact
from .contact_registered import ContactRegistered
from .dice import Dice
from .document import Document
from .game import Game
from .gift import Gift
from .gift_code import GiftCode
from .gifted_premium import GiftedPremium
from .gifted_stars import GiftedStars
from .giveaway import Giveaway
from .giveaway_completed import GiveawayCompleted
from .giveaway_created import GiveawayCreated
from .giveaway_winners import GiveawayWinners
from .location import Location
from .message import Message
from .message_auto_delete_timer_changed import MessageAutoDeleteTimerChanged
from .message_effect import MessageEffect
from .message_entity import MessageEntity
from .message_reaction_count_updated import MessageReactionCountUpdated
from .message_reaction_updated import MessageReactionUpdated
from .message_reactions import MessageReactions
from .paid_message_price_changed import PaidMessagePriceChanged
from .paid_messages_refunded import PaidMessagesRefunded
from .payment_form import PaymentForm
from .photo import Photo
from .poll import Poll
from .poll_answer import PollAnswer
from .poll_option import PollOption
from .reaction import (
    Reaction,
    ReactionCount,
    ReactionType,
    ReactionTypeCustomEmoji,
    ReactionTypeEmoji,
    ReactionTypePaid,
)
from .received_gift import ReceivedGift
from .screenshot_taken import ScreenshotTaken
from .sponsored_message import SponsoredMessage
from .sticker import Sticker
from .story import Story
from .stripped_thumbnail import StrippedThumbnail
from .thumbnail import Thumbnail
from .translated_text import TranslatedText
from .upgraded_gift import UpgradedGift
from .venue import Venue
from .video import Video
from .video_note import VideoNote
from .voice import Voice
from .web_app_data import WebAppData
from .web_page import WebPage
from .write_access_allowed import WriteAccessAllowed

__all__ = [
    "AlternativeVideo",
    "Animation",
    "Audio",
    "ChatBoostAdded",
    "Contact",
    "ContactRegistered",
    "Dice",
    "Document",
    "Game",
    "Gift",
    "GiftCode",
    "GiftedPremium",
    "GiftedStars",
    "Giveaway",
    "GiveawayCompleted",
    "GiveawayCreated",
    "GiveawayWinners",
    "Location",
    "Message",  # TODO
    "MessageAutoDeleteTimerChanged",
    "MessageEffect",
    "MessageEntity",
    "MessageReactionCountUpdated",
    "MessageReactionUpdated",
    "MessageReactions",
    "PaidMessagePriceChanged",
    "PaidMessagesRefunded",
    "PaymentForm",
    "Photo",
    "Poll",
    "PollAnswer",
    "PollOption",
    "Reaction",
    "ReactionCount",
    "ReactionType",
    "ReactionTypeCustomEmoji",
    "ReactionTypeEmoji",
    "ReactionTypePaid",
    "ReceivedGift",
    "ScreenshotTaken",
    "SponsoredMessage",
    "Sticker",
    "Story",
    "StrippedThumbnail",
    "Thumbnail",
    "TranslatedText",
    "UpgradedGift",
    "Venue",
    "Video",
    "VideoNote",
    "Voice",
    "WebAppData",
    "WebPage",
    "WriteAccessAllowed",
]
