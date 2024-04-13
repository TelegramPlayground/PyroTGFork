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
from typing import List, Union, Callable

import pyrogram
from pyrogram import raw, utils, types, enums
from ..object import Object
from ..update import Update
from .message import Str
from pyrogram.errors import RPCError


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

        date = None
        expire_date = None
        media = None
        has_protected_content = None
        photo = None
        video = None
        edited = None
        pinned = None
        caption = None
        caption_entities = None
        views = None
        forwards = None
        reactions = None
        skipped = None
        deleted = None

        # TODO: investigate a bug here
        if story_media:
            if story_media.peer:
                raw_peer_id = utils.get_peer_id(story_media.peer)
                chat = await client.get_chat(raw_peer_id, False)
            story_id = getattr(story_media, "id", None)
        if reply_story:
            if reply_story.peer:
                raw_peer_id = utils.get_peer_id(reply_story.peer)
                chat = await client.get_chat(raw_peer_id, False)
            story_id = getattr(reply_story, "story_id", None)
        if story_id and not client.me.is_bot:
            try:
                story_item = (
                    await client.invoke(
                        raw.functions.stories.GetStoriesByID(
                            peer=await client.resolve_peer(raw_peer_id),
                            id=[story_id]
                        )
                    )
                ).stories[0]
            except (RPCError,IndexError):
                pass
            else:
                if isinstance(story_item, raw.types.StoryItemDeleted):
                    deleted = True
                elif isinstance(story_item, raw.types.StoryItemSkipped):
                    skipped = True
                else:
                    date = utils.timestamp_to_datetime(story_item.date)
                    expire_date = utils.timestamp_to_datetime(story_item.expire_date)
                    if isinstance(story_item.media, raw.types.MessageMediaPhoto):
                        photo = types.Photo._parse(client, story_item.media.photo, story_item.media.ttl_seconds)
                        media = enums.MessageMediaType.PHOTO
                    elif isinstance(story_item.media, raw.types.MessageMediaDocument):
                        doc = story_item.media.document
                        attributes = {type(i): i for i in doc.attributes}
                        video_attributes = attributes.get(raw.types.DocumentAttributeVideo, None)
                        video = types.Video._parse(client, doc, video_attributes, None)
                        media = enums.MessageMediaType.VIDEO
                    has_protected_content = story_item.noforwards
                    edited = story_item.edited
                    pinned = story_item.pinned
                    entities = [e for e in (types.MessageEntity._parse(client, entity, {}) for entity in story_item.entities) if e]
                    caption = Str(story_item.caption or "").init(entities) or None
                    caption_entities = entities or None
                    if story_item.views:
                        views = getattr(story_item.views, "views_count", None)
                        forwards = getattr(story_item.views, "forwards_count", None)
                        reactions = [
                            types.Reaction._parse_count(client, reaction)
                            for reaction in getattr(story_item.views, "reactions", [])
                        ] or None
        return Story(
            client=client,
            _raw=story_media,
            id=story_id,
            chat=chat,
            date=date,
            expire_date=expire_date,
            media=media,
            has_protected_content=has_protected_content,
            photo=photo,
            video=video,
            edited=edited,
            pinned=pinned,
            caption=caption,
            caption_entities=caption_entities,
            views=views,
            forwards=forwards,
            reactions=reactions,
            skipped=skipped,
            deleted=deleted
        )

    async def react(
        self,
        reaction: Union[
            int,
            str
        ] = None,
        add_to_recent: bool = True
    ) -> "types.MessageReactions":
        """Bound method *react* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.set_reaction(
                chat_id=chat_id,
                story_id=message.id,
                reaction=[ReactionTypeEmoji(emoji="👍")]
            )

        Example:
            .. code-block:: python

                # Send a reaction
                await story.react([ReactionTypeEmoji(emoji="👍")])

                # Retract a reaction
                await story.react()

        Parameters:
            reaction (``int`` | ``str``, *optional*):
                New list of reaction types to set on the message.
                Pass None as emoji (default) to retract the reaction.

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

        if isinstance(reaction, List):
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
            story_id=self.id,
            reaction=sr,
            add_to_recent=add_to_recent
        )

    async def download(
        self,
        file_name: str = "",
        in_memory: bool = False,
        block: bool = True,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> str:
        """Bound method *download* of :obj:`~pyrogram.types.Story`.

        Use as a shortcut for:

        .. code-block:: python

            await client.download_media(story)

        Example:
            .. code-block:: python

                await story.download()

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
            On success, the absolute path of the downloaded file as string is returned, None otherwise.

        Raises:
            RPCError: In case of a Telegram RPC error.
            ``ValueError``: If the message doesn't contain any downloadable media
        """
        return await self._client.download_media(
            message=self,
            file_name=file_name,
            in_memory=in_memory,
            block=block,
            progress=progress,
            progress_args=progress_args,
        )
