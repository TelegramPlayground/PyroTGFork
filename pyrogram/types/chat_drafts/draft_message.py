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
from typing import Optional, Union

import pyrogram
from pyrogram import raw, types, utils, enums
from ..object import Object
from ..messages_and_media.message import Str


class DraftMessage(Object):
    """Contains information about a message draft.

    Parameters:
        reply_to_message_id (``int``, *optional*):
            The id of the message which this draft directly replied to.

        reply_to_message (:obj:`~pyrogram.types.Message`, *optional*):
            Information about the message to be replied.
        
        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the message was sent.

        text (``str``, *optional*):
            For text messages, the actual UTF-8 text of the message, 0-4096 characters.
            If the message contains entities (bold, italic, ...) you can access *text.markdown* or
            *text.html* to get the marked up message text. In case there is no entity, the fields
            will contain the same text as *text*.

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text.

        link_preview_options (:obj:`~pyrogram.types.LinkPreviewOptions`, *optional*):
            Options used for link preview generation for the draft message, if it is a text message and link preview options were changed.

        effect_id (``str``, *optional*):
            Unique identifier of the message effect added to the message. Use :meth:`~pyrogram.Client.get_message_effects` to get the list of available message effect ids.

        video_note (:obj:`~pyrogram.types.VideoNote`, *optional*):
            Message is a video note, information about the video message.

        voice (:obj:`~pyrogram.types.Voice`, *optional*):
            Message is a voice message, information about the file.

        show_caption_above_media (``bool``, *optional*):
            True, if the caption must be shown above the message media.
        
        media (:obj:`~pyrogram.enums.MessageMediaType`, *optional*):
            The message is a media message.
            This field will contain the enumeration type of the media message.
            You can use ``media = getattr(message, message.media.value)`` to access the media message.
        
        empty (``bool``, *optional*):
            The message is empty.
            A message can be empty in case it was deleted or you tried to retrieve a message that doesn't exist yet.

        chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Conversation the message belongs to. Can be None if unknown.

    """

    def __init__(
        self,
        *,
        reply_to_message_id: int = None,
        reply_to_message: "types.Message" = None,
        date: datetime = None,
        text: Str = None,
        entities: list["types.MessageEntity"] = None,
        link_preview_options: "types.LinkPreviewOptions" = None,
        effect_id: str = None,
        video_note: "types.VideoNote" = None,
        voice: "types.Voice" = None,
        show_caption_above_media: bool = None,
        media: "enums.MessageMediaType" = None,
        empty: bool = None,
        chat: "types.Chat" = None,
        
        _raw: "raw.types.DraftMessage" = None

    ):
        super().__init__()

        self.reply_to_message_id = reply_to_message_id
        self.reply_to_message = reply_to_message
        self.date = date
        self.text = text
        self.entities = entities
        self.link_preview_options = link_preview_options
        self.effect_id = effect_id
        self.video_note = video_note
        self.voice = voice
        self.show_caption_above_media = show_caption_above_media
        self.media = media
        self.empty = empty
        self.chat = chat

        self._raw = _raw


    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        raw_draft_message: Union[
            "raw.types.DraftMessage",
            "raw.types.DraftMessageEmpty",
        ],
        users: dict, # raw
        chats: dict, # raw 
    ) -> "DraftMessage":
        if not raw_draft_message:
            return None
        if isinstance(raw_draft_message, raw.types.DraftMessageEmpty):
            return DraftMessage(
                date=utils.timestamp_to_datetime(raw_draft_message.date),
                empty=True,
                _raw=raw_draft_message
            )

        entities = [types.MessageEntity._parse(client, entity, users) for entity in raw_draft_message.entities]
        entities = types.List(filter(lambda x: x is not None, entities))

        voice = None
        video_note = None
        link_preview_options = None
        web_page_url = None
        media = raw_draft_message.media
        media_type = None

        if media:
            if isinstance(media, raw.types.MessageMediaDocument):
                doc = media.document

                if isinstance(doc, raw.types.Document):
                    attributes = {type(i): i for i in doc.attributes}

                    file_name = getattr(
                        attributes.get(
                            raw.types.DocumentAttributeFilename, None
                        ), "file_name", None
                    )

                    if raw.types.DocumentAttributeVideo in attributes:
                        video_attributes = attributes[raw.types.DocumentAttributeVideo]

                        if video_attributes.round_message:
                            video_note = types.VideoNote._parse(client, doc, video_attributes, media.ttl_seconds)
                            media_type = enums.MessageMediaType.VIDEO_NOTE

                    elif raw.types.DocumentAttributeAudio in attributes:
                        audio_attributes = attributes[raw.types.DocumentAttributeAudio]

                        if audio_attributes.voice:
                            voice = types.Voice._parse(client, doc, audio_attributes, media.ttl_seconds)
                            media_type = enums.MessageMediaType.VOICE

            elif isinstance(media, raw.types.MessageMediaWebPage):
                if isinstance(media.webpage, raw.types.WebPage):
                    media_type = None
                    web_page_url = media.webpage.url
                elif isinstance(media.webpage, raw.types.WebPageEmpty):
                    media_type = None
                    web_page_url = getattr(media.webpage, "url", None)
                else:
                    media_type = None
                    web_page_url = utils.get_first_url(raw_draft_message)
                link_preview_options = types.LinkPreviewOptions._parse(
                    client,
                    media,
                    web_page_url,
                    getattr(raw_draft_message, "invert_media", False)
                )

        if (
            not link_preview_options and
            web_page_url
        ):
            link_preview_options = types.LinkPreviewOptions._parse(
                client,
                None,
                web_page_url,
                getattr(raw_draft_message, "invert_media", False)
            )

        draft_message = DraftMessage(
            date=utils.timestamp_to_datetime(raw_draft_message.date),
            text=(
                Str(raw_draft_message.message).init(entities) or None
            ),
            entities=entities or None,
            link_preview_options=link_preview_options,
            effect_id=raw_draft_message.effect,
            video_note=video_note,
            voice=voice,
            show_caption_above_media=getattr(raw_draft_message, "invert_media", False),
            media=media_type,
            _raw=raw_draft_message
        )
        # if raw_draft_message.reply_to:
        #     # TODO reply_to:flags.4?InputReplyTo
        #     draft_message.reply_to_message_id
        #     draft_message.reply_to_message 

        return draft_message
