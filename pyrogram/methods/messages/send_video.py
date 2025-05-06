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

import logging
import io
import os
import re
from datetime import datetime
from typing import Union, Optional, Callable

import pyrogram
from pyrogram import StopTransmission, enums, raw, types, utils
from pyrogram.errors import FilePartMissing
from pyrogram.file_id import FileType
from .inline_session import get_session

log = logging.getLogger(__name__)


class SendVideo:
    async def send_video(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        video: Union[str, "io.BytesIO"],
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
        paid_message_star_count: int = None,
        message_thread_id: int = None,
        business_connection_id: str = None,
        send_as: Union[int, str] = None,
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
        schedule_date: datetime = None,
        reply_to_message_id: int = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> Optional["types.Message"]:
        """Send video files.

        .. note::

            Starting December 1, 2024 messages with video that are sent, copied or forwarded to groups and channels with a sufficiently large audience can be automatically scheduled by the server until the respective video is reencoded. Such messages will have ``scheduled`` property set and beware of using the correct :doc:`Message Identifiers <../../topics/message-identifiers>` when using such :obj:`~pyrogram.types.Message` objects.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            video (``str`` | :obj:`io.BytesIO`):
                Video to send.
                Pass a file_id as string to send a video that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a video from the Internet,
                pass a file path as string to upload a new video that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

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

            paid_message_star_count (``int``, *optional*):
                The number of Telegram Stars the user agreed to pay to send the messages.

            message_thread_id (``int``, *optional*):
                If the message is in a thread, ID of the original message.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

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
            :obj:`~pyrogram.types.Message` | ``None``: On success, the sent video message is returned, otherwise, in
            case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned.

        Example:
            .. code-block:: python

                # Send video by uploading from local file
                await app.send_video("me", "video.mp4")

                # Add caption to the video
                await app.send_video("me", "video.mp4", caption="video caption")

                # Send self-destructing video
                await app.send_video("me", "video.mp4", ttl_seconds=10)

                # Send view-once video
                await app.send_video("me", "video.mp4", view_once=True)

                # Keep track of the progress while uploading
                async def progress(current, total):
                    print(f"{current * 100 / total:.1f}%")

                await app.send_video("me", "video.mp4", progress=progress)
        """

        if reply_to_message_id and reply_parameters:
            raise ValueError(
                "Parameters `reply_to_message_id` and `reply_parameters` are mutually "
                "exclusive."
            )
        
        if reply_to_message_id is not None:
            log.warning(
                "This property is deprecated. "
                "Please use reply_parameters instead"
            )
            reply_parameters = types.ReplyParameters(message_id=reply_to_message_id)

        file = None
        ttl_seconds = 0x7FFFFFFF if view_once else ttl_seconds

        coverfile = None
        if cover:
            is_bytes_io = isinstance(cover, io.BytesIO)
            is_uploaded_file = is_bytes_io or os.path.isfile(cover)
            is_external_url = not is_uploaded_file and re.match("^https?://", cover)

            if is_bytes_io and not hasattr(cover, "name"):
                cover.name = "cover.jpg"
            if is_uploaded_file:
                coverfile = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        business_connection_id=business_connection_id,
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedPhoto(
                            file=await self.save_file(cover)
                        )
                    )
                )
                coverfile = raw.types.InputPhoto(
                    id=coverfile.photo.id,
                    access_hash=coverfile.photo.access_hash,
                    file_reference=coverfile.photo.file_reference
                )
            elif is_external_url:
                coverfile = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        business_connection_id=business_connection_id,
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaPhotoExternal(
                            url=cover
                        )
                    )
                )
                coverfile = raw.types.InputPhoto(
                    id=coverfile.photo.id,
                    access_hash=coverfile.photo.access_hash,
                    file_reference=coverfile.photo.file_reference
                )
            else:
                coverfile = (utils.get_input_media_from_file_id(cover, FileType.PHOTO)).id

        try:
            if isinstance(video, str):
                if os.path.isfile(video):
                    file = await self.save_file(video, progress=progress, progress_args=progress_args)
                    thumb = await self.save_file(thumb)
                    media = raw.types.InputMediaUploadedDocument(
                        mime_type=self.guess_mime_type(video) or "video/mp4" if mime_type is None else mime_type,
                        file=file,
                        ttl_seconds=ttl_seconds,
                        nosound_video=True,
                        spoiler=has_spoiler,
                        thumb=thumb,
                        attributes=[
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=supports_streaming or None,
                                duration=duration,
                                w=width,
                                h=height
                            ),
                            raw.types.DocumentAttributeFilename(file_name=file_name or os.path.basename(video))
                        ],
                        video_cover=coverfile,
                        video_timestamp=start_timestamp
                    )
                elif re.match("^https?://", video):
                    media = raw.types.InputMediaDocumentExternal(
                        url=video,
                        ttl_seconds=ttl_seconds,
                        spoiler=has_spoiler,
                        video_cover=coverfile,
                        video_timestamp=start_timestamp
                    )
                else:
                    media = utils.get_input_media_from_file_id(
                        video,
                        FileType.VIDEO,
                        ttl_seconds=ttl_seconds,
                        has_spoiler=has_spoiler
                    )
                    media.video_cover = coverfile
                    media.video_timestamp = start_timestamp
                    
            else:
                file = await self.save_file(video, progress=progress, progress_args=progress_args)
                thumb = await self.save_file(thumb)
                media = raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(file_name or video.name) or "video/mp4" if mime_type is None else mime_type,
                    file=file,
                    ttl_seconds=ttl_seconds,
                    spoiler=has_spoiler,
                    thumb=thumb,
                    attributes=[
                        raw.types.DocumentAttributeVideo(
                            supports_streaming=supports_streaming or None,
                            duration=duration,
                            w=width,
                            h=height
                        ),
                        raw.types.DocumentAttributeFilename(file_name=file_name or video.name)
                    ],
                    video_cover=coverfile,
                    video_timestamp=start_timestamp
                )

            reply_to = await utils._get_reply_message_parameters(
                self,
                message_thread_id,
                reply_parameters
            )
            rpc = raw.functions.messages.SendMedia(
                peer=await self.resolve_peer(chat_id),
                media=media,
                silent=disable_notification or None,
                reply_to=reply_to,
                random_id=self.rnd_id(),
                send_as=await self.resolve_peer(send_as) if send_as else None,
                schedule_date=utils.datetime_to_timestamp(schedule_date),
                noforwards=protect_content,
                allow_paid_floodskip=allow_paid_broadcast,
                allow_paid_stars=paid_message_star_count,
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                effect=message_effect_id,
                invert_media=show_caption_above_media,
                **await utils.parse_text_entities(self, caption, parse_mode, caption_entities)
            )
            session = None
            business_connection = None
            if business_connection_id:
                business_connection = self.business_user_connection_cache[business_connection_id]
                if not business_connection:
                    business_connection = await self.get_business_connection(business_connection_id)
                session = await get_session(
                    self,
                    business_connection._raw.connection.dc_id
                )

            while True:
                try:
                    if business_connection_id:
                        r = await session.invoke(
                            raw.functions.InvokeWithBusinessConnection(
                                query=rpc,
                                connection_id=business_connection_id
                            )
                        )
                        # await session.stop()
                    else:
                        r = await self.invoke(rpc)
                except FilePartMissing as e:
                    await self.save_file(video, file_id=file.id, file_part=e.value)
                else:
                    for i in r.updates:
                        if isinstance(
                            i,
                            (
                                raw.types.UpdateNewMessage,
                                raw.types.UpdateNewChannelMessage,
                                raw.types.UpdateNewScheduledMessage
                            )
                        ):
                            return await types.Message._parse(
                                self, i.message,
                                {i.id: i for i in r.users},
                                {i.id: i for i in r.chats},
                                is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage),
                                replies=self.fetch_replies
                            )
                        elif isinstance(
                            i,
                            (
                                raw.types.UpdateBotNewBusinessMessage
                            )
                        ):
                            return await types.Message._parse(
                                self,
                                i.message,
                                {i.id: i for i in r.users},
                                {i.id: i for i in r.chats},
                                business_connection_id=getattr(i, "connection_id", business_connection_id),
                                raw_reply_to_message=i.reply_to_message,
                                replies=0
                            )
        except StopTransmission:
            return None
