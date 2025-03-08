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

import io
import logging
import re
from datetime import datetime
from functools import partial
from typing import Union, Optional, Callable

import pyrogram
from pyrogram import raw, enums, types, utils
from pyrogram.errors import MessageIdsEmpty, PeerIdInvalid
from pyrogram.parser import utils as parser_utils, Parser
from ..object import Object
from ..update import Update

log = logging.getLogger(__name__)


class Str(str):
    def __init__(self, *args):
        super().__init__()

        self.entities: Optional[list["types.MessageEntity"]] = None

    def init(self, entities):
        self.entities = entities

        return self

    @property
    def markdown(self):
        return Parser.unparse(self, self.entities, False)

    @property
    def html(self):
        return Parser.unparse(self, self.entities, True)

    def __getitem__(self, item):
        return parser_utils.remove_surrogates(parser_utils.add_surrogates(self)[item])


class Message(Object, Update):
    """A message.

    Parameters:
        id (``int``):
            Unique message identifier inside this chat.

        message_thread_id (``int``, *optional*):
            Unique identifier of a message thread to which the message belongs; for supergroups only

        from_user (:obj:`~pyrogram.types.User`, *optional*):
            Sender, empty for messages sent to channels.

        sender_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Sender of the message, sent on behalf of a chat.
            The channel itself for channel messages.
            The supergroup itself for messages from anonymous group administrators.
            The linked channel for messages automatically forwarded to the discussion group.

        sender_boost_count (``int``, *optional*):
            If the sender of the message boosted the chat, the number of boosts added by the user.

        sender_business_bot (:obj:`~pyrogram.types.User`, *optional*):
            The bot that actually sent the message on behalf of the business account. Available only for outgoing messages sent on behalf of the connected business account.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the message was sent.

        business_connection_id (``str``, *optional*):
            Unique identifier of the business connection from which the message was received.
            If non-empty, the message belongs to a chat of the corresponding business account that is independent from any potential bot chat which might share the same identifier.
            This update may at times be triggered by unavailable changes to message fields that are either unavailable or not actively used by the current bot.

        chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Conversation the message belongs to.

        forward_origin (:obj:`~pyrogram.types.MessageOrigin`, *optional*):
            Information about the original message for forwarded messages

        is_topic_message (``bool``, *optional*):
            True, if the message is sent to a forum topic.

        is_automatic_forward (``bool``, *optional*):
            True, if the message is a channel post that was automatically forwarded to the connected discussion group.

        reply_to_message_id (``int``, *optional*):
            The id of the message which this message directly replied to.

        reply_to_message (:obj:`~pyrogram.types.Message`, *optional*):
            For replies, the original message. Note that the Message object in this field will not contain
            further reply_to_message fields even if it itself is a reply.

        external_reply (:obj:`~pyrogram.types.ExternalReplyInfo`, *optional*):
            Information about the message that is being replied to, which may come from another chat or forum topic

        quote (:obj:`~pyrogram.types.TextQuote`, *optional*):
            For replies that quote part of the original message, the quoted part of the message

        reply_to_story (:obj:`~pyrogram.types.Story`, *optional*):
            For replies to a story, the original story

        via_bot (:obj:`~pyrogram.types.User`):
            The information of the bot that generated the message from an inline query of a user.

        edit_date (:py:obj:`~datetime.datetime`, *optional*):
            Date the message was last edited.

        has_protected_content (``bool``, *optional*):
            True, if the message can't be forwarded.

        is_from_offline (``bool``, *optional*):
            True, if the message was sent by an implicit action, for example, as an away or a greeting business message, or as a scheduled message

        media_group_id (``str``, *optional*):
            The unique identifier of a media message group this message belongs to.

        author_signature (``str``, *optional*):
            Signature of the post author for messages in channels, or the custom title of an anonymous group
            administrator.

        text (``str``, *optional*):
            For text messages, the actual UTF-8 text of the message, 0-4096 characters.
            If the message contains entities (bold, italic, ...) you can access *text.markdown* or
            *text.html* to get the marked up message text. In case there is no entity, the fields
            will contain the same text as *text*.

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text.

        link_preview_options (:obj:`~pyrogram.types.LinkPreviewOptions`, *optional*):
            Options used for link preview generation for the message, if it is a text message and link preview options were changed

        effect_id (``str``, *optional*):
            Unique identifier of the message effect added to the message. Use :meth:`~pyrogram.Client.get_message_effects` to get the list of available message effect ids.

        animation (:obj:`~pyrogram.types.Animation`, *optional*):
            Message is an animation, information about the animation.

        audio (:obj:`~pyrogram.types.Audio`, *optional*):
            Message is an audio file, information about the file.

        document (:obj:`~pyrogram.types.Document`, *optional*):
            Message is a general file, information about the file.

        paid_media (:obj:`~pyrogram.types.PaidMediaInfo`, *optional*):
            Message contains paid media; information about the paid media.

        photo (:obj:`~pyrogram.types.Photo`, *optional*):
            Message is a photo, information about the photo.

        sticker (:obj:`~pyrogram.types.Sticker`, *optional*):
            Message is a sticker, information about the sticker.

        story (:obj:`~pyrogram.types.Story`, *optional*):
            Message might be a forwarded story.

        video (:obj:`~pyrogram.types.Video`, *optional*):
            Message is a video, information about the video.

        alternative_videos (List of :obj:`~pyrogram.types.AlternativeVideo`, *optional*):
            Alternative qualities of the video, if the message is a video.

        video_note (:obj:`~pyrogram.types.VideoNote`, *optional*):
            Message is a video note, information about the video message.

        voice (:obj:`~pyrogram.types.Voice`, *optional*):
            Message is a voice message, information about the file.

        caption (``str``, *optional*):
            Caption for the audio, document, photo, video or voice, 0-1024 characters.
            If the message contains caption entities (bold, italic, ...) you can access *caption.markdown* or
            *caption.html* to get the marked up caption text. In case there is no caption entity, the fields
            will contain the same text as *caption*.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For messages with a caption, special entities like usernames, URLs, bot commands, etc. that appear
            in the caption.

        show_caption_above_media (``bool``, *optional*):
            True, if the caption must be shown above the message media.

        has_media_spoiler (``bool``, *optional*):
            True, if the message media is covered by a spoiler animation.

        contact (:obj:`~pyrogram.types.Contact`, *optional*):
            Message is a shared contact, information about the contact.

        dice (:obj:`~pyrogram.types.Dice`, *optional*):
            A dice containing a value that is randomly generated by Telegram.

        game (:obj:`~pyrogram.types.Game`, *optional*):
            Message is a game, information about the game.

        poll (:obj:`~pyrogram.types.Poll`, *optional*):
            Message is a native poll, information about the poll.

        venue (:obj:`~pyrogram.types.Venue`, *optional*):
            Message is a venue, information about the venue.

        location (:obj:`~pyrogram.types.Location`, *optional*):
            Message is a shared location, information about the location.

        new_chat_members (List of :obj:`~pyrogram.types.User`, *optional*):
            New members that were added to the group or supergroup and information about them
            (the bot itself may be one of these members).

        left_chat_member (:obj:`~pyrogram.types.User`, *optional*):
            A member was removed from the group, information about them (this member may be the bot itself).

        new_chat_title (``str``, *optional*):
            A chat title was changed to this value.

        new_chat_photo (:obj:`~pyrogram.types.Photo`, *optional*):
            A chat photo was change to this value.

        delete_chat_photo (``bool``, *optional*):
            Service message: the chat photo was deleted.

        group_chat_created (``bool``, *optional*):
            Service message: the group has been created.

        supergroup_chat_created (``bool``, *optional*):
            Service message: the supergroup has been created.
            This field can't be received in a message coming through updates, because bot can't be a member of a
            supergroup when it is created. It can only be found in reply_to_message if someone replies to a very
            first message in a directly created supergroup.

        channel_chat_created (``bool``, *optional*):
            Service message: the channel has been created.
            This field can't be received in a message coming through updates, because bot can't be a member of a
            channel when it is created. It can only be found in reply_to_message if someone replies to a very
            first message in a channel.

        message_auto_delete_timer_changed (:obj:`~pyrogram.types.MessageAutoDeleteTimerChanged`, *optional*):
            Service message: auto-delete timer settings changed in the chat.

        migrate_to_chat_id (``int``, *optional*):
            The group has been migrated to a supergroup with the specified identifier.
            This number may be greater than 32 bits and some programming languages may have difficulty/silent defects
            in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float
            type are safe for storing this identifier.

        migrate_from_chat_id (``int``, *optional*):
            The supergroup has been migrated from a group with the specified identifier.
            This number may be greater than 32 bits and some programming languages may have difficulty/silent defects
            in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float
            type are safe for storing this identifier.

        pinned_message (:obj:`~pyrogram.types.Message`, *optional*):
            Specified message was pinned.
            Note that the Message object in this field will not contain further reply_to_message fields even if it
            is itself a reply.

        invoice (:obj:`~pyrogram.types.Invoice`, *optional*):
            Message is an invoice for a `payment <https://core.telegram.org/bots/api#payments>`_, information about the invoice. `More about payments » <https://core.telegram.org/bots/api#payments>`_

        successful_payment (:obj:`~pyrogram.types.SuccessfulPayment`, *optional*):
            Message is a service message about a successful payment, information about the payment. `More about payments <https://core.telegram.org/bots/api#payments>`_

        refunded_payment (:obj:`~pyrogram.types.RefundedPayment`, *optional*):
            Message is a service message about a refunded payment, information about the payment. `More about payments <https://core.telegram.org/bots/api#payments>`_

        users_shared (:obj:`~pyrogram.types.UsersShared`, *optional*):
            Service message: users were shared with the bot

        chat_shared (:obj:`~pyrogram.types.ChatShared`, *optional*):
            Service message: a chat was shared with the bot

        connected_website (``str``, *optional*):
            The domain name of the website on which the user has logged in. `More about Telegram Login <https://core.telegram.org/widgets/login>`__

        write_access_allowed (:obj:`~pyrogram.types.WriteAccessAllowed`, *optional*):
            Service message: the user allowed the bot to write messages after adding it to the attachment or side menu, launching a Web App from a link, or accepting an explicit request from a Web App sent by the method `requestWriteAccess <https://core.telegram.org/bots/webapps#initializing-mini-apps>`__

        boost_added (:obj:`~pyrogram.types.ChatBoostAdded`, *optional*):
            Service message: user boosted the chat

        forum_topic_created (:obj:`~pyrogram.types.ForumTopicCreated`, *optional*):
            Service message: forum topic created

        forum_topic_edited (:obj:`~pyrogram.types.ForumTopicEdited`, *optional*):
            Service message: forum topic edited

        forum_topic_closed (:obj:`~pyrogram.types.ForumTopicClosed`, *optional*):
            Service message: forum topic closed

        forum_topic_reopened (:obj:`~pyrogram.types.ForumTopicReopened`, *optional*):
            Service message: forum topic reopened

        general_forum_topic_hidden (:obj:`~pyrogram.types.GeneralForumTopicHidden`, *optional*):
            Service message: the 'General' forum topic hidden

        general_forum_topic_unhidden (:obj:`~pyrogram.types.GeneralForumTopicUnhidden`, *optional*):
            Service message: the 'General' forum topic unhidden

        giveaway_created (:obj:`~pyrogram.types.GiveawayCreated`, *optional*):
            Service message: a scheduled giveaway was created

        giveaway (:obj:`~pyrogram.types.Giveaway`, *optional*):
            The message is a scheduled giveaway message

        giveaway_winners (:obj:`~pyrogram.types.GiveawayWinners`, *optional*):
            A giveaway with public winners was completed        

        giveaway_completed (:obj:`~pyrogram.types.GiveawayCompleted`, *optional*):
            Service message: a giveaway without public winners was completed

        video_chat_scheduled (:obj:`~pyrogram.types.VideoChatScheduled`, *optional*):
            Service message: voice chat scheduled.

        video_chat_started (:obj:`~pyrogram.types.VideoChatStarted`, *optional*):
            Service message: the voice chat started.

        video_chat_ended (:obj:`~pyrogram.types.VideoChatEnded`, *optional*):
            Service message: the voice chat has ended.

        video_chat_participants_invited (:obj:`~pyrogram.types.VideoChatParticipantsInvited`, *optional*):
            Service message: new members were invited to the voice chat.

        web_app_data (:obj:`~pyrogram.types.WebAppData`, *optional*):
            Service message: web app data sent to the bot.

        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
            Additional interface options. An object for an inline keyboard, custom reply keyboard,
            instructions to remove reply keyboard or to force a reply from the user.

        empty (``bool``, *optional*):
            The message is empty.
            A message can be empty in case it was deleted or you tried to retrieve a message that doesn't exist yet.

        mentioned (``bool``, *optional*):
            The message contains a mention.

        service (:obj:`~pyrogram.enums.MessageServiceType`, *optional*):
            The message is a service message.
            This field will contain the enumeration type of the service message.
            You can use ``service = getattr(message, message.service.value)`` to access the service message.

        media (:obj:`~pyrogram.enums.MessageMediaType`, *optional*):
            The message is a media message.
            This field will contain the enumeration type of the media message.
            You can use ``media = getattr(message, message.media.value)`` to access the media message.

        web_page (:obj:`~pyrogram.types.WebPage`, *optional*):
            Message was sent with a webpage preview.

        game_high_score (:obj:`~pyrogram.types.GameHighScore`, *optional*):
            The game score for a user.
            The reply_to_message field will contain the game Message.

        views (``int``, *optional*):
            View counter for channel posts.

	    forwards (``int``, *optional*):
            Forward counter for channel posts.

        outgoing (``bool``, *optional*):
            Whether the message is incoming or outgoing.
            Messages received from other chats are incoming (*outgoing* is False).
            Messages sent from yourself to other chats are outgoing (*outgoing* is True).
            An exception is made for your own personal chat; messages sent there will be incoming.

        matches (List of regex Matches, *optional*):
            A list containing all `Match Objects <https://docs.python.org/3/library/re.html#match-objects>`_ that match
            the text of this message. Only applicable when using :obj:`Filters.regex <pyrogram.Filters.regex>`.

        command (List of ``str``, *optional*):
            A list containing the command and its arguments, if any.
            E.g.: "/start 1 2 3" would produce ["start", "1", "2", "3"].
            Only applicable when using :obj:`~pyrogram.filters.command`.

        reactions (List of :obj:`~pyrogram.types.Reaction`):
            List of the reactions to this message.

        custom_action (``str``, *optional*):
            Custom action (most likely not supported by the current layer, an upgrade might be needed)

        gift_code (:obj:`~pyrogram.types.GiftCode`, *optional*):
            Service message: gift code information.
            Contains a `Telegram Premium giftcode link <https://core.telegram.org/api/links#premium-giftcode-links>`_.

        gifted_premium (:obj:`~pyrogram.types.GiftedPremium`, *optional*):
            Info about a gifted Telegram Premium subscription

        gifted_stars (:obj:`~pyrogram.types.GiftedStars`, *optional*):
            Info about gifted Telegram Stars

        received_gift (:obj:`~pyrogram.types.ReceivedGift`, *optional*):
            Service message: Represents a gift received by a user.

        contact_registered (:obj:`~pyrogram.types.ContactRegistered`, *optional*):
            A service message that a contact has registered with Telegram.

        chat_join_type (:obj:`~pyrogram.enums.ChatJoinType`, *optional*):
            The message is a service message of the type :obj:`~pyrogram.enums.MessageServiceType.NEW_CHAT_MEMBERS`.
            This field will contain the enumeration type of how the user had joined the chat.

        screenshot_taken (:obj:`~pyrogram.types.ScreenshotTaken`, *optional*):
            A service message that a screenshot of a message in the chat has been taken.

        paid_message_star_count (``int``, *optional*):
            The number of Telegram Stars the sender paid to send the message.

        link (``str``, *property*):
            Generate a link to this message, only for supergroups and channels. Can be None if the message cannot have a link.

        content (``str``, *property*):
            The text or caption content of the message.
            If the message contains entities (bold, italic, ...) you can access *content.markdown* or
            *content.html* to get the marked up content. In case there is no caption entity, the fields
            will contain the same text as *content*.

    """

    # TODO: Add game missing field.

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        message_thread_id: int = None,
        from_user: "types.User" = None,
        sender_chat: "types.Chat" = None,
        sender_boost_count: int = None,
        sender_business_bot: "types.User" = None,
        date: datetime = None,
        business_connection_id: str = None,
        chat: "types.Chat" = None,
        forward_origin: "types.MessageOrigin" = None,
        is_topic_message: bool = None,
        is_automatic_forward: bool = None,
        reply_to_message_id: int = None,
        reply_to_message: "Message" = None,
        external_reply: "types.ExternalReplyInfo" = None,
        quote: "types.TextQuote" = None,
        reply_to_story: "types.Story" = None,
        via_bot: "types.User" = None,
        edit_date: datetime = None,
        has_protected_content: bool = None,
        is_from_offline: bool = None,
        media_group_id: str = None,
        author_signature: str = None,
        text: Str = None,
        entities: list["types.MessageEntity"] = None,
        link_preview_options: "types.LinkPreviewOptions" = None,
        effect_id: str = None,
        animation: "types.Animation" = None,
        audio: "types.Audio" = None,
        document: "types.Document" = None,
        paid_media: "types.PaidMediaInfo" = None,
        photo: "types.Photo" = None,
        sticker: "types.Sticker" = None,
        story: "types.Story" = None,
        video: "types.Video" = None,
        alternative_videos: list["types.AlternativeVideo"] = None,
        video_note: "types.VideoNote" = None,
        voice: "types.Voice" = None,
        caption: Str = None,
        caption_entities: list["types.MessageEntity"] = None,
        show_caption_above_media: bool = None,
        has_media_spoiler: bool = None,
        contact: "types.Contact" = None,
        dice: "types.Dice" = None,
        game: "types.Game" = None,
        poll: "types.Poll" = None,
        venue: "types.Venue" = None,
        location: "types.Location" = None,
        new_chat_members: list["types.User"] = None,
        left_chat_member: "types.User" = None,
        new_chat_title: str = None,
        new_chat_photo: "types.Photo" = None,
        delete_chat_photo: bool = None,
        group_chat_created: bool = None,
        supergroup_chat_created: bool = None,
        channel_chat_created: bool = None,
        message_auto_delete_timer_changed: "types.MessageAutoDeleteTimerChanged" = None,
        migrate_to_chat_id: int = None,
        migrate_from_chat_id: int = None,
        pinned_message: "Message" = None,
        invoice: "types.Invoice" = None,
        successful_payment: "types.SuccessfulPayment" = None,
        refunded_payment: "types.RefundedPayment" = None,
        users_shared: "types.UsersShared" = None,
        chat_shared: "types.ChatShared" = None,
        connected_website: str = None,
        write_access_allowed: "types.WriteAccessAllowed" = None,


        boost_added: "types.ChatBoostAdded" = None,
        forum_topic_created: "types.ForumTopicCreated" = None,
        forum_topic_edited: "types.ForumTopicEdited" = None,
        forum_topic_closed: "types.ForumTopicClosed" = None,
        forum_topic_reopened: "types.ForumTopicReopened" = None,
        general_forum_topic_hidden: "types.GeneralForumTopicHidden" = None,
        general_forum_topic_unhidden: "types.GeneralForumTopicUnhidden" = None,
        giveaway_created: "types.GiveawayCreated" = None,
        giveaway: "types.Giveaway" = None,
        giveaway_winners: "types.GiveawayWinners" = None,
        giveaway_completed: "types.GiveawayCompleted" = None,
        video_chat_scheduled: "types.VideoChatScheduled" = None,
        video_chat_started: "types.VideoChatStarted" = None,
        video_chat_ended: "types.VideoChatEnded" = None,
        video_chat_participants_invited: "types.VideoChatParticipantsInvited" = None,
        web_app_data: "types.WebAppData" = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,

        gift_code: "types.GiftCode" = None,
        gifted_premium: "types.GiftedPremium" = None,
        gifted_stars: "types.GiftedStars" = None,
        received_gift: "types.ReceivedGift" = None,
        empty: bool = None,
        mentioned: bool = None,
        service: "enums.MessageServiceType" = None,
        scheduled: bool = None,
        from_scheduled: bool = None,
        media: "enums.MessageMediaType" = None,
        web_page: "types.WebPage" = None,
        game_high_score: int = None,
        views: int = None,
        forwards: int = None,
        outgoing: bool = None,
        matches: list[re.Match] = None,
        command: list[str] = None,
        reactions: list["types.Reaction"] = None,
        custom_action: str = None,
        contact_registered: "types.ContactRegistered" = None,
        chat_join_type: "enums.ChatJoinType" = None,
        screenshot_taken: "types.ScreenshotTaken" = None,
        paid_message_star_count: int = None,
        _raw = None
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.sender_chat = sender_chat
        self.date = date
        self.chat = chat
        self.forward_origin = forward_origin
        self.reply_to_message_id = reply_to_message_id
        self.message_thread_id = message_thread_id
        self.reply_to_message = reply_to_message
        self.mentioned = mentioned
        self.empty = empty
        self.service = service
        self.scheduled = scheduled
        self.from_scheduled = from_scheduled
        self.media = media
        self.edit_date = edit_date
        self.media_group_id = media_group_id
        self.author_signature = author_signature
        self.has_protected_content = has_protected_content
        self.is_from_offline = is_from_offline
        self.has_media_spoiler = has_media_spoiler
        self.text = text
        self.entities = entities
        self.caption_entities = caption_entities
        self.show_caption_above_media = show_caption_above_media
        self.audio = audio
        self.document = document
        self.photo = photo
        self.sticker = sticker
        self.animation = animation
        self.game = game
        self.video = video
        self.alternative_videos = alternative_videos
        self.voice = voice
        self.video_note = video_note
        self.caption = caption
        self.contact = contact
        self.location = location
        self.venue = venue
        self.web_page = web_page
        self.poll = poll
        self.dice = dice
        self.new_chat_members = new_chat_members
        self.left_chat_member = left_chat_member
        self.new_chat_title = new_chat_title
        self.new_chat_photo = new_chat_photo
        self.delete_chat_photo = delete_chat_photo
        self.group_chat_created = group_chat_created
        self.supergroup_chat_created = supergroup_chat_created
        self.channel_chat_created = channel_chat_created
        self.message_auto_delete_timer_changed = message_auto_delete_timer_changed
        self.migrate_to_chat_id = migrate_to_chat_id
        self.migrate_from_chat_id = migrate_from_chat_id
        self.pinned_message = pinned_message
        self.invoice = invoice
        self.game_high_score = game_high_score
        self.views = views
        self.forwards = forwards
        self.via_bot = via_bot
        self.outgoing = outgoing
        self.matches = matches
        self.command = command
        self.reply_markup = reply_markup
        self.video_chat_scheduled = video_chat_scheduled
        self.video_chat_started = video_chat_started
        self.video_chat_ended = video_chat_ended
        self.video_chat_participants_invited = video_chat_participants_invited
        self.web_app_data = web_app_data
        self.reactions = reactions
        self.link_preview_options = link_preview_options
        self.effect_id = effect_id
        self.external_reply = external_reply
        self.is_topic_message = is_topic_message
        self.is_automatic_forward = is_automatic_forward
        self.sender_boost_count = sender_boost_count
        self.boost_added = boost_added
        self.quote = quote
        self.story = story
        self.reply_to_story = reply_to_story
        self.giveaway = giveaway
        self.giveaway_created = giveaway_created
        self.users_shared = users_shared
        self.chat_shared = chat_shared
        self.connected_website = connected_website
        self.write_access_allowed = write_access_allowed
        self.giveaway_completed = giveaway_completed
        self.giveaway_winners = giveaway_winners
        self.gift_code = gift_code
        self.gifted_premium = gifted_premium
        self.gifted_stars = gifted_stars
        self.forum_topic_created = forum_topic_created
        self.forum_topic_edited = forum_topic_edited
        self.forum_topic_closed = forum_topic_closed
        self.forum_topic_reopened = forum_topic_reopened
        self.general_forum_topic_hidden = general_forum_topic_hidden
        self.general_forum_topic_unhidden = general_forum_topic_unhidden
        self.custom_action = custom_action
        self.sender_business_bot = sender_business_bot
        self.business_connection_id = business_connection_id
        self.received_gift = received_gift
        self.successful_payment = successful_payment
        self.paid_media = paid_media
        self.refunded_payment = refunded_payment
        self.contact_registered = contact_registered
        self.chat_join_type = chat_join_type
        self.screenshot_taken = screenshot_taken
        self.paid_message_star_count = paid_message_star_count
        self._raw = _raw

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        message: raw.base.Message,
        users: dict,
        chats: dict,
        is_scheduled: bool = False,
        replies: int = 1,
        business_connection_id: str = None,
        raw_reply_to_message: raw.base.Message = None
    ):
        peer_id = utils.get_raw_peer_id(message.peer_id)

        if isinstance(message, raw.types.MessageEmpty):
            sender_chat = None
            if peer_id:
                if isinstance(message.peer_id, raw.types.PeerUser):
                    sender_chat = types.Chat._parse_user_chat(client, users[peer_id])

                elif isinstance(message.peer_id, raw.types.PeerChat):
                    sender_chat = types.Chat._parse_chat_chat(client, chats[peer_id])

                else:
                    sender_chat = types.Chat._parse_channel_chat(client, chats[peer_id])

            return Message(
                id=message.id,
                empty=True,
                chat=sender_chat,
                business_connection_id=business_connection_id if business_connection_id else None,
                client=client,
                _raw=message
            )

        from_id = utils.get_raw_peer_id(message.from_id)
        user_id = from_id or peer_id

        if isinstance(message.from_id, raw.types.PeerUser) and isinstance(message.peer_id, raw.types.PeerUser):
            if from_id not in users or peer_id not in users:
                try:
                    r = await client.invoke(
                        raw.functions.users.GetUsers(
                            id=[
                                await client.resolve_peer(from_id),
                                await client.resolve_peer(peer_id)
                            ]
                        )
                    )
                except PeerIdInvalid:
                    pass
                else:
                    users.update({i.id: i for i in r})

        if isinstance(message, raw.types.MessageService):
            action = message.action

            chat = types.Chat._parse(client, message, users, chats, is_chat=True)
            from_user = types.User._parse(client, users.get(user_id, None))
            sender_chat = types.Chat._parse(client, message, users, chats, is_chat=False) if not from_user else None

            new_chat_members = None
            left_chat_member = None
            new_chat_title = None
            delete_chat_photo = None
            migrate_to_chat_id = None
            migrate_from_chat_id = None
            group_chat_created = None
            supergroup_chat_created = None
            channel_chat_created = None
            new_chat_photo = None
            video_chat_scheduled = None
            video_chat_started = None
            video_chat_ended = None
            video_chat_participants_invited = None
            web_app_data = None
            gift_code = None
            gifted_premium = None
            gifted_stars = None
            giveaway_created = None
            users_shared = None
            chat_shared = None
            connected_website = None
            write_access_allowed = None
            message_auto_delete_timer_changed = None
            boost_added = None
            giveaway_completed = None
            custom_action = None

            forum_topic_created = None
            forum_topic_edited = None
            forum_topic_closed = None
            forum_topic_reopened = None
            general_forum_topic_hidden = None
            general_forum_topic_unhidden = None
            successful_payment = None
            refunded_payment = None

            contact_registered = None
            chat_join_type = None
            screenshot_taken = None

            received_gift = None

            service_type = enums.MessageServiceType.UNKNOWN

            if isinstance(action, raw.types.MessageActionChatAddUser):
                new_chat_members = [types.User._parse(client, users[i]) for i in action.users]
                service_type = enums.MessageServiceType.NEW_CHAT_MEMBERS
                chat_join_type = enums.ChatJoinType.BY_ADD
            elif isinstance(action, raw.types.MessageActionChatJoinedByLink):
                new_chat_members = [types.User._parse(client, users[utils.get_raw_peer_id(message.from_id)])]
                service_type = enums.MessageServiceType.NEW_CHAT_MEMBERS
                chat_join_type = enums.ChatJoinType.BY_LINK
            elif isinstance(action, raw.types.MessageActionChatJoinedByRequest):
                new_chat_members = [types.User._parse(client, users[utils.get_raw_peer_id(message.from_id)])]
                service_type = enums.MessageServiceType.NEW_CHAT_MEMBERS
                chat_join_type = enums.ChatJoinType.BY_REQUEST
            elif isinstance(action, raw.types.MessageActionChatDeleteUser):
                left_chat_member = types.User._parse(client, users[action.user_id])
                service_type = enums.MessageServiceType.LEFT_CHAT_MEMBERS
            elif isinstance(action, raw.types.MessageActionChatEditTitle):
                new_chat_title = action.title
                service_type = enums.MessageServiceType.NEW_CHAT_TITLE
            elif isinstance(action, raw.types.MessageActionChatDeletePhoto):
                delete_chat_photo = True
                service_type = enums.MessageServiceType.DELETE_CHAT_PHOTO
            elif isinstance(action, raw.types.MessageActionChatMigrateTo):
                migrate_to_chat_id = action.channel_id
                service_type = enums.MessageServiceType.MIGRATE_TO_CHAT_ID
            elif isinstance(action, raw.types.MessageActionChannelMigrateFrom):
                migrate_from_chat_id = action.chat_id
                service_type = enums.MessageServiceType.MIGRATE_FROM_CHAT_ID
            elif isinstance(action, raw.types.MessageActionChatCreate):
                group_chat_created = True
                service_type = enums.MessageServiceType.GROUP_CHAT_CREATED
            elif isinstance(action, raw.types.MessageActionChannelCreate):
                if chat.type == enums.ChatType.SUPERGROUP:
                    supergroup_chat_created = True
                    service_type = enums.MessageServiceType.SUPERGROUP_CHAT_CREATED
                else:
                    channel_chat_created = True
                    service_type = enums.MessageServiceType.CHANNEL_CHAT_CREATED
            elif isinstance(action, raw.types.MessageActionChatEditPhoto):
                new_chat_photo = types.Photo._parse(client, action.photo)
                service_type = enums.MessageServiceType.NEW_CHAT_PHOTO
            elif isinstance(action, raw.types.MessageActionGroupCallScheduled):
                video_chat_scheduled = types.VideoChatScheduled._parse(action)
                service_type = enums.MessageServiceType.VIDEO_CHAT_SCHEDULED
            elif isinstance(action, raw.types.MessageActionGroupCall):
                if action.duration:
                    video_chat_ended = types.VideoChatEnded._parse(action)
                    service_type = enums.MessageServiceType.VIDEO_CHAT_ENDED
                else:
                    video_chat_started = types.VideoChatStarted()
                    service_type = enums.MessageServiceType.VIDEO_CHAT_STARTED
            elif isinstance(action, raw.types.MessageActionInviteToGroupCall):
                video_chat_participants_invited = types.VideoChatParticipantsInvited._parse(client, action, users)
                service_type = enums.MessageServiceType.VIDEO_CHAT_PARTICIPANTS_INVITED
            elif isinstance(action, raw.types.MessageActionWebViewDataSentMe):
                web_app_data = types.WebAppData._parse(action)
                service_type = enums.MessageServiceType.WEB_APP_DATA
            elif isinstance(action, raw.types.MessageActionGiveawayLaunch):
                giveaway_created = types.GiveawayCreated._parse(
                    client, action
                )
                service_type = enums.MessageServiceType.GIVEAWAY_CREATED
            elif isinstance(action, raw.types.MessageActionGiftCode):
                gift_code = types.GiftCode._parse(client, action, chats)
                service_type = enums.MessageServiceType.GIFT_CODE
            elif isinstance(action, raw.types.MessageActionGiftPremium):
                gifted_premium = await types.GiftedPremium._parse(client, action, from_user.id)
                service_type = enums.MessageServiceType.GIFTED_PREMIUM
            elif isinstance(action, raw.types.MessageActionGiftStars):
                gifted_stars = await types.GiftedStars._parse(client, action, from_user.id, chat.id)
                service_type = enums.MessageServiceType.GIFTED_STARS

            elif (
                isinstance(action, raw.types.MessageActionRequestedPeer) or
                isinstance(action, raw.types.MessageActionRequestedPeerSentMe)
            ):
                _requested_chats = []
                _requested_users = []

                for requested_peer in action.peers:
                    if isinstance(requested_peer, raw.types.RequestedPeerUser):
                        _requested_users.append(
                            types.Chat(
                                client=client,
                                id=requested_peer.user_id,
                                first_name=requested_peer.first_name,
                                last_name=requested_peer.last_name,
                                username=requested_peer.username,
                                photo=types.Photo._parse(
                                    client=client,
                                    photo=getattr(requested_peer, "photo", None)
                                )
                            )
                        )
                    elif isinstance(requested_peer, raw.types.RequestedPeerChat):
                        _requested_chats.append(
                            types.Chat(
                                client=client,
                                id=-requested_peer.chat_id,
                                title=requested_peer.title,
                                photo=types.Photo._parse(
                                    client=client,
                                    photo=getattr(requested_peer, "photo", None)
                                )
                            )
                        )
                    elif isinstance(requested_peer, raw.types.RequestedPeerChannel):
                        _requested_chats.append(
                            types.Chat(
                                client=client,
                                id=utils.get_channel_id(
                                    requested_peer.channel_id
                                ),
                                title=requested_peer.title,
                                username=requested_peer.username,
                                photo=types.Photo._parse(
                                    client=client,
                                    photo=getattr(requested_peer, "photo", None)
                                )
                            )
                        )
                    else:
                        raw_peer_id = utils.get_raw_peer_id(requested_peer)

                        if isinstance(requested_peer, raw.types.PeerUser):
                            _requested_users.append(
                                types.Chat._parse_user_chat(
                                    client,
                                    users.get(raw_peer_id, raw_peer_id)
                                )
                            )
                        elif isinstance(requested_peer, raw.types.PeerChat):
                            _requested_chats.append(
                                types.Chat._parse_chat_chat(
                                    client,
                                    chats.get(raw_peer_id, raw_peer_id)
                                )
                            )
                        else:
                            _requested_chats.append(
                                types.Chat._parse_channel_chat(
                                    client,
                                    chats.get(raw_peer_id, raw_peer_id)
                                )
                            )

                if _requested_users:
                    service_type = enums.MessageServiceType.USERS_SHARED
                    users_shared = types.UsersShared(
                        request_id=action.button_id,
                        users=types.List(_requested_users) or None
                    )
                if _requested_chats:
                    service_type = enums.MessageServiceType.CHAT_SHARED
                    chat_shared = types.ChatShared(
                        request_id=action.button_id,
                        chats=types.List(_requested_chats) or None
                    )

            elif isinstance(action, raw.types.MessageActionSetMessagesTTL):
                message_auto_delete_timer_changed = types.MessageAutoDeleteTimerChanged(
                    message_auto_delete_time=action.period
                )
                service_type = enums.MessageServiceType.MESSAGE_AUTO_DELETE_TIMER_CHANGED
                auto_setting_from = getattr(action, "auto_setting_from", None)
                if auto_setting_from:
                    message_auto_delete_timer_changed.from_user = types.User._parse(
                        client,
                        users[auto_setting_from]
                    )

            elif isinstance(action, raw.types.MessageActionBoostApply):
                service_type = enums.MessageServiceType.CHAT_BOOST_ADDED
                boost_added = types.ChatBoostAdded._parse(
                    action
                )

            elif isinstance(action, raw.types.MessageActionGiveawayResults):
                service_type = enums.MessageServiceType.GIVEAWAY_COMPLETED
                giveaway_completed = types.GiveawayCompleted._parse(
                    client,
                    action,
                    getattr(
                        getattr(
                            message,
                            "reply_to",
                            None
                        ),
                        "reply_to_msg_id",
                        None
                    )
                )

            elif isinstance(action, raw.types.MessageActionCustomAction):
                service_type = enums.MessageServiceType.CUSTOM_ACTION
                custom_action = action.message
            elif isinstance(action, raw.types.MessageActionContactSignUp):
                service_type = enums.MessageServiceType.CONTACT_REGISTERED
                contact_registered = types.ContactRegistered()
            elif isinstance(action, raw.types.MessageActionScreenshotTaken):
                service_type = enums.MessageServiceType.SCREENSHOT_TAKEN
                screenshot_taken = types.ScreenshotTaken()

            elif isinstance(action, raw.types.MessageActionTopicCreate):
                title = action.title
                icon_color = action.icon_color
                icon_emoji_id = getattr(action, "icon_emoji_id", None)
                service_type = enums.MessageServiceType.FORUM_TOPIC_CREATED
                forum_topic_created = types.ForumTopicCreated._parse(action)

            elif isinstance(action, (raw.types.MessageActionPaymentSent, raw.types.MessageActionPaymentSentMe)):
                successful_payment = types.SuccessfulPayment._parse(client, action)
                service_type = enums.MessageServiceType.SUCCESSFUL_PAYMENT
            
            elif isinstance(action, raw.types.MessageActionPaymentRefunded):
                refunded_payment = types.RefundedPayment._parse(client, action)
                service_type = enums.MessageServiceType.REFUNDED_PAYMENT

            elif isinstance(action, raw.types.MessageActionTopicEdit):
                title = getattr(action, "title", None)
                icon_emoji_id = getattr(action, "icon_emoji_id", None)
                closed = getattr(action, "closed", None)
                hidden = getattr(action, "hidden", None)

                if title:
                    forum_topic_edited = types.ForumTopicEdited._parse(action)
                    service_type = enums.MessageServiceType.FORUM_TOPIC_EDITED
                elif hidden in {True, False}:
                    if not bool(message.reply_to):
                        if action.hidden:
                            service_type = enums.MessageServiceType.GENERAL_FORUM_TOPIC_HIDDEN
                            general_forum_topic_hidden = types.GeneralForumTopicHidden()
                        else:
                            service_type = enums.MessageServiceType.GENERAL_FORUM_TOPIC_UNHIDDEN
                            general_forum_topic_unhidden = types.GeneralForumTopicUnhidden()
                    # else: # TODO
                elif closed in {True, False}:
                    if action.closed:
                        service_type = enums.MessageServiceType.FORUM_TOPIC_CLOSED
                        forum_topic_closed = types.ForumTopicClosed()
                    else:
                        service_type = enums.MessageServiceType.FORUM_TOPIC_REOPENED
                        forum_topic_reopened = types.ForumTopicReopened()

            elif isinstance(action, raw.types.MessageActionBotAllowed):
                connected_website = getattr(action, "domain", None)
                if connected_website:
                    service_type = enums.MessageServiceType.CONNECTED_WEBSITE
                else:
                    write_access_allowed = types.WriteAccessAllowed._parse(action)
                    service_type = enums.MessageServiceType.WRITE_ACCESS_ALLOWED

            elif (
                isinstance(action, raw.types.MessageActionStarGift) or
                isinstance(action, raw.types.MessageActionStarGiftUnique)
            ):
                received_gift = await types.ReceivedGift._parse_action(client, message, users, chats)
                service_type = enums.MessageServiceType.RECEIVED_GIFT

            parsed_message = Message(
                id=message.id,
                date=utils.timestamp_to_datetime(message.date),
                chat=chat,
                from_user=from_user,
                sender_chat=sender_chat,
                service=service_type,
                new_chat_members=new_chat_members,
                left_chat_member=left_chat_member,
                new_chat_title=new_chat_title,
                new_chat_photo=new_chat_photo,
                delete_chat_photo=delete_chat_photo,
                migrate_to_chat_id=utils.get_channel_id(migrate_to_chat_id) if migrate_to_chat_id else None,
                migrate_from_chat_id=-migrate_from_chat_id if migrate_from_chat_id else None,
                group_chat_created=group_chat_created,
                supergroup_chat_created=supergroup_chat_created,
                channel_chat_created=channel_chat_created,
                video_chat_scheduled=video_chat_scheduled,
                video_chat_started=video_chat_started,
                video_chat_ended=video_chat_ended,
                video_chat_participants_invited=video_chat_participants_invited,
                web_app_data=web_app_data,
                giveaway_created=giveaway_created,
                giveaway_completed=giveaway_completed,
                gift_code=gift_code,
                gifted_premium=gifted_premium,
                gifted_stars=gifted_stars,
                users_shared=users_shared,
                chat_shared=chat_shared,
                connected_website=connected_website,
                write_access_allowed=write_access_allowed,
                received_gift=received_gift,
                successful_payment=successful_payment,
                message_auto_delete_timer_changed=message_auto_delete_timer_changed,
                boost_added=boost_added,
                forum_topic_created=forum_topic_created,
                forum_topic_edited=forum_topic_edited,
                forum_topic_closed=forum_topic_closed,
                forum_topic_reopened=forum_topic_reopened,
                general_forum_topic_hidden=general_forum_topic_hidden,
                general_forum_topic_unhidden=general_forum_topic_unhidden,
                custom_action=custom_action,
                contact_registered=contact_registered,
                chat_join_type=chat_join_type,
                screenshot_taken=screenshot_taken,
                reactions=types.MessageReactions._parse(client, message.reactions) if message.reactions else None,
                client=client
            )

            if isinstance(action, raw.types.MessageActionPinMessage):
                try:
                    parsed_message.pinned_message = await client.get_replied_message(
                        chat_id=parsed_message.chat.id,
                        message_ids=message.id,
                        replies=0
                    )
                except MessageIdsEmpty:
                    parsed_message.pinned_message = types.Message(
                        id=message.reply_to.reply_to_msg_id,
                        empty=True,
                        client=client
                    )
                parsed_message.service = enums.MessageServiceType.PINNED_MESSAGE

            if isinstance(action, raw.types.MessageActionGameScore):
                parsed_message.game_high_score = types.GameHighScore._parse_action(client, message, users)

                if message.reply_to and replies:
                    try:
                        parsed_message.reply_to_message = await client.get_replied_message(
                            chat_id=parsed_message.chat.id,
                            message_ids=message.id,
                            replies=0
                        )

                        parsed_message.service = enums.MessageServiceType.GAME_HIGH_SCORE
                    except MessageIdsEmpty:
                        pass

        if isinstance(message, raw.types.Message):
            entities = [types.MessageEntity._parse(client, entity, users) for entity in message.entities]
            entities = types.List(filter(lambda x: x is not None, entities))

            forward_origin = None
            forward_header = message.fwd_from  # type: raw.types.MessageFwdHeader

            if forward_header:
                forward_origin = types.MessageOrigin._parse(
                    client,
                    forward_header,
                    users,
                    chats,
                )

            photo = None
            location = None
            contact = None
            venue = None
            game = None
            audio = None
            voice = None
            animation = None
            video = None
            alternative_videos = []
            video_note = None
            sticker = None
            story = None
            document = None
            web_page = None
            poll = None
            dice = None
            giveaway = None
            giveaway_winners = None
            invoice = None
            paid_media = None

            media = message.media
            media_type = None
            has_media_spoiler = None

            link_preview_options = None
            web_page_url = None

            if media:
                if isinstance(media, raw.types.MessageMediaPhoto):
                    photo = types.Photo._parse(client, media.photo, media.ttl_seconds, media.spoiler)
                    media_type = enums.MessageMediaType.PHOTO
                    has_media_spoiler = media.spoiler
                elif isinstance(media, raw.types.MessageMediaGeo):
                    location = types.Location._parse(client, media.geo)
                    media_type = enums.MessageMediaType.LOCATION
                elif isinstance(media, raw.types.MessageMediaContact):
                    contact = types.Contact._parse(client, media)
                    media_type = enums.MessageMediaType.CONTACT
                elif isinstance(media, raw.types.MessageMediaVenue):
                    venue = types.Venue._parse(client, media)
                    media_type = enums.MessageMediaType.VENUE
                elif isinstance(media, raw.types.MessageMediaGame):
                    game = types.Game._parse(client, media.game)
                    media_type = enums.MessageMediaType.GAME
                elif isinstance(media, raw.types.MessageMediaDocument):
                    doc = media.document

                    if isinstance(doc, raw.types.Document):
                        attributes = {type(i): i for i in doc.attributes}

                        file_name = getattr(
                            attributes.get(
                                raw.types.DocumentAttributeFilename, None
                            ), "file_name", None
                        )

                        if raw.types.DocumentAttributeAnimated in attributes:
                            video_attributes = attributes.get(raw.types.DocumentAttributeVideo, None)
                            animation = types.Animation._parse(client, doc, video_attributes, file_name)
                            media_type = enums.MessageMediaType.ANIMATION
                            has_media_spoiler = media.spoiler
                        elif raw.types.DocumentAttributeSticker in attributes:
                            sticker = await types.Sticker._parse(client, doc, attributes)
                            media_type = enums.MessageMediaType.STICKER
                        elif raw.types.DocumentAttributeVideo in attributes:
                            video_attributes = attributes[raw.types.DocumentAttributeVideo]

                            if video_attributes.round_message:
                                video_note = types.VideoNote._parse(client, doc, video_attributes, media.ttl_seconds)
                                media_type = enums.MessageMediaType.VIDEO_NOTE
                            else:
                                video = types.Video._parse(client, media, video_attributes, file_name, media.ttl_seconds)
                                media_type = enums.MessageMediaType.VIDEO
                                has_media_spoiler = media.spoiler

                                altdocs = media.alt_documents or []
                                for altdoc in altdocs:
                                    if isinstance(altdoc, raw.types.Document):
                                        altdoc_attributes = {type(i): i for i in altdoc.attributes}

                                        altdoc_file_name = getattr(
                                            altdoc_attributes.get(
                                                raw.types.DocumentAttributeFilename, None
                                            ), "file_name", None
                                        )
                                        altdoc_video_attribute = altdoc_attributes.get(raw.types.DocumentAttributeVideo, None)
                                        if altdoc_video_attribute:
                                            alternative_videos.append(
                                                types.AlternativeVideo._parse(client, altdoc, altdoc_video_attribute, altdoc_file_name)
                                            )
                        elif raw.types.DocumentAttributeAudio in attributes:
                            audio_attributes = attributes[raw.types.DocumentAttributeAudio]

                            if audio_attributes.voice:
                                voice = types.Voice._parse(client, doc, audio_attributes, media.ttl_seconds)
                                media_type = enums.MessageMediaType.VOICE
                            else:
                                audio = types.Audio._parse(client, doc, audio_attributes, file_name)
                                media_type = enums.MessageMediaType.AUDIO
                        else:
                            document = types.Document._parse(client, doc, file_name)
                            media_type = enums.MessageMediaType.DOCUMENT

                    elif doc is None:
                        has_media_spoiler = media.spoiler
                        if media.video:
                            video = types.Video._parse(client, media, None, None, media.ttl_seconds)
                            media_type = enums.MessageMediaType.VIDEO
                        elif media.round:
                            video_note = types.VideoNote._parse(client, doc, None, media.ttl_seconds)
                            media_type = enums.MessageMediaType.VIDEO_NOTE
                        elif media.voice:
                            voice = types.Voice._parse(client, doc, None, media.ttl_seconds)
                            media_type = enums.MessageMediaType.VOICE

                elif isinstance(media, raw.types.MessageMediaWebPage):
                    if isinstance(media.webpage, raw.types.WebPage):
                        web_page = types.WebPage._parse(client, media.webpage)
                        media_type = enums.MessageMediaType.WEB_PAGE
                        web_page_url = media.webpage.url
                    elif isinstance(media.webpage, raw.types.WebPageEmpty):
                        media_type = None
                        web_page_url = getattr(media.webpage, "url", None)
                    else:
                        media_type = None
                        web_page_url = utils.get_first_url(message)
                    link_preview_options = types.LinkPreviewOptions._parse(
                        client,
                        media,
                        web_page_url,
                        getattr(message, "invert_media", False)
                    )
                    if not web_page:
                        media = None
                elif isinstance(media, raw.types.MessageMediaPoll):
                    poll = types.Poll._parse(client, media)
                    media_type = enums.MessageMediaType.POLL
                elif isinstance(media, raw.types.MessageMediaDice):
                    dice = types.Dice._parse(client, media)
                    media_type = enums.MessageMediaType.DICE
                elif isinstance(media, raw.types.MessageMediaStory):
                    story = await types.Story._parse(client, users, chats, media, None, None, None, None)
                    media_type = enums.MessageMediaType.STORY
                elif isinstance(media, raw.types.MessageMediaGiveaway):
                    giveaway = types.Giveaway._parse(client, chats, media)
                    media_type = enums.MessageMediaType.GIVEAWAY
                elif isinstance(media, raw.types.MessageMediaGiveawayResults):
                    giveaway_winners = types.GiveawayWinners._parse(client, chats, users, media)
                    media_type = enums.MessageMediaType.GIVEAWAY_WINNERS
                elif isinstance(media, raw.types.MessageMediaInvoice):
                    invoice = types.Invoice._parse(client, media)
                    media_type = enums.MessageMediaType.INVOICE
                elif isinstance(media, raw.types.MessageMediaPaidMedia):
                    paid_media = types.PaidMediaInfo._parse(client, media)
                    media_type = enums.MessageMediaType.PAID_MEDIA
                else:
                    media = None

            show_caption_above_media = getattr(message, "invert_media", False)
            if (
                not link_preview_options and
                web_page_url
            ):
                link_preview_options = types.LinkPreviewOptions._parse(
                    client,
                    None,
                    web_page_url,
                    show_caption_above_media
                )

            reply_markup = message.reply_markup

            if reply_markup:
                if isinstance(reply_markup, raw.types.ReplyKeyboardForceReply):
                    reply_markup = types.ForceReply.read(reply_markup)
                elif isinstance(reply_markup, raw.types.ReplyKeyboardMarkup):
                    reply_markup = types.ReplyKeyboardMarkup.read(reply_markup)
                elif isinstance(reply_markup, raw.types.ReplyInlineMarkup):
                    reply_markup = types.InlineKeyboardMarkup.read(reply_markup)
                elif isinstance(reply_markup, raw.types.ReplyKeyboardHide):
                    reply_markup = types.ReplyKeyboardRemove.read(reply_markup)
                else:
                    reply_markup = None

            from_user = types.User._parse(client, users.get(user_id, None))
            sender_chat = types.Chat._parse(client, message, users, chats, is_chat=False) if not from_user else None

            reactions = types.MessageReactions._parse(client, message.reactions)

            parsed_message = Message(
                id=message.id,
                date=utils.timestamp_to_datetime(message.date),
                chat=types.Chat._parse(client, message, users, chats, is_chat=True),
                from_user=from_user,
                sender_chat=sender_chat,
                text=(
                    Str(message.message).init(entities) or None
                    if media is None or web_page is not None
                    else None
                ),
                caption=(
                    Str(message.message).init(entities) or None
                    if media is not None and web_page is None
                    else None
                ),
                entities=(
                    entities or None
                    if media is None or web_page is not None
                    else None
                ),
                caption_entities=(
                    entities or None
                    if media is not None and web_page is None
                    else None
                ),
                author_signature=message.post_author,
                has_protected_content=message.noforwards,
                has_media_spoiler=has_media_spoiler,
                forward_origin=forward_origin,
                mentioned=message.mentioned,
                scheduled=is_scheduled,
                from_scheduled=message.from_scheduled,
                media=media_type,
                edit_date=utils.timestamp_to_datetime(message.edit_date),
                media_group_id=message.grouped_id,
                photo=photo,
                location=location,
                contact=contact,
                venue=venue,
                audio=audio,
                voice=voice,
                animation=animation,
                game=game,
                video=video,
                alternative_videos=types.List(alternative_videos) if alternative_videos else None,
                video_note=video_note,
                sticker=sticker,
                story=story,
                document=document,
                web_page=web_page,
                poll=poll,
                dice=dice,
                giveaway=giveaway,
                giveaway_winners=giveaway_winners,
                invoice=invoice,
                views=message.views,
                forwards=message.forwards,
                via_bot=types.User._parse(client, users.get(message.via_bot_id, None)),
                outgoing=message.out,
                reply_markup=reply_markup,
                reactions=reactions,
                client=client,
                link_preview_options=link_preview_options,
                effect_id=getattr(message, "effect", None),
                show_caption_above_media=show_caption_above_media,
                paid_media=paid_media,
                paid_message_star_count=message.paid_message_stars
            )

            parsed_message.external_reply = await types.ExternalReplyInfo._parse(
                client,
                chats,
                users,
                message.reply_to
            )
            parsed_message.sender_boost_count = getattr(message, "from_boosts_applied", None)

            if getattr(message, "via_business_bot_id", None):
                parsed_message.sender_business_bot = types.User._parse(client, users.get(message.via_business_bot_id, None))

            parsed_message.is_from_offline = getattr(message, "offline", None)

            if (
                forward_header and
                forward_header.saved_from_peer and
                forward_header.saved_from_msg_id
            ):
                saved_from_peer_id = utils.get_raw_peer_id(forward_header.saved_from_peer)
                saved_from_peer_chat = chats.get(saved_from_peer_id)
                if (
                    isinstance(saved_from_peer_chat, raw.types.Channel) and
                    not saved_from_peer_chat.megagroup
                ):
                    parsed_message.is_automatic_forward = True

        if getattr(message, "reply_to", None):
            parsed_message.reply_to_message_id = None
            parsed_message.message_thread_id = None
            if isinstance(message.reply_to, raw.types.MessageReplyHeader):
                parsed_message.reply_to_message_id = message.reply_to.reply_to_msg_id
                parsed_message.message_thread_id = message.reply_to.reply_to_top_id
                if message.reply_to.forum_topic:
                    parsed_message.is_topic_message = True
                    if message.reply_to.reply_to_top_id:
                        parsed_message.message_thread_id = message.reply_to.reply_to_top_id
                    else:
                        parsed_message.message_thread_id = message.reply_to.reply_to_msg_id
                    if not parsed_message.message_thread_id:
                        parsed_message.message_thread_id = 1  # https://t.me/c/1279877202/31475
                if getattr(message.reply_to, "quote", False):
                    parsed_message.quote = types.TextQuote._parse(
                        client,
                        chats,
                        users,
                        message.reply_to
                    )

            if isinstance(message.reply_to, raw.types.MessageReplyStoryHeader):
                parsed_message.reply_to_story = await types.Story._parse(client, users, chats, None, message.reply_to, None, None, None)

            if replies:
                try:
                    key = (parsed_message.chat.id, parsed_message.reply_to_message_id)
                    reply_to_message = client.message_cache[key]

                    if not reply_to_message:
                        reply_to_message = await client.get_replied_message(
                            chat_id=parsed_message.chat.id,
                            message_ids=message.id,
                            replies=replies - 1
                        )

                    parsed_message.reply_to_message = reply_to_message
                except MessageIdsEmpty:
                    pass

        if business_connection_id:
            parsed_message.business_connection_id = business_connection_id
        if raw_reply_to_message:
            parsed_message.reply_to_message = await types.Message._parse(
                client,
                raw_reply_to_message,
                users,
                chats,
                business_connection_id=business_connection_id,
                replies=0
            )

        if not parsed_message.poll:  # Do not cache poll messages
            client.message_cache[(parsed_message.chat.id, parsed_message.id)] = parsed_message

        parsed_message._raw = message

        return parsed_message

    @property
    def link(self) -> str:
        if (
            self.chat and
            self.chat.type in {
                enums.ChatType.SUPERGROUP,
                enums.ChatType.CHANNEL
            }
        ):
            if self.chat.username:
                return f"https://t.me/{self.chat.username}{f'/{self.message_thread_id}' if self.message_thread_id else ''}/{self.id}"
            return f"https://t.me/c/{utils.get_channel_id(self.chat.id)}{f'/{self.message_thread_id}' if self.message_thread_id else ''}/{self.id}"

    @property
    def content(self) -> str:
        return self.text or self.caption or Str("").init([])

    async def get_media_group(self) -> list["types.Message"]:
        """Bound method *get_media_group* of :obj:`~pyrogram.types.Message`.
        
        Use as a shortcut for:
        
        .. code-block:: python

            await client.get_media_group(
                chat_id=message.chat.id,
                message_id=message.id
            )
            
        Example:
            .. code-block:: python

                await message.get_media_group()
                
        Returns:
            List of :obj:`~pyrogram.types.Message`: On success, a list of messages of the media group is returned.
            
        Raises:
            ValueError: In case the passed message id doesn't belong to a media group.
        """

        return await self._client.get_media_group(
            chat_id=self.chat.id,
            message_id=self.id
        )

    async def reply_text(
        self,
        text: str = None,
        quote: bool = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: list["types.MessageEntity"] = None,
        link_preview_options: "types.LinkPreviewOptions" = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        disable_web_page_preview: bool = None,
        reply_to_message_id: int = None
    ) -> "Message":
        """Bound method *reply_text* of :obj:`~pyrogram.types.Message`.

        An alias exists as *reply*.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_message(
                chat_id=message.chat.id,
                text="hello",
                reply_parameters=ReplyParameter(
                    message_id=message_id
                )
            )

        Example:
            .. code-block:: python

                await message.reply_text(text="hello", quote=True)

        Parameters:
            text (``str``):
                Text of the message to be sent.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_parameters* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            link_preview_options (:obj:`~pyrogram.types.LinkPreviewOptions`, *optional*):
                Link preview generation options for the message

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

        Returns:
            On success, the sent Message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_message(
            chat_id=self.chat.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
            schedule_date=schedule_date,
            disable_web_page_preview=disable_web_page_preview,
            reply_to_message_id=reply_to_message_id
        )

    reply = reply_text

    async def reply_animation(
        self,
        animation: Union[str, "io.BytesIO"],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        show_caption_above_media: bool = None,
        unsave: bool = False,
        has_spoiler: bool = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: Union[str, "io.BytesIO"] = None,
        file_name: str = None,
        disable_notification: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        ttl_seconds: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        send_as: Union[int, str] = None,
        reply_to_message_id: int = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_animation* :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_animation(
                chat_id=message.chat.id,
                animation=animation
            )

        Example:
            .. code-block:: python

                await message.reply_animation(animation)

        Parameters:
            animation (``str``):
                Animation to send.
                Pass a file_id as string to send an animation that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an animation from the Internet, or
                pass a file path as string to upload a new animation that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_parameters* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Animation caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media.

            unsave (``bool``, *optional*):
                By default, the server will save into your own collection any new animation you send.
                Pass True to automatically unsave the sent animation. Defaults to False.

            has_spoiler (``bool``, *optional*):
                Pass True if the animation needs to be covered with a spoiler animation.

            duration (``int``, *optional*):
                Duration of sent animation in seconds.

            width (``int``, *optional*):
                Animation width.

            height (``int``, *optional*):
                Animation height.

            thumb (``str``, *optional*):
                Thumbnail of the animation file sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            file_name (``str``, *optional*):
                File name of the animation sent.
                Defaults to file's path basename.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            ttl_seconds (``int``, *optional*):
                The message will be self-destructed in the specified time after its content was opened.
                The message's self-destruct time, in seconds; must be between 0 and 60 in private chats.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_animation(
            chat_id=self.chat.id,
            animation=animation,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            unsave=unsave,
            has_spoiler=has_spoiler,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            file_name=file_name,
            disable_notification=disable_notification,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            schedule_date=schedule_date,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            ttl_seconds=ttl_seconds,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_audio(
        self,
        audio: Union[str, "io.BytesIO"],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        duration: int = 0,
        performer: str = None,
        title: str = None,
        thumb: Union[str, "io.BytesIO"] = None,
        file_name: str = None,
        disable_notification: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reply_to_message_id: int = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_audio* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_audio(
                chat_id=message.chat.id,
                audio=audio
            )

        Example:
            .. code-block:: python

                await message.reply_audio(audio)

        Parameters:
            audio (``str``):
                Audio file to send.
                Pass a file_id as string to send an audio file that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an audio file from the Internet, or
                pass a file path as string to upload a new audio file that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Audio caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            duration (``int``, *optional*):
                Duration of the audio in seconds.

            performer (``str``, *optional*):
                Performer.

            title (``str``, *optional*):
                Track name.

            thumb (``str``, *optional*):
                Thumbnail of the music file album cover.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            file_name (``str``, *optional*):
                File name of the audio sent.
                Defaults to file's path basename.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_audio(
            chat_id=self.chat.id,
            audio=audio,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumb=thumb,
            file_name=file_name,
            disable_notification=disable_notification,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            schedule_date=schedule_date,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_cached_media(
        self,
        file_id: str,
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        show_caption_above_media: bool = None,
        disable_notification: bool = None,
        message_effect_id: int = None,
        allow_paid_broadcast: bool = None,
        reply_parameters: "types.ReplyParameters" = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reply_to_message_id: int = None
    ) -> "Message":
        """Bound method *reply_cached_media* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_cached_media(
                chat_id=message.chat.id,
                file_id=file_id
            )

        Example:
            .. code-block:: python

                await message.reply_cached_media(file_id)

        Parameters:
            file_id (``str``):
                Media to send.
                Pass a file_id as string to send a media that exists on the Telegram servers.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``bool``, *optional*):
                Media caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media. Supported only for animation, photo and video messages.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_cached_media(
            chat_id=self.chat.id,
            file_id=file_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            disable_notification=disable_notification,
            message_effect_id=message_effect_id,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            reply_parameters=reply_parameters,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            schedule_date=schedule_date,
            protect_content=self.has_protected_content,
            has_spoiler=self.has_media_spoiler,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id
        )

    async def reply_chat_action(
        self,
        action: "enums.ChatAction",
        progress: int = 0,
        emoji: str = None,
        emoji_message_id: int = None,
        emoji_message_interaction: "raw.types.DataJSON" = None
    ) -> bool:
        """Bound method *reply_chat_action* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            from pyrogram import enums

            await client.send_chat_action(
                chat_id=message.chat.id,
                action=enums.ChatAction.TYPING
            )

        Example:
            .. code-block:: python

                from pyrogram import enums

                await message.reply_chat_action(enums.ChatAction.TYPING)

        Parameters:
            action (:obj:`~pyrogram.enums.ChatAction`):
                Type of action to broadcast.

            progress (``int``, *optional*):
                Upload progress, as a percentage.

            emoji (``str``, *optional*):
                The animated emoji. Only supported for :obj:`~pyrogram.enums.ChatAction.TRIGGER_EMOJI_ANIMATION` and :obj:`~pyrogram.enums.ChatAction.WATCH_EMOJI_ANIMATION`.

            emoji_message_id (``int``, *optional*):
                Message identifier of the message containing the animated emoji. Only supported for :obj:`~pyrogram.enums.ChatAction.TRIGGER_EMOJI_ANIMATION`.

            emoji_message_interaction (:obj:`raw.types.DataJSON`, *optional*):
                Only supported for :obj:`~pyrogram.enums.ChatAction.TRIGGER_EMOJI_ANIMATION`.

        Returns:
            ``bool``: On success, True is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
            ValueError: In case the provided string is not a valid chat action.
        """
        return await self._client.send_chat_action(
            chat_id=self.chat.id,
            action=action,
            progress=progress,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            emoji=emoji,
            emoji_message_id=emoji_message_id,
            emoji_message_interaction=emoji_message_interaction
        )

    async def reply_contact(
        self,
        phone_number: str,
        first_name: str,
        quote: bool = None,
        last_name: str = "",
        vcard: str = "",
        disable_notification: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reply_to_message_id: int = None
    ) -> "Message":
        """Bound method *reply_contact* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_contact(
                chat_id=message.chat.id,
                phone_number=phone_number,
                first_name=first_name
            )

        Example:
            .. code-block:: python

                await message.reply_contact("+1-123-456-7890", "Name")

        Parameters:
            phone_number (``str``):
                Contact's phone number.

            first_name (``str``):
                Contact's first name.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            last_name (``str``, *optional*):
                Contact's last name.

            vcard (``str``, *optional*):
                Additional data about the contact in the form of a vCard, 0-2048 bytes

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_contact(
            chat_id=self.chat.id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            schedule_date=schedule_date,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id
        )

    async def reply_document(
        self,
        document: Union[str, "io.BytesIO"],
        quote: bool = None,
        thumb: Union[str, "io.BytesIO"] = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        file_name: str = None,
        disable_content_type_detection: bool = None,
        disable_notification: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reply_to_message_id: int = None,
        force_document: bool = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_document* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_document(
                chat_id=message.chat.id,
                document=document
            )

        Example:
            .. code-block:: python

                await message.reply_document(document)

        Parameters:
            document (``str``):
                File to send.
                Pass a file_id as string to send a file that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a file from the Internet, or
                pass a file path as string to upload a new file that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            thumb (``str`` | :obj:`io.BytesIO`, *optional*):
                Thumbnail of the file sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            caption (``str``, *optional*):
                Document caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.
            
            file_name (``str``, *optional*):
                File name of the document sent.
                Defaults to file's path basename.

            disable_content_type_detection (``bool``, *optional*):
                Disables automatic server-side content type detection for files uploaded using multipart/form-data.
                Pass True to force sending files as document. Useful for video files that need to be sent as
                document messages instead of video messages.
                Defaults to False.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_document(
            chat_id=self.chat.id,
            document=document,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            file_name=file_name,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            schedule_date=schedule_date,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
            force_document=force_document,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_game(
        self,
        game_short_name: str,
        quote: bool = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        send_as: Union[int, str] = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reply_to_message_id: int = None
    ) -> "Message":
        """Bound method *reply_game* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_game(
                chat_id=message.chat.id,
                game_short_name="lumberjack"
            )

        Example:
            .. code-block:: python

                await message.reply_game("lumberjack")

        Parameters:
            game_short_name (``str``):
                Short name of the game, serves as the unique identifier for the game. Set up your games via Botfather.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An object for an inline keyboard. If empty, one ‘Play game_title’ button will be shown automatically.
                If not empty, the first button must launch the game.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_game(
            chat_id=self.chat.id,
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id
        )

    async def reply_inline_bot_result(
        self,
        query_id: int,
        result_id: str,
        quote: bool = None,
        disable_notification: bool = None,
        reply_parameters: "types.ReplyParameters" = None,
        send_as: Union[int, str] = None,
        reply_to_message_id: int = None
    ) -> "Message":
        """Bound method *reply_inline_bot_result* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_inline_bot_result(
                chat_id=message.chat.id,
                query_id=query_id,
                result_id=result_id
            )

        Example:
            .. code-block:: python

                await message.reply_inline_bot_result(query_id, result_id)

        Parameters:
            query_id (``int``):
                Unique identifier for the answered query.

            result_id (``str``):
                Unique identifier for the result that was chosen.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

        Returns:
            On success, the sent Message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_inline_bot_result(
            chat_id=self.chat.id,
            query_id=query_id,
            result_id=result_id,
            disable_notification=disable_notification,
            reply_parameters=reply_parameters,
            send_as=send_as,
            reply_to_message_id=reply_to_message_id
        )

    async def reply_location(
        self,
        latitude: float,
        longitude: float,
        quote: bool = None,
        horizontal_accuracy: float = None,
        # TODO
        disable_notification: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reply_to_message_id: int = None
    ) -> "Message":
        """Bound method *reply_location* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_location(
                chat_id=message.chat.id,
                latitude=latitude,
                longitude=longitude
            )

        Example:
            .. code-block:: python

                await message.reply_location(latitude, longitude)

        Parameters:
            latitude (``float``):
                Latitude of the location.

            longitude (``float``):
                Longitude of the location.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            horizontal_accuracy (``float``, *optional*):
                The radius of uncertainty for the location, measured in meters; 0-1500.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_location(
            chat_id=self.chat.id,
            latitude=latitude,
            longitude=longitude,
            horizontal_accuracy=horizontal_accuracy,
            disable_notification=disable_notification,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            schedule_date=schedule_date,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id
        )

    async def reply_media_group(
        self,
        media: list[Union["types.InputMediaPhoto", "types.InputMediaVideo"]],
        quote: bool = None,
        disable_notification: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        reply_to_message_id: int = None
    ) -> list["types.Message"]:
        """Bound method *reply_media_group* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_media_group(
                chat_id=message.chat.id,
                media=list_of_media
            )

        Example:
            .. code-block:: python

                await message.reply_media_group(list_of_media)

        Parameters:
            media (``list``):
                A list containing either :obj:`~pyrogram.types.InputMediaPhoto` or
                :obj:`~pyrogram.types.InputMediaVideo` objects
                describing photos and videos to be sent, must include 2–10 items.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

        Returns:
            On success, a :obj:`~pyrogram.types.Messages` object is returned containing all the
            single messages sent.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_media_group(
            chat_id=self.chat.id,
            media=media,
            disable_notification=disable_notification,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            schedule_date=schedule_date,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            reply_to_message_id=reply_to_message_id
        )

    async def reply_photo(
        self,
        photo: Union[str, "io.BytesIO"],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        show_caption_above_media: bool = None,
        has_spoiler: bool = None,
        ttl_seconds: int = None,
        disable_notification: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        view_once: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reply_to_message_id: int = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_photo* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_photo(
                chat_id=message.chat.id,
                photo=photo
            )

        Example:
            .. code-block:: python

                await message.reply_photo(photo)

        Parameters:
            photo (``str`` | :obj:`io.BytesIO`):
                Photo to send.
                Pass a file_id as string to send a photo that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a photo from the Internet,
                pass a file path as string to upload a new photo that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.
                The photo must be at most 10 MB in size.
                The photo's width and height must not exceed 10000 in total.
                The photo's width and height ratio must be at most 20.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Photo caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media.

            has_spoiler (``bool``, *optional*):
                Pass True if the photo needs to be covered with a spoiler animation.

            ttl_seconds (``int``, *optional*):
                The message will be self-destructed in the specified time after its content was opened.
                The message's self-destruct time, in seconds; must be between 0 and 60 in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            view_once (``bool``, *optional*):
                Pass True if the message should be opened only once and should be self-destructed once closed; private chats only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_photo(
            chat_id=self.chat.id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            has_spoiler=has_spoiler,
            ttl_seconds=ttl_seconds,
            disable_notification=disable_notification,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            schedule_date=schedule_date,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            view_once=view_once,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_poll(
        self,
        question: str,
        options: list[str],
        question_parse_mode: "enums.ParseMode" = None,
        question_entities: list["types.MessageEntity"] = None,
        is_anonymous: bool = True,
        type: "enums.PollType" = enums.PollType.REGULAR,
        allows_multiple_answers: bool = None,
        correct_option_id: int = None,
        explanation: str = None,
        explanation_parse_mode: "enums.ParseMode" = None,
        explanation_entities: list["types.MessageEntity"] = None,
        open_period: int = None,
        close_date: datetime = None,
        is_closed: bool = None,
        quote: bool = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reply_to_message_id: int = None
    ) -> "Message":
        """Bound method *reply_poll* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_poll(
                chat_id=message.chat.id,
                question="This is a poll",
                options=[
                    InputPollOption(text="A"),
                    InputPollOption(text="B"),
                    InputPollOption(text= "C"),
                ]
            )

        Example:
            .. code-block:: python

                await message.reply_poll(
                    question="This is a poll",
                    options=[
                        InputPollOption(text="A"),
                        InputPollOption(text="B"),
                        InputPollOption(text= "C"),
                    ]
                )

        Parameters:

            question (``str``):
                Poll question, 1-255 characters.

            options (List of ``str``):
                List of answer options, 2-10 strings 1-100 characters each.

            question_parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            question_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the poll question, which can be specified instead of *question_parse_mode*.

            is_anonymous (``bool``, *optional*):
                True, if the poll needs to be anonymous.
                Defaults to True.

            type (:obj:`~pyrogram.enums.PollType`, *optional*):
                Poll type, :obj:`~pyrogram.enums.PollType.QUIZ` or :obj:`~pyrogram.enums.PollType.REGULAR`.
                Defaults to :obj:`~pyrogram.enums.PollType.REGULAR`.

            allows_multiple_answers (``bool``, *optional*):
                True, if the poll allows multiple answers, ignored for polls in quiz mode.
                Defaults to False.

            correct_option_id (``int``, *optional*):
                0-based identifier of the correct answer option, required for polls in quiz mode.

            explanation (``str``, *optional*):
                Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style
                poll, 0-200 characters with at most 2 line feeds after entities parsing.

            explanation_parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            explanation_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the poll explanation, which can be specified instead of
                *parse_mode*.

            open_period (``int``, *optional*):
                Amount of time in seconds the poll will be active after creation, 5-600.
                Can't be used together with *close_date*.

            close_date (:py:obj:`~datetime.datetime`, *optional*):
                Point in time when the poll will be automatically closed.
                Must be at least 5 and no more than 600 seconds in the future.
                Can't be used together with *open_period*.

            is_closed (``bool``, *optional*):
                Pass True, if the poll needs to be immediately closed.
                This can be useful for poll preview.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_poll(
            chat_id=self.chat.id,
            question=question,
            options=options,
            question_parse_mode=question_parse_mode,
            question_entities=question_entities,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            correct_option_id=correct_option_id,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            schedule_date=schedule_date,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup
        )

    async def reply_sticker(
        self,
        sticker: Union[str, "io.BytesIO"],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        emoji: str = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        reply_to_message_id: int = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_sticker* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_sticker(
                chat_id=message.chat.id,
                sticker=sticker
            )

        Example:
            .. code-block:: python

                await message.reply_sticker(sticker)

        Parameters:
            sticker (``str``):
                Sticker to send.
                Pass a file_id as string to send a sticker that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a .webp sticker file from the Internet, or
                pass a file path as string to upload a new sticker that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Photo caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            emoji (``str``, *optional*):
                Emoji associated with the sticker; only for just uploaded stickers

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_sticker(
            chat_id=self.chat.id,
            sticker=sticker,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            emoji=emoji,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
            schedule_date=schedule_date,
            reply_to_message_id=reply_to_message_id,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_venue(
        self,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        quote: bool = None,
        foursquare_id: str = "",
        foursquare_type: str = "",
        # TODO
        disable_notification: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reply_to_message_id: int = None
    ) -> "Message":
        """Bound method *reply_venue* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_venue(
                chat_id=message.chat.id,
                latitude=latitude,
                longitude=longitude,
                title="Venue title",
                address="Venue address"
            )

        Example:
            .. code-block:: python

                await message.reply_venue(latitude, longitude, "Venue title", "Venue address")

        Parameters:
            latitude (``float``):
                Latitude of the venue.

            longitude (``float``):
                Longitude of the venue.

            title (``str``):
                Name of the venue.

            address (``str``):
                Address of the venue.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            foursquare_id (``str``, *optional*):
                Foursquare identifier of the venue.

            foursquare_type (``str``, *optional*):
                Foursquare type of the venue, if known.
                (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_venue(
            chat_id=self.chat.id,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            disable_notification=disable_notification,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            schedule_date=schedule_date,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup
        )

    async def reply_video(
        self,
        video: Union[str, "io.BytesIO"],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        show_caption_above_media: bool = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: Union[str, "io.BytesIO"] = None,
        cover: Optional[Union[str, "io.BytesIO"]] = None,
        start_timestamp: int = None,
        has_spoiler: bool = None,
        supports_streaming: bool = True,
        disable_notification: bool = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        ttl_seconds: int = None,
        view_once: bool = None,
        file_name: str = None,
        mime_type: str = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        reply_to_message_id: int = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_video* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_video(
                chat_id=message.chat.id,
                video=video
            )

        Example:
            .. code-block:: python

                await message.reply_video(video)

        Parameters:
            video (``str``):
                Video to send.
                Pass a file_id as string to send a video that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a video from the Internet, or
                pass a file path as string to upload a new video that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Video caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media.

            duration (``int``, *optional*):
                Duration of sent video in seconds.

            width (``int``, *optional*):
                Video width.

            height (``int``, *optional*):
                Video height.

            thumb (``str`` | :obj:`io.BytesIO`, *optional*):
                Thumbnail of the video sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            cover (``str`` | :obj:`io.BytesIO`, *optional*):
                Cover for the video in the message. Pass None to skip cover uploading.
            
            start_timestamp (``int``, *optional*):
                Timestamp from which the video playing must start, in seconds.

            has_spoiler (``bool``, *optional*):
                Pass True if the video needs to be covered with a spoiler animation.

            supports_streaming (``bool``, *optional*):
                Pass True, if the uploaded video is suitable for streaming.
                Defaults to True.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            ttl_seconds (``int``, *optional*):
                The message will be self-destructed in the specified time after its content was opened.
                The message's self-destruct time, in seconds; must be between 0 and 60 in private chats.

            view_once (``bool``, *optional*):
                Pass True if the message should be opened only once and should be self-destructed once closed; private chats only.

            file_name (``str``, *optional*):
                File name of the video sent.
                Defaults to file's path basename.

            mime_type (``str``, *optional*):
                no docs!

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_video(
            chat_id=self.chat.id,
            video=video,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            show_caption_above_media=show_caption_above_media,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            cover=cover,
            start_timestamp=start_timestamp,
            has_spoiler=has_spoiler,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
            ttl_seconds=ttl_seconds,
            view_once=view_once,
            file_name=file_name,
            mime_type=mime_type,
            schedule_date=schedule_date,
            reply_to_message_id=reply_to_message_id,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_video_note(
        self,
        video_note: Union[str, "io.BytesIO"],
        quote: bool = None,
        duration: int = 0,
        length: int = 1,
        thumb: Union[str, "io.BytesIO"] = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        ttl_seconds: int = None,
        view_once: bool = None,
        reply_to_message_id: int = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_video_note* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_video_note(
                chat_id=message.chat.id,
                video_note=video_note
            )

        Example:
            .. code-block:: python

                await message.reply_video_note(video_note)

        Parameters:
            video_note (``str``):
                Video note to send.
                Pass a file_id as string to send a video note that exists on the Telegram servers, or
                pass a file path as string to upload a new video note that exists on your local machine.
                Sending video notes by a URL is currently unsupported.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            duration (``int``, *optional*):
                Duration of sent video in seconds.

            length (``int``, *optional*):
                Video width and height.

            thumb (``str``, *optional*):
                Thumbnail of the video sent.
                The thumbnail should be in JPEG format and less than 200 KB in size.
                A thumbnail's width and height should not exceed 320 pixels.
                Thumbnails can't be reused and can be only uploaded as a new file.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            caption (``str``, *optional*):
                Video caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            ttl_seconds (``int``, *optional*):
                The message will be self-destructed in the specified time after its content was opened.
                The message's self-destruct time, in seconds; must be between 0 and 60 in private chats.

            view_once (``bool``, *optional*):
                Pass True if the message should be opened only once and should be self-destructed once closed; private chats only.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_video_note(
            chat_id=self.chat.id,
            video_note=video_note,
            duration=duration,
            length=length,
            thumb=thumb,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            schedule_date=schedule_date,
            ttl_seconds=ttl_seconds,
            view_once=view_once,
            reply_to_message_id=reply_to_message_id,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_voice(
        self,
        voice: Union[str, "io.BytesIO"],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        duration: int = 0,
        disable_notification: bool = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        ttl_seconds: int = None,
        view_once: bool = None,
        waveform: bytes = None,
        reply_to_message_id: int = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        """Bound method *reply_voice* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_voice(
                chat_id=message.chat.id,
                voice=voice
            )

        Example:
            .. code-block:: python

                await message.reply_voice(voice)

        Parameters:
            voice (``str``):
                Audio file to send.
                Pass a file_id as string to send an audio that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get an audio from the Internet, or
                pass a file path as string to upload a new audio that exists on your local machine.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            caption (``str``, *optional*):
                Voice message caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            duration (``int``, *optional*):
                Duration of the voice message in seconds.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            ttl_seconds (``int``, *optional*):
                The message will be self-destructed in the specified time after its content was opened.
                The message's self-destruct time, in seconds; must be between 0 and 60 in private chats.

            view_once (``bool``, *optional*):
                Pass True if the message should be opened only once and should be self-destructed once closed; private chats only.

            waveform (``bytes``, *optional*):
                no docs!

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.
            In case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned
            instead.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_voice(
            chat_id=self.chat.id,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            message_thread_id=self.message_thread_id,
            business_connection_id=self.business_connection_id,
            send_as=send_as,
            message_effect_id=message_effect_id,
            reply_parameters=reply_parameters,
            reply_markup=reply_markup,
            schedule_date=schedule_date,
            ttl_seconds=ttl_seconds,
            view_once=view_once,
            waveform=waveform,
            reply_to_message_id=reply_to_message_id,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_invoice(
        self,
        title: str,
        description: str,
        payload: Union[str, bytes],
        currency: str,
        prices: list["types.LabeledPrice"],
        message_thread_id: int = None,
        quote: bool = None,
        provider_token: str = None,
        max_tip_amount: int = None,
        suggested_tip_amounts: list[int] = None,
        start_parameter: str = None,
        provider_data: str = None,
        photo_url: str = "",
        photo_size: int = None,
        photo_width: int = None,
        photo_height: int = None,
        need_name: bool = None,
        need_phone_number: bool = None,
        need_email: bool = None,
        need_shipping_address: bool = None,
        send_phone_number_to_provider: bool = None,
        send_email_to_provider: bool = None,
        is_flexible: bool = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        message_effect_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        send_as: Union[int, str] = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None
    ) -> "Message":
        """Bound method *reply_invoice* of :obj:`~pyrogram.types.Message`.

        Parameters:
            title (``str``):
                Product name, 1-32 characters.

            description (``str``):
                Product description, 1-255 characters

            payload (``str`` | ``bytes``):
                Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use for your internal processes.

            currency (``str``):
                Three-letter ISO 4217 currency code, see `more on currencies <https://core.telegram.org/bots/payments#supported-currencies>`_. Pass ``XTR`` for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            prices (List of :obj:`~pyrogram.types.LabeledPrice`):
                Price breakdown, a JSON-serialized list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.). Must contain exactly one item for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            message_thread_id (``int``, *optional*):
                If the message is in a thread, ID of the original message.

            quote (``bool``, *optional*):
                If ``True``, the message will be sent as a reply to this message.
                If *reply_to_message_id* is passed, this parameter will be ignored.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            provider_token (``str``, *optional*):
                Payment provider token, obtained via `@BotFather <https://t.me/botfather>`_. Pass an empty string for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            max_tip_amount (``int``, *optional*):
                The maximum accepted amount for tips in the smallest units of the currency (integer, **not** float/double). For example, for a maximum tip of ``US$ 1.45`` pass ``max_tip_amount = 145``. See the exp parameter in `currencies.json <https://core.telegram.org/bots/payments/currencies.json>`_, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0. Not supported for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            suggested_tip_amounts (List of ``int``, *optional*):
                An array of suggested amounts of tips in the smallest units of the currency (integer, **not** float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed ``max_tip_amount``.

            start_parameter (``str``, *optional*):
                Unique deep-linking parameter. If left empty, **forwarded copies** of the sent message will have a Pay button, allowing multiple users to pay directly from the forwarded message, using the same invoice. If non-empty, forwarded copies of the sent message will have a URL button with a deep link to the bot (instead of a Pay button), with the value used as the start parameter.

            provider_data (``str``, *optional*):
                JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.

            photo_url (``str``, *optional*):
                URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service. People like it better when they see what they are paying for.

            photo_size (``int``, *optional*):
                Photo size in bytes

            photo_width (``int``, *optional*):
                Photo width

            photo_height (``int``, *optional*):
                Photo height

            need_name (``bool``, *optional*):
                Pass True if you require the user's full name to complete the order. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            need_phone_number (``bool``, *optional*):
                Pass True if you require the user's phone number to complete the order. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            need_email (``bool``, *optional*):
                Pass True if you require the user's email address to complete the order. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            need_shipping_address (``bool``, *optional*):
                Pass True if you require the user's shipping address to complete the order. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            send_phone_number_to_provider (``bool``, *optional*):
                Pass True if the user's phone number should be sent to the provider. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            send_email_to_provider (``bool``, *optional*):
                Pass True if the user's email address should be sent to the provider. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            is_flexible (``bool``, *optional*):
                Pass True if the final price depends on the shipping method. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            caption (``str``, *optional*):
                Document caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        Returns:
            On success, the sent :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if not reply_parameters and quote:
            reply_parameters = types.ReplyParameters(
                message_id=self.id
            )

        return await self._client.send_invoice(
            chat_id=self.chat.id,
            title=title,
            description=description,
            payload=payload,
            currency=currency,
            prices=prices,
            message_thread_id=self.message_thread_id if message_thread_id is None else message_thread_id,
            provider_token=provider_token,
            max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts,
            start_parameter=start_parameter,
            provider_data=provider_data,
            photo_url=photo_url,
            photo_size=photo_size,
            photo_width=photo_width,
            photo_height=photo_height,
            need_name=need_name,
            need_phone_number=need_phone_number,
            need_email=need_email,
            need_shipping_address=need_shipping_address,
            send_phone_number_to_provider=send_phone_number_to_provider,
            send_email_to_provider=send_email_to_provider,
            is_flexible=is_flexible,
            disable_notification=disable_notification,
            protect_content=self.has_protected_content if protect_content is None else protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=(self and self.chat and self.chat.paid_message_star_count) or None,
            message_effect_id=message_effect_id or self.effect_id,
            reply_parameters=reply_parameters,
            send_as=send_as,
            reply_markup=reply_markup,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities
        )

    async def edit_text(
        self,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: list["types.MessageEntity"] = None,
        link_preview_options: "types.LinkPreviewOptions" = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        disable_web_page_preview: bool = None
    ) -> "Message":
        """Bound method *edit_text* of :obj:`~pyrogram.types.Message`.

        An alias exists as *edit*.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text="hello"
            )

        Example:
            .. code-block:: python

                await message.edit_text("hello")

        Parameters:
            text (``str``):
                New text of the message.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            link_preview_options (:obj:`~pyrogram.types.LinkPreviewOptions`, *optional*):
                Link preview generation options for the message

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            On success, the edited :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_message_text(
            chat_id=self.chat.id,
            message_id=self.id,
            schedule_date=self.date if self.scheduled else None,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            link_preview_options=link_preview_options,
            reply_markup=reply_markup,
            business_connection_id=self.business_connection_id,
            disable_web_page_preview=disable_web_page_preview
        )

    edit = edit_text

    async def edit_caption(
        self,
        caption: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> "Message":
        """Bound method *edit_caption* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.id,
                caption="hello"
            )

        Example:
            .. code-block:: python

                await message.edit_caption("hello")

        Parameters:
            caption (``str``):
                New caption of the message.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            On success, the edited :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_message_caption(
            chat_id=self.chat.id,
            message_id=self.id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            reply_markup=reply_markup,
            schedule_date=self.date if self.scheduled else None
        )

    async def edit_media(
        self,
        media: "types.InputMedia",
        reply_markup: "types.InlineKeyboardMarkup" = None,
        file_name: str = None
    ) -> "Message":
        """Bound method *edit_media* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.id,
                media=media
            )

        Example:
            .. code-block:: python

                await message.edit_media(media)

        Parameters:
            media (:obj:`~pyrogram.types.InputMedia`):
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            file_name (``str``, *optional*):
                File name of the media to be sent. Not applicable to photos.
                Defaults to file's path basename.

        Returns:
            On success, the edited :obj:`~pyrogram.types.Message` is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_message_media(
            chat_id=self.chat.id,
            message_id=self.id,
            media=media,
            reply_markup=reply_markup,
            file_name=file_name,
            schedule_date=self.date if self.scheduled else None,
            business_connection_id=self.business_connection_id
        )

    async def edit_reply_markup(self, reply_markup: "types.InlineKeyboardMarkup" = None) -> "Message":
        """Bound method *edit_reply_markup* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.edit_message_reply_markup(
                chat_id=message.chat.id,
                message_id=message.id,
                reply_markup=inline_reply_markup
            )

        Example:
            .. code-block:: python

                await message.edit_reply_markup(inline_reply_markup)

        Parameters:
            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`):
                An InlineKeyboardMarkup object.

        Returns:
            On success, if edited message is sent by the bot, the edited
            :obj:`~pyrogram.types.Message` is returned, otherwise True is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.edit_message_reply_markup(
            chat_id=self.chat.id,
            message_id=self.id,
            reply_markup=reply_markup,
            business_connection_id=self.business_connection_id
        )

    async def edit_cached_media(
        self,
        file_id: str,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        schedule_date: datetime = None,
        has_spoiler: bool = None,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> "Message":
        """Edit a media stored on the Telegram servers using a file_id.

        This convenience method works with any valid file_id only.
        It does the same as calling the relevant method for editing media using a file_id, thus saving you from the
        hassle of using the correct :obj:`~pyrogram.types.InputMedia` for the media the file_id is pointing to.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            file_id (``str``):
                Media to send.
                Pass a file_id as string to send a media that exists on the Telegram servers.

            caption (``str``, *optional*):
                Media caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            has_spoiler (``bool``, *optional*):
                True, if the message media is covered by a spoiler animation.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the edited media message is returned.

        Example:
            .. code-block:: python

                await message.edit_cached_media(file_id)
        """
        return await self._client.edit_cached_media(
            chat_id=self.chat.id,
            message_id=self.id,
            file_id=file_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            schedule_date=schedule_date,
            has_spoiler=has_spoiler,
            reply_markup=reply_markup
        )

    async def forward(
        self,
        chat_id: Union[int, str],
        message_thread_id: int = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        paid_message_star_count: int = None,
        send_copy: bool = None,
        remove_caption: bool = None,
        video_start_timestamp: int = None,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None
    ) -> Union["types.Message", list["types.Message"]]:
        """Bound method *forward* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.forward_messages(
                chat_id=chat_id,
                from_chat_id=message.chat.id,
                message_ids=message.id
            )

        Example:
            .. code-block:: python

                await message.forward(chat_id)

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum; for forum supergroups only

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a fee; for bots only

            paid_message_star_count (``int``, *optional*):
                The number of Telegram Stars the user agreed to pay to send the messages.

            send_copy (``bool``, *optional*):
                Pass True to copy content of the messages without reference to the original sender.

            remove_caption (``bool``, *optional*):
                Pass True to remove media captions of message copies.

            video_start_timestamp (``int``, *optional*):
                New start timestamp for the copied video in the message.

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

        Returns:
            On success, the forwarded Message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.forward_messages(
            from_chat_id=self.chat.id,
            message_ids=self.id,
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_paid_broadcast=allow_paid_broadcast,
            paid_message_star_count=paid_message_star_count,
            send_copy=send_copy,
            remove_caption=remove_caption,
            video_start_timestamp=video_start_timestamp,
            send_as=send_as,
            schedule_date=schedule_date
        )

    async def copy(
        self,
        chat_id: Union[int, str],
        caption: str = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        show_caption_above_media: bool = None,
        video_cover: Optional[Union[str, "io.BytesIO"]] = None,
        video_start_timestamp: int = None,
        disable_notification: bool = None,
        reply_parameters: "types.ReplyParameters" = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = object,
        send_as: Union[int, str] = None,
        schedule_date: datetime = None,
        business_connection_id: str = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        paid_message_star_count: int = None,
        message_thread_id: int = None,
        reply_to_message_id: int = None
    ) -> Union["types.Message", list["types.Message"]]:
        """Bound method *copy* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.copy_message(
                chat_id=chat_id,
                from_chat_id=message.chat.id,
                message_id=message.id
            )

        Example:
            .. code-block:: python

                await message.copy(chat_id)

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            caption (``string``, *optional*):
                New caption for media, 0-1024 characters after entities parsing.
                If not specified, the original caption is kept.
                Pass "" (empty string) to remove the caption.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the new caption, which can be specified instead of *parse_mode*.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media. Ignored if a new caption isn't specified.

            video_cover (``str`` | :obj:`io.BytesIO`, *optional*):
                New cover for the copied video in the message. Pass None to skip cover uploading and use the existing cover.
            
            video_start_timestamp (``int``, *optional*):
                New start timestamp, from which the video playing must start, in seconds for the copied video in the message.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.
                If not specified, the original reply markup is kept.
                Pass None to remove the reply markup.

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            paid_message_star_count (``int``, *optional*):
                The number of Telegram Stars the user agreed to pay to send the messages.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum; for forum supergroups only

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the copied message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if self.service:
            log.warning("Service messages cannot be copied. chat_id: %s, message_id: %s",
                        self.chat.id, self.id)
        elif self.game and not (self._client.me and self._client.me.is_bot):
            log.warning("Users cannot send messages with Game media type. chat_id: %s, message_id: %s",
                        self.chat.id, self.id)
        elif self.empty:
            log.warning("Empty messages cannot be copied.")
        elif self.text:
            return await self._client.send_message(
                chat_id=chat_id,
                message_thread_id=self.message_thread_id if message_thread_id is None else message_thread_id,
                business_connection_id=self.business_connection_id if business_connection_id is None else business_connection_id,
                text=self.text,
                parse_mode=enums.ParseMode.DISABLED,
                entities=self.entities,
                link_preview_options=self.link_preview_options,
                disable_notification=disable_notification,
                protect_content=self.has_protected_content if protect_content is None else protect_content,
                allow_paid_broadcast=allow_paid_broadcast,
                paid_message_star_count=paid_message_star_count,
                message_effect_id=self.effect_id,
                reply_parameters=reply_parameters,
                reply_markup=self.reply_markup if reply_markup is object else reply_markup,
                reply_to_message_id=reply_to_message_id,
                send_as=send_as,
                schedule_date=schedule_date
            )
        elif self.media:
            send_media = partial(
                self._client.send_cached_media,
                chat_id=chat_id,
                disable_notification=disable_notification,
                message_effect_id=self.effect_id,
                show_caption_above_media=show_caption_above_media or self.show_caption_above_media,
                reply_parameters=reply_parameters,
                message_thread_id=self.message_thread_id if message_thread_id is None else message_thread_id,
                business_connection_id=self.business_connection_id if business_connection_id is None else business_connection_id,
                schedule_date=schedule_date,
                protect_content=self.has_protected_content if protect_content is None else protect_content,
                allow_paid_broadcast=allow_paid_broadcast,
                paid_message_star_count=paid_message_star_count,
                has_spoiler=self.has_media_spoiler,
                reply_to_message_id=reply_to_message_id,
                send_as=send_as,
                reply_markup=self.reply_markup if reply_markup is object else reply_markup
            )
            if caption is None:
                caption = self.caption or ""
                caption_entities = self.caption_entities
            if self.photo:
                file_id = self.photo.file_id
            elif self.audio:
                file_id = self.audio.file_id
            elif self.document:
                file_id = self.document.file_id
            elif self.video:
                riom = None
                try:
                    riom = await self._client.send_video(
                        chat_id,
                        video=self.video.file_id,
                        caption=caption,
                        parse_mode=parse_mode,
                        caption_entities=caption_entities,
                        show_caption_above_media=show_caption_above_media or self.show_caption_above_media,
                        cover=video_cover,
                        start_timestamp=video_start_timestamp,
                        has_spoiler=self.has_media_spoiler,
                        disable_notification=disable_notification,
                        protect_content=self.has_protected_content if protect_content is None else protect_content,
                        allow_paid_broadcast=allow_paid_broadcast,
                        paid_message_star_count=paid_message_star_count,
                        message_thread_id=self.message_thread_id if message_thread_id is None else message_thread_id,
                        business_connection_id=self.business_connection_id if business_connection_id is None else business_connection_id,
                        send_as=send_as,
                        message_effect_id=self.effect_id,
                        reply_parameters=reply_parameters,
                        reply_markup=self.reply_markup if reply_markup is object else reply_markup,
                        # TODO
                        schedule_date=schedule_date,
                        reply_to_message_id=reply_to_message_id
                    )
                except FileReferenceExpired:
                    ohm = await self._client.get_messages(self.chat.id, self.id)
                    riom = await self._client.send_video(
                        chat_id,
                        video=ohm.video.file_id,
                        caption=caption,
                        parse_mode=parse_mode,
                        caption_entities=caption_entities,
                        show_caption_above_media=show_caption_above_media or self.show_caption_above_media,
                        cover=video_cover,
                        start_timestamp=video_start_timestamp,
                        has_spoiler=self.has_media_spoiler,
                        disable_notification=disable_notification,
                        protect_content=self.has_protected_content if protect_content is None else protect_content,
                        allow_paid_broadcast=allow_paid_broadcast,
                        paid_message_star_count=paid_message_star_count,
                        message_thread_id=self.message_thread_id if message_thread_id is None else message_thread_id,
                        business_connection_id=self.business_connection_id if business_connection_id is None else business_connection_id,
                        send_as=send_as,
                        message_effect_id=self.effect_id,
                        reply_parameters=reply_parameters,
                        reply_markup=self.reply_markup if reply_markup is object else reply_markup,
                        # TODO
                        schedule_date=schedule_date,
                        reply_to_message_id=reply_to_message_id
                    )
                return riom
            elif self.animation:
                file_id = self.animation.file_id
            elif self.voice:
                file_id = self.voice.file_id
            elif self.sticker:
                file_id = self.sticker.file_id
            elif self.video_note:
                file_id = self.video_note.file_id
            elif self.contact:
                return await self._client.send_contact(
                    chat_id,
                    phone_number=self.contact.phone_number,
                    first_name=self.contact.first_name,
                    last_name=self.contact.last_name,
                    vcard=self.contact.vcard,
                    disable_notification=disable_notification,
                    message_effect_id=self.effect_id,
                    reply_parameters=reply_parameters,
                    message_thread_id=self.message_thread_id if message_thread_id is None else message_thread_id,
                    business_connection_id=self.business_connection_id if business_connection_id is None else business_connection_id,
                    schedule_date=schedule_date,
                    protect_content=self.has_protected_content if protect_content is None else protect_content,
                    allow_paid_broadcast=allow_paid_broadcast,
                    paid_message_star_count=paid_message_star_count,
                    reply_to_message_id=reply_to_message_id,
                    send_as=send_as,
                    reply_markup=self.reply_markup if reply_markup is object else reply_markup
                )
            elif self.location:
                return await self._client.send_location(
                    chat_id,
                    latitude=self.location.latitude,
                    longitude=self.location.longitude,
                    disable_notification=disable_notification,
                    message_effect_id=self.effect_id,
                    reply_parameters=reply_parameters,
                    message_thread_id=self.message_thread_id if message_thread_id is None else message_thread_id,
                    business_connection_id=self.business_connection_id if business_connection_id is None else business_connection_id,
                    schedule_date=schedule_date,
                    protect_content=self.has_protected_content if protect_content is None else protect_content,
                    allow_paid_broadcast=allow_paid_broadcast,
                    paid_message_star_count=paid_message_star_count,
                    reply_to_message_id=reply_to_message_id,
                    send_as=send_as,
                    reply_markup=self.reply_markup if reply_markup is object else reply_markup
                )
            elif self.venue:
                return await self._client.send_venue(
                    chat_id,
                    latitude=self.venue.location.latitude,
                    longitude=self.venue.location.longitude,
                    title=self.venue.title,
                    address=self.venue.address,
                    foursquare_id=self.venue.foursquare_id,
                    foursquare_type=self.venue.foursquare_type,
                    disable_notification=disable_notification,
                    message_effect_id=self.effect_id,
                    reply_parameters=reply_parameters,
                    message_thread_id=self.message_thread_id if message_thread_id is None else message_thread_id,
                    business_connection_id=self.business_connection_id if business_connection_id is None else business_connection_id,
                    schedule_date=schedule_date,
                    protect_content=self.has_protected_content if protect_content is None else protect_content,
                    allow_paid_broadcast=allow_paid_broadcast,
                    paid_message_star_count=paid_message_star_count,
                    reply_to_message_id=reply_to_message_id,
                    send_as=send_as,
                    reply_markup=self.reply_markup if reply_markup is object else reply_markup
                )
            elif self.poll:
                return await self._client.send_poll(
                    chat_id,
                    question=self.poll.question,
                    question_entities=self.poll.question_entities,
                    options=[
                        types.InputPollOption(
                            text=opt.text,
                            text_entities=opt.text_entities
                        ) for opt in self.poll.options
                    ],
                    is_anonymous=self.poll.is_anonymous,
                    type=self.poll.type,
                    allows_multiple_answers=self.poll.allows_multiple_answers,
                    correct_option_id=self.poll.correct_option_id,
                    explanation=self.poll.explanation,
                    explanation_entities=self.poll.explanation_entities,
                    open_period=self.poll.open_period,
                    close_date=self.poll.close_date,
                    disable_notification=disable_notification,
                    protect_content=self.has_protected_content if protect_content is None else protect_content,
                    allow_paid_broadcast=allow_paid_broadcast,
                    paid_message_star_count=paid_message_star_count,
                    message_effect_id=self.effect_id,
                    reply_parameters=reply_parameters,
                    message_thread_id=self.message_thread_id if message_thread_id is None else message_thread_id,
                    business_connection_id=self.business_connection_id if business_connection_id is None else business_connection_id,
                    schedule_date=schedule_date,
                    reply_to_message_id=reply_to_message_id,
                    send_as=send_as,
                    reply_markup=self.reply_markup if reply_markup is object else reply_markup
                )
            elif self.game:
                return await self._client.send_game(
                    chat_id,
                    game_short_name=self.game.short_name,
                    disable_notification=disable_notification,
                    protect_content=self.has_protected_content if protect_content is None else protect_content,
                    allow_paid_broadcast=allow_paid_broadcast,
                    paid_message_star_count=paid_message_star_count,
                    message_thread_id=self.message_thread_id if message_thread_id is None else message_thread_id,
                    business_connection_id=self.business_connection_id if business_connection_id is None else business_connection_id,
                    message_effect_id=self.effect_id,
                    reply_parameters=reply_parameters,
                    reply_to_message_id=reply_to_message_id,
                    send_as=send_as,
                    reply_markup=self.reply_markup if reply_markup is object else reply_markup
                )
            else:
                raise ValueError("Unknown media type")

            return await send_media(
                file_id=file_id,
                caption=caption,
                parse_mode=parse_mode,
                caption_entities=caption_entities,
            )
        else:
            raise ValueError("Can't copy this message")

    async def delete(self, revoke: bool = True):
        """Bound method *delete* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.delete_messages(
                chat_id=chat_id,
                message_ids=message.id
            )

        Example:
            .. code-block:: python

                await message.delete()

        Parameters:
            revoke (``bool``, *optional*):
                Deletes messages on both parts.
                This is only for private cloud chats and normal groups, messages on
                channels and supergroups are always revoked (i.e.: deleted for everyone).
                Defaults to True.

        Returns:
            ``int``: Amount of affected messages

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.delete_messages(
            chat_id=self.chat.id,
            message_ids=self.id,
            revoke=revoke,
            is_scheduled=self.scheduled
        )

    async def click(
        self,
        x: Union[int, str] = 0,
        y: int = None,
        quote: bool = None,
        timeout: int = 10,
        request_write_access: bool = True,
        password: str = None
    ):
        """Bound method *click* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for clicking a button attached to the message instead of:

        - Clicking inline buttons:

        .. code-block:: python

            await client.request_callback_answer(
                chat_id=message.chat.id,
                message_id=message.id,
                callback_data=message.reply_markup[i][j].callback_data
            )

        - Clicking normal buttons:

        .. code-block:: python

            await client.send_message(
                chat_id=message.chat.id,
                text=message.reply_markup[i][j].text
            )

        Example:
            This method can be used in three different ways:

            1.  Pass one integer argument only (e.g.: ``.click(2)``, to click a button at index 2).
                Buttons are counted left to right, starting from the top.

            2.  Pass two integer arguments (e.g.: ``.click(1, 0)``, to click a button at position (1, 0)).
                The origin (0, 0) is top-left.

            3.  Pass one string argument only (e.g.: ``.click("Settings")``, to click a button by using its label).
                Only the first matching button will be pressed.

        Parameters:
            x (``int`` | ``str``):
                Used as integer index, integer abscissa (in pair with y) or as string label.
                Defaults to 0 (first button).

            y (``int``, *optional*):
                Used as ordinate only (in pair with x).

            quote (``bool``, *optional*):
                Useful for normal buttons only, where pressing it will result in a new message sent.
                If ``True``, the message will be sent as a reply to this message.
                Defaults to ``True`` in group chats and ``False`` in private chats.

            timeout (``int``, *optional*):
                Timeout in seconds.

            request_write_access (``bool``, *optional*):
                Only used in case of :obj:`~pyrogram.types.LoginUrl` button.
                True, if the bot can send messages to the user.
                Defaults to ``True``.

            password (``str``, *optional*):
                When clicking certain buttons (such as BotFather's confirmation button to transfer ownership), if your account has 2FA enabled, you need to provide your account's password. 
                The 2-step verification password for the current user. Only applicable, if the :obj:`~pyrogram.types.InlineKeyboardButton` contains ``callback_data_with_password``.

        Returns:
            -   The result of :meth:`~pyrogram.Client.request_callback_answer` in case of inline callback button clicks.
            -   The result of :meth:`~Message.reply()` in case of normal button clicks.
            -   A string in case the inline button is a URL, a *switch_inline_query* or a
                *switch_inline_query_current_chat* button.
            -   A string URL with the user details, in case of a LoginUrl button.
            -   A :obj:`~pyrogram.types.SwitchInlineQueryChosenChat` object in case of a ``switch_inline_query_chosen_chat``.
            -   A :obj:`~pyrogram.types.User` object in case of a ``KeyboardButtonUserProfile`` button.

        Raises:
            RPCError: In case of a Telegram RPC error.
            ValueError: In case the provided index or position is out of range or the button label was not found.
            TimeoutError: In case, after clicking an inline button, the bot fails to answer within the timeout.
        """

        if isinstance(self.reply_markup, types.ReplyKeyboardMarkup):
            keyboard = self.reply_markup.keyboard
            is_inline = False
        elif isinstance(self.reply_markup, types.InlineKeyboardMarkup):
            keyboard = self.reply_markup.inline_keyboard
            is_inline = True
        else:
            raise ValueError("The message doesn't contain any keyboard")

        if isinstance(x, int) and y is None:
            try:
                button = [
                    button
                    for row in keyboard
                    for button in row
                ][x]
            except IndexError:
                raise ValueError(f"The button at index {x} doesn't exist")
        elif isinstance(x, int) and isinstance(y, int):
            try:
                button = keyboard[y][x]
            except IndexError:
                raise ValueError(f"The button at position ({x}, {y}) doesn't exist")
        elif isinstance(x, str) and y is None:
            label = x.encode("utf-16", "surrogatepass").decode("utf-16")

            try:
                button = [
                    button
                    for row in keyboard
                    for button in row
                    if label == button.text
                ][0]
            except IndexError:
                raise ValueError(f"The button with label '{x}' doesn't exists")
        else:
            raise ValueError("Invalid arguments")

        if is_inline:
            if button.callback_data:
                return await self._client.request_callback_answer(
                    chat_id=self.chat.id,
                    message_id=self.id,
                    callback_data=button.callback_data,
                    timeout=timeout
                )
            elif button.callback_data_with_password:
                if password is None:
                    raise ValueError(
                        "Invalid argument passed"
                    )
                return await self._client.request_callback_answer(
                    chat_id=self.chat.id,
                    message_id=self.id,
                    callback_data=button.callback_data_with_password,
                    password=password,
                    timeout=timeout
                )
            elif button.url:
                return button.url
            elif button.login_url:
                tlu = button.login_url
                rieep = await self._client.resolve_peer(
                    self.chat.id
                )
                okduit = await self._client.invoke(
                    raw.functions.messages.RequestUrlAuth(
                        peer=rieep,
                        msg_id=self.id,
                        button_id=tlu.button_id,
                        url=tlu.url
                    )
                )
                tiudko = await self._client.invoke(
                    raw.functions.messages.AcceptUrlAuth(
                        write_allowed=request_write_access,
                        peer=rieep,
                        msg_id=self.id,
                        button_id=tlu.button_id,
                        url=tlu.url
                    )
                )
                return tiudko.url
            elif button.web_app:
                tlu = button.web_app
                whichbotchat = (
                    self.via_bot and
                    self.via_bot.id
                ) or (
                    self.from_user and
                    self.from_user.is_bot and
                    self.from_user.id
                ) or None
                if not whichbotchat:
                    raise ValueError(
                        "Invalid ChatBotType"
                    )
                rieep = await self._client.resolve_peer(
                    self.chat.id
                )
                ieepr = await self._client.resolve_peer(
                    whichbotchat
                )
                okduit = await self._client.invoke(
                    raw.functions.messages.RequestWebView(
                        peer=rieep,
                        bot=ieepr,
                        url=tlu.url,
                        platform=self._client.client_platform.value,
                        # TODO
                    )
                )
                return okduit.url
            elif button.user_id:
                return await self._client.get_chat(
                    button.user_id,
                    False
                )
            elif button.switch_inline_query:
                return button.switch_inline_query
            elif button.switch_inline_query_current_chat:
                return button.switch_inline_query_current_chat
            elif button.switch_inline_query_chosen_chat:
                return button.switch_inline_query_chosen_chat
            else:
                raise ValueError("This button is not supported yet")
        else:
            await self.reply(text=button, quote=quote)

    async def react(
        self,
        reaction: Union[
            int,
            str,
            list[Union[int, str, "types.ReactionType"]]
        ] = None,
        is_big: bool = False,
        add_to_recent: bool = True
    ) -> "types.MessageReactions":
        """Bound method *react* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.set_reaction(
                chat_id=chat_id,
                message_id=message.id,
                reaction=[ReactionTypeEmoji(emoji="👍")]
            )

        Example:
            .. code-block:: python

                # Send a reaction
                await message.react([ReactionTypeEmoji(emoji="👍")])

                # Retract a reaction
                await message.react()

        Parameters:
            reaction (``int`` | ``str`` | List of ``int`` OR ``str`` | List of :obj:`~pyrogram.types.ReactionType`, *optional*):
                New list of reaction types to set on the message.
                Pass None as emoji (default) to retract the reaction.

            is_big (``bool``, *optional*):
                Pass True to set the reaction with a big animation.
                Defaults to False.
            
            add_to_recent (``bool``, *optional*):
                Pass True if the reaction should appear in the recently used reactions.
                This option is applicable only for users.
                Defaults to True.
        Returns:
            On success, :obj:`~pyrogram.types.MessageReactions`: is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        sr = None

        if isinstance(reaction, list):
            sr = []
            for i in reaction:
                if isinstance(i, types.ReactionType):
                    sr.append(i)
                elif isinstance(i, int):
                    sr.append(types.ReactionTypeCustomEmoji(
                        custom_emoji_id=str(i)
                    ))
                else:
                    sr.append(types.ReactionTypeEmoji(
                        emoji=i
                    ))

        elif isinstance(reaction, int):
            sr = [
                types.ReactionTypeCustomEmoji(
                    custom_emoji_id=str(reaction)
                )
            ]

        elif isinstance(reaction, str):
            sr = [
                types.ReactionTypeEmoji(
                    emoji=reaction
                )
            ]

        return await self._client.set_reaction(
            chat_id=self.chat.id,
            message_id=self.id,
            reaction=sr,
            is_big=is_big,
            add_to_recent=add_to_recent
        )

    async def retract_vote(
        self,
    ) -> "types.Poll":
        """Bound method *retract_vote* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            client.retract_vote(
                chat_id=message.chat.id,
                message_id=message_id,
            )

        Example:
            .. code-block:: python

                message.retract_vote()

        Returns:
            :obj:`~pyrogram.types.Poll`: On success, the poll with the retracted vote is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.retract_vote(
            chat_id=self.chat.id,
            message_id=self.id
        )

    async def download(
        self,
        file_name: str = "",
        in_memory: bool = False,
        block: bool = True,
        idx: int = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> Optional[Union[str, "io.BytesIO", list[str], list["io.BytesIO"]]]:
        """Bound method *download* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.download_media(message)

        Example:
            .. code-block:: python

                await message.download()

        Parameters:
            file_name (``str``, *optional*):
                A custom *file_name* to be used instead of the one provided by Telegram.
                By default, all files are downloaded in the *downloads* folder in your working directory.
                You can also specify a path for downloading files in a custom location: paths that end with "/"
                are considered directories. All non-existent folders will be created automatically.

            in_memory (``bool``, *optional*):
                Pass True to download the media in-memory.
                A binary file-like object with its attribute ".name" set will be returned.
                Defaults to False.

            block (``bool``, *optional*):
                Blocks the code execution until the file has been downloaded.
                Defaults to True.

            idx (``int``, *optional*):
                In case of a :obj:`~pyrogram.types.PaidMediaInfo` with more than one ``paid_media``, the zero based index of the :obj:`~pyrogram.types.PaidMedia` to download. Raises ``IndexError`` if the index specified does not exist in the original ``message``.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            ``str`` | ``None`` | :obj:`io.BytesIO`: On success, the absolute path of the downloaded file is returned,
            otherwise, in case the download failed or was deliberately stopped with
            :meth:`~pyrogram.Client.stop_transmission`, None is returned.
            Otherwise, in case ``in_memory=True``, a binary file-like object with its attribute ".name" set is returned.
            If the message is a :obj:`~pyrogram.types.PaidMediaInfo` with more than one ``paid_media`` containing ``minithumbnail`` and ``idx`` is not specified, then a list of paths or binary file-like objects is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
            IndexError: In case of wrong value of ``idx``.
            ValueError: If the message doesn't contain any downloadable media.

        """
        return await self._client.download_media(
            message=self,
            file_name=file_name,
            in_memory=in_memory,
            block=block,
            idx=idx,
            progress=progress,
            progress_args=progress_args,
        )

    async def vote(
        self,
        option: int,
    ) -> "types.Poll":
        """Bound method *vote* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            client.vote_poll(
                chat_id=message.chat.id,
                message_id=message.id,
                option=1
            )

        Example:
            .. code-block:: python

                message.vote(6)

        Parameters:
            option (``int``):
                Index of the poll option you want to vote for (0 to 9).

        Returns:
            :obj:`~pyrogram.types.Poll`: On success, the poll with the chosen option is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.vote_poll(
            chat_id=self.chat.id,
            message_id=self.id,
            options=option
        )

    async def pin(self, disable_notification: bool = False, both_sides: bool = False) -> "types.Message":
        """Bound method *pin* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.pin_chat_message(
                chat_id=message.chat.id,
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await message.pin()

        Parameters:
            disable_notification (``bool``):
                Pass True, if it is not necessary to send a notification to all chat members about the new pinned
                message. Notifications are always disabled in channels.

            both_sides (``bool``, *optional*):
                Pass True to pin the message for both sides (you and recipient).
                Applicable to private chats only. Defaults to False.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the service message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.pin_chat_message(
            chat_id=self.chat.id,
            message_id=self.id,
            disable_notification=disable_notification,
            both_sides=both_sides
        )

    async def unpin(self) -> bool:
        """Bound method *unpin* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.unpin_chat_message(
                chat_id=message.chat.id,
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await message.unpin()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.unpin_chat_message(
            chat_id=self.chat.id,
            message_id=self.id
        )

    # BEGIN: the below properties were removed in `BOT API 7.0 <https://core.telegram.org/bots/api-changelog#december-29-2023>`_

    @property
    def forward_from(self) -> "types.User":
        log.warning(
            "This property is deprecated. "
            "Please use forward_origin instead"
        )
        return getattr(self.forward_origin, "sender_user", None)
    
    @property
    def forward_sender_name(self) -> str:
        log.warning(
            "This property is deprecated. "
            "Please use forward_origin instead"
        )
        return getattr(self.forward_origin, "sender_user_name", None)

    @property
    def forward_from_chat(self) -> "types.Chat":
        log.warning(
            "This property is deprecated. "
            "Please use forward_origin instead"
        )
        return getattr(
            self.forward_origin,
            "chat",
            getattr(
                self.forward_origin,
                "sender_chat",
                None
            )
        )

    @property
    def forward_from_message_id(self) -> int:
        log.warning(
            "This property is deprecated. "
            "Please use forward_origin instead"
        )
        return getattr(self.forward_origin, "message_id", None)

    @property
    def forward_signature(self) -> str:
        log.warning(
            "This property is deprecated. "
            "Please use forward_origin instead"
        )
        return getattr(self.forward_origin, "author_signature", None)
        
    @property
    def forward_date(self) -> datetime:
        log.warning(
            "This property is deprecated. "
            "Please use forward_origin instead"
        )
        return getattr(self.forward_origin, "date", None)

    # END: the below properties were removed in `BOT API 7.0 <https://core.telegram.org/bots/api-changelog#december-29-2023>`_

    async def read(self) -> bool:
        """Bound method *read* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.read_chat_history(
                chat_id=message.chat.id,
                max_id=message_id
            )

        Example:

            .. code-block:: python

                await message.read()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.

        """
        return await self._client.read_chat_history(
            chat_id=self.chat.id,
            max_id=self.id
        )

    async def view(self, force_read: bool = True) -> bool:
        """Bound method *view* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.view_messages(
                chat_id=message.chat.id,
                message_ids=message_id
            )

        Example:
            .. code-block:: python

                await message.view()

        Parameters:
            force_read (``bool``, *optional*):
                Pass True to mark as read the specified messages and also increment the view counter.

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.

        """
        return await self._client.view_messages(
            chat_id=self.chat.id,
            message_ids=self.id,
            force_read=force_read
        )

    async def translate(
        self,
        to_language_code: str
    ) -> "types.TranslatedText":
        """Bound method *translate* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.translate_message_text(
                chat_id=message.chat.id,
                message_ids=message_id,
                to_language_code="en"
            )

        Example:
            .. code-block:: python

                await message.translate("en")

        Parameters:
            to_language_code (``str``):
                Language code of the language to which the message is translated.
                Must be one of "af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "zh-CN", "zh", "zh-Hans", "zh-TW", "zh-Hant", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "he", "iw", "hi", "hmn", "hu", "is", "ig", "id", "in", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "ko", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ny", "or", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tl", "tg", "ta", "tt", "te", "th", "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy", "xh", "yi", "ji", "yo", "zu".

        Returns:
            :obj:`~pyrogram.types.TranslatedText`: The translated result is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.

        """
        return await self._client.translate_message_text(
            chat_id=self.chat.id,
            message_ids=self.id,
            to_language_code=to_language_code
        )


    async def pay(self) -> Union[
        bool,
        list["types.PaidMediaPhoto"],
        list["types.PaidMediaVideo"]
    ]:
        """Bound method *pay* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.send_payment_form(
                chat_id=message.chat.id,
                message_id=message_id
            )

        Example:
            .. code-block:: python

                await message.pay()

        Returns:
            ``bool`` | List of :obj:`~pyrogram.types.PaidMediaPhoto` | List of :obj:`~pyrogram.types.PaidMediaVideo`: On success, the list of bought photos and videos is returned.

        """
        return await self._client.send_payment_form(
            chat_id=self.chat.id,
            message_id=self.id
        )

    async def star(
        self,
        star_count: int = None,
        paid_reaction_type: "types.PaidReactionType" = None
    ) -> "types.MessageReactions":
        """Bound method *star* of :obj:`~pyrogram.types.Message`.

        Use as a shortcut for:

        .. code-block:: python

            await client.add_paid_message_reaction(
                chat_id=chat_id,
                message_id=message.id,
                star_count=1
            )

        Example:
            .. code-block:: python

                # Add a paid reaction to a message
                await message.star(1)

                # Add an anonymous paid reaction to a message
                await message.star(1, True)

        Parameters:
            star_count (``int``, *optional*):
                Number of Telegram Stars to be used for the reaction; 1-2500.

            paid_reaction_type (:obj:`~pyrogram.types.PaidReactionType`, *optional*):
                Type of the paid reaction; pass None if the user didn't choose reaction type explicitly, for example, the reaction is set from the message bubble.

        Returns:
            On success, :obj:`~pyrogram.types.MessageReactions`: is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.add_paid_message_reaction(
            chat_id=self.chat.id,
            message_id=self.id,
            star_count=star_count,
            paid_reaction_type=paid_reaction_type
        )
