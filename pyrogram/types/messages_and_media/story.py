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
from typing import List

import pyrogram
from pyrogram import raw, utils, types
from ..object import Object
from ..update import Update
from .message import Str


class Story(Object, Update):
    """This object represents a story.

    Parameters:
        chat (:obj:`~pyrogram.types.Chat`):
            Chat that posted the story.
        
        id (``int``):
            Unique identifier for the story in the chat.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the story was sent.
        
        expire_date (:py:obj:`~datetime.datetime`, *optional*):
            Date the story will be expired.
        
        media (:obj:`~pyrogram.enums.MessageMediaType`, *optional*):
            The media type of the Story.
            This field will contain the enumeration type of the media message.
            You can use ``media = getattr(story, story.media.value)`` to access the media message.

        has_protected_content (``bool``, *optional*):
            True, if the story can't be forwarded.

        photo (:obj:`~pyrogram.types.Photo`, *optional*):
            Story is a photo, information about the photo.

        video (:obj:`~pyrogram.types.Video`, *optional*):
            Story is a video, information about the video.

        edited (``bool``, *optional*):
           True, if the Story has been edited.

        pinned (``bool``, *optional*):
           True, if the Story is pinned.

        caption (``str``, *optional*):
            Caption for the Story, 0-1024 characters.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the caption.

        views (``int``, *optional*):
            Stories views.

        forwards (``int``, *optional*):
            Stories forwards.

        reactions (List of :obj:`~pyrogram.types.Reaction`):
            List of the reactions to this story.

        skipped (``bool``, *optional*):
            The story is skipped.
            A story can be skipped in case it was skipped.

        deleted (``bool``, *optional*):
            The story is deleted.
            A story can be deleted in case it was deleted or you tried to retrieve a story that doesn't exist yet.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chat: "types.Chat" = None,
        id: int = None,
        date: datetime = None,
        expire_date: datetime = None,
        media: "enums.MessageMediaType" = None,
        has_protected_content: bool = None,
        photo: "types.Photo" = None,
        video: "types.Video" = None,
        edited: bool = None,
        pinned: bool = None,
        caption: Str = None,
        caption_entities: List["types.MessageEntity"] = None,
        views: int = None,
        forwards: int = None,
        reactions: List["types.Reaction"] = None,
        skipped: bool = None,
        deleted: bool = None,
        _raw = None
    ):
        super().__init__(client)

        self.chat = chat
        self.id = id
        self.date = date
        self.expire_date = expire_date
        self.media = media
        self.has_protected_content = has_protected_content
        self.photo = photo
        self.video = video
        self.edited = edited
        self.pinned = pinned
        self.caption = caption
        self.caption_entities = caption_entities
        self.views = views
        self.forwards = forwards
        self.reactions = reactions
        self.skipped = skipped
        self.deleted = deleted
        self._raw = _raw


    @staticmethod
    async def _parse(
        client,
        chats: dict,
        story_media: "raw.types.MessageMediaStory",
        reply_story: "raw.types.MessageReplyStoryHeader"
    ) -> "Video":
        story_id = None
        chat = None
        if story_media:
            if story_media.peer:
                raw_peer_id = utils.get_peer_id(story_media.peer)
                chat = await client.get_chat(raw_peer_id)
            story_id = getattr(story_media, "id", None)
        if reply_story:
            if reply_story.peer:
                raw_peer_id = utils.get_peer_id(reply_story.peer)
                chat = await client.get_chat(raw_peer_id)
            story_id = getattr(reply_story, "story_id", None)
        return Story(
            client=client,
            _raw=story_media,
            id=story_id,
            chat=chat
        )
