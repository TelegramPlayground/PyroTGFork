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

import os
from typing import Callable, Union

import pyrogram
from pyrogram import StopTransmission, enums, raw, types, utils
from pyrogram.errors import FilePartMissing


class PostStory:
    async def post_story(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        content: "types.InputStoryContent",
        active_period: int = None,
        caption: str = None,
        parse_mode: "enums.ParseMode" = None,
        caption_entities: list["types.MessageEntity"] = None,
        areas: list["types.StoryArea"] = None,
        post_to_chat_page: bool = None,
        protect_content: bool = None,
        business_connection_id: str = None,
        privacy_settings: "types.StoryPrivacySettings" = None,
        from_story_chat_id: Union[int, str] = None,
        from_story_id: int = None,
        progress: Callable = None,
        progress_args: tuple = (),
    ) -> "types.Story":
        """Posts a new story on behalf of a chat.

        .. include:: /_includes/usable-by/users.rst

        Requires can_post_stories right for supergroup and channel chats.

        .. include:: /_includes/usable-by/bots.rst

        Requires the can_manage_stories business bot right.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".

            content (:obj:`~pyrogram.types.InputStoryContent`):
                Content of the story.

            active_period (``int``, *optional*):
                Period after which the story is moved to the archive, in seconds; must be one of 6 * 3600, 12 * 3600, 86400, or 2 * 86400.

            caption (``str``, *optional*):
                Caption of the story, 0-2048 characters after entities parsing.
            
            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            areas (List of :obj:`~pyrogram.types.StoryArea`, *optional*):
                List of of clickable areas to be shown on the story.

            post_to_chat_page (``bool``, *optional*):
                Pass True to keep the story accessible after it expires.
            
            protect_content (``bool``, *optional*):
                Pass True if the content of the story must be protected from forwarding and screenshotting.

            business_connection_id (``str``):
                Unique identifier of the business connection.

            privacy_settings (:obj:`~pyrogram.types.StoryPrivacySettings`, *optional*):
                The privacy settings for the story; ignored for stories sent to supergroup and channel chats.
                Defaults to :obj:`~pyrogram.types.StoryPrivacySettingsEveryone`.

            from_story_chat_id (``int`` | ``str``, *optional*):
                Full identifier of the original story, which content was used to create the story; pass None if the story isn't repost of another story.
                Identifier of the chat that posted the story.

            from_story_id (``int``, *optional*):
                Full identifier of the original story, which content was used to create the story; pass None if the story isn't repost of another story.
                Unique story identifier among stories of the given sender.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Returns:
            :obj:`~pyrogram.types.Story` a single story is returned.

        Example:
            .. code-block:: python

                # Post story to your profile
                await app.post_story("me", InputStoryContentPhoto("story.png"), caption='My new story!')

        Raises:
            ValueError: In case of invalid arguments.
            RPCError: In case of Telegram RPCError.

        """
        if business_connection_id:
            business_connection = self.business_user_connection_cache[business_connection_id]
            if not business_connection:
                business_connection = await self.get_business_connection(business_connection_id)

            return await self.post_story(
                chat_id=business_connection.user_chat_id,
                content=content,
                active_period=active_period,
                caption=caption,
                parse_mode=parse_mode,
                caption_entities=caption_entities,
                areas=areas,
                post_to_chat_page=post_to_chat_page,
                protect_content=protect_content,
                privacy_settings=privacy_settings,
                from_story_chat_id=from_story_chat_id,
                from_story_id=from_story_id,
                progress=progress,
                progress_args=progress_args
            )

        message, entities = (await utils.parse_text_entities(self, caption, parse_mode, caption_entities)).values()

        media = None
        thumb = None
        mime_type = None
        if isinstance(content, types.InputStoryContentPhoto):
            media = content.photo
            thumb = content.thumbnail
            mime_type = "image/jpg"
        elif isinstance(content, types.InputStoryContentVideo):
            media = content.video
            thumb = content.thumbnail
            mime_type = "video/mp4"
        else:
            raise ValueError("invalid content")

        try:
            if isinstance(media, str):
                if os.path.isfile(media):
                    file = await self.save_file(media, progress=progress, progress_args=progress_args)
                    thumb = await self.save_file(thumb) if thumb else None
                    if isinstance(content, types.InputStoryContentVideo):
                        media = raw.types.InputMediaUploadedDocument(
                            mime_type=mime_type,
                            file=file,
                            thumb=thumb,
                            attributes=[
                                raw.types.DocumentAttributeVideo(
                                    supports_streaming=content.supports_streaming or None,
                                    duration=content.duration,
                                    w=content.width,
                                    h=content.height,
                                ),
                                raw.types.DocumentAttributeFilename(file_name=content.file_name or os.path.basename(media))
                            ]
                        )
                    else:
                        media = raw.types.InputMediaUploadedPhoto(
                            file=file,
                        )
                else:
                    media = utils.get_input_media_from_file_id(media)
            else:
                file = await self.save_file(media, progress=progress, progress_args=progress_args)
                thumb = await self.save_file(thumb) if thumb else None
                if isinstance(content, types.InputStoryContentVideo):
                    media = raw.types.InputMediaUploadedDocument(
                        mime_type=mime_type,
                        file=file,
                        thumb=thumb,
                        attributes=[
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=content.supports_streaming or None,
                                duration=content.duration,
                                w=content.width,
                                h=content.height,
                            ),
                            raw.types.DocumentAttributeFilename(file_name=content.file_name or media.name)
                        ]
                    )
                else:
                    media = raw.types.InputMediaUploadedPhoto(
                        file=file,
                    )

            privacy_rules = []
            if privacy_settings:
                privacy_rules += (await privacy_settings.write(self))
            else:
                privacy_rules += (await (types.StoryPrivacySettingsEveryone()).write(self))

            while True:
                try:
                    r = await self.invoke(
                        raw.functions.stories.SendStory( 
                            peer=await self.resolve_peer(chat_id),
                            media=media,
                            privacy_rules=privacy_rules,
                            random_id=self.rnd_id(),
                            pinned=post_to_chat_page,
                            noforwards=protect_content,
                            media_areas=[await area.write(self) for area in (areas or [])] or None,
                            caption=message,
                            entities=entities,
                            period=active_period,
                            # fwd_modified=True if from_story_id else None,
                            fwd_from_id=await self.resolve_peer(from_story_chat_id) if from_story_chat_id else None,
                            fwd_from_story=from_story_id,
                        )
                    )
                except FilePartMissing as e:
                    await self.save_file(media, file_id=file.id, file_part=e.value)
                else:
                    for i in r.updates:
                        if isinstance(i, raw.types.UpdateStory):
                            return await types.Story._parse(
                                self,
                                {i.id: i for i in r.users},
                                {i.id: i for i in r.chats},
                                None, None,
                                i,
                                i.story,
                                i.peer
                            )
        except StopTransmission:
            return None
