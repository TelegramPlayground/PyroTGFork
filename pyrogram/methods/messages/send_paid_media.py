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
import os
import re

from datetime import datetime
from typing import Union, Optional

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.file_id import FileType
from .inline_session import get_session


class SendPaidMedia:
    async def send_paid_media(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        star_count: int,
        media: list[Union[
            "types.InputPaidMediaPhoto",
            "types.InputPaidMediaVideo"
        ]],
        payload: str = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        show_caption_above_media: bool = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        paid_message_star_count: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        business_connection_id: str = None,
        send_as: Union[int, str] = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        schedule_date: datetime = None
    ) -> "types.Message":
        """Use this method to send paid media.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel (in the format @channelusername).
                If the chat is a channel, all Telegram Star proceeds from this media will be credited to the chat's balance. Otherwise, they will be credited to the bot's balance.

            star_count (``int``):
                The number of Telegram Stars that must be paid to buy access to the media.

            media (List of :obj:`~pyrogram.types.InputPaidMedia`):
                A list describing the media to be sent; up to 10 items.
            
            payload (``str``, *optional*):
                Bot-defined paid media payload, 0-128 bytes. This will not be displayed to the user, use it for your internal processes.

            caption (``str``, *optional*):
                Media caption, 0-1024 characters after entities parsing.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            show_caption_above_media (``bool``, *optional*):
                Pass True, if the caption must be shown above the message media.            

            disable_notification (``bool``, *optional*):
                Sends the message silently. Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.

            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            paid_message_star_count (``int``, *optional*):
                The number of Telegram Stars the user agreed to pay to send the messages.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to
            
            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            schedule_date (:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent. Pass a :obj:`~datetime.datetime` object.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent message is returned.

        """
        multi_media = []

        peer = await self.resolve_peer(chat_id)
        for i in media:
            if isinstance(i, types.InputPaidMediaPhoto):
                if isinstance(i.media, str):
                    if os.path.isfile(i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaUploadedPhoto(
                                    file=await self.save_file(i.media)
                                )
                            )
                        )

                        media = raw.types.InputMediaPhoto(
                            id=raw.types.InputPhoto(
                                id=media.photo.id,
                                access_hash=media.photo.access_hash,
                                file_reference=media.photo.file_reference
                            )
                        )
                    elif re.match("^https?://", i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaPhotoExternal(
                                    url=i.media
                                )
                            )
                        )

                        media = raw.types.InputMediaPhoto(
                            id=raw.types.InputPhoto(
                                id=media.photo.id,
                                access_hash=media.photo.access_hash,
                                file_reference=media.photo.file_reference
                            )
                        )
                    else:
                        media = utils.get_input_media_from_file_id(i.media, FileType.PHOTO)
                else:
                    media = await self.invoke(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaUploadedPhoto(
                                file=await self.save_file(i.media)
                            )
                        )
                    )

                    media = raw.types.InputMediaPhoto(
                        id=raw.types.InputPhoto(
                            id=media.photo.id,
                            access_hash=media.photo.access_hash,
                            file_reference=media.photo.file_reference
                        )
                    )
            elif isinstance(i, types.InputPaidMediaVideo):
                video_cover_file = None
                if i.cover:
                    is_bytes_io = isinstance(i.cover, io.BytesIO)
                    is_uploaded_file = is_bytes_io or os.path.isfile(i.cover)
                    is_external_url = not is_uploaded_file and re.match("^https?://", i.cover)
                    if is_bytes_io and not hasattr(i.cover, "name"):
                        cover.name = "cover.jpg"

                    if is_uploaded_file:
                        video_cover_file = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                business_connection_id=business_connection_id,
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaUploadedPhoto(
                                    file=await self.save_file(i.cover)
                                )
                            )
                        )
                        video_cover_file = raw.types.InputPhoto(
                            id=video_cover_file.photo.id,
                            access_hash=video_cover_file.photo.access_hash,
                            file_reference=video_cover_file.photo.file_reference
                        )
                    elif is_external_url:
                        video_cover_file = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                business_connection_id=business_connection_id,
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaPhotoExternal(
                                    url=i.cover
                                )
                            )
                        )
                        video_cover_file = raw.types.InputPhoto(
                            id=video_cover_file.photo.id,
                            access_hash=video_cover_file.photo.access_hash,
                            file_reference=video_cover_file.photo.file_reference
                        )
                    else:
                        video_cover_file = (utils.get_input_media_from_file_id(i.cover, FileType.PHOTO)).id

                if isinstance(i.media, str):
                    if os.path.isfile(i.media):
                        attributes = [
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=i.supports_streaming or None,
                                duration=i.duration,
                                w=i.width,
                                h=i.height
                            ),
                            raw.types.DocumentAttributeFilename(file_name=os.path.basename(i.media))
                        ]
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaUploadedDocument(
                                    file=await self.save_file(i.media),
                                    thumb=await self.save_file(i.thumbnail),
                                    mime_type=self.guess_mime_type(i.media) or "video/mp4",
                                    nosound_video=True,
                                    attributes=attributes,
                                    video_cover=video_cover_file,
                                    video_timestamp=i.start_timestamp
                                )
                            )
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference
                            )
                        )
                    elif re.match("^https?://", i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaDocumentExternal(
                                    url=i.media,
                                    video_cover=video_cover_file,
                                    video_timestamp=i.start_timestamp
                                )
                            )
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference
                            )
                        )
                    else:
                        media = utils.get_input_media_from_file_id(i.media, FileType.VIDEO)
                        media.video_cover = video_cover_file
                        media.video_timestamp = i.start_timestamp
                else:
                    media = await self.invoke(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaUploadedDocument(
                                file=await self.save_file(i.media),
                                thumb=await self.save_file(i.thumbnail),
                                mime_type=self.guess_mime_type(getattr(i.media, "name", "video.mp4")) or "video/mp4",
                                attributes=[
                                    raw.types.DocumentAttributeVideo(
                                        supports_streaming=i.supports_streaming or None,
                                        duration=i.duration,
                                        w=i.width,
                                        h=i.height
                                    ),
                                    raw.types.DocumentAttributeFilename(file_name=getattr(i.media, "name", "video.mp4"))
                                ],
                                video_cover=video_cover_file,
                                video_timestamp=i.start_timestamp
                            )
                        )
                    )

                    media = raw.types.InputMediaDocument(
                        id=raw.types.InputDocument(
                            id=media.document.id,
                            access_hash=media.document.access_hash,
                            file_reference=media.document.file_reference
                        )
                    )
            else:
                raise ValueError(f"{i.__class__.__name__} is not a supported type for send_paid_media")
            multi_media.append(media)
        
        rpc = raw.functions.messages.SendMedia(
            peer=await self.resolve_peer(chat_id),
            media=raw.types.InputMediaPaidMedia(
                stars_amount=star_count,
                extended_media=multi_media,
                payload=payload
            ),
            silent=disable_notification or None,
            random_id=self.rnd_id(),
            send_as=await self.resolve_peer(send_as) if send_as else None,
            schedule_date=utils.datetime_to_timestamp(schedule_date),
            reply_markup=await reply_markup.write(self) if reply_markup else None,
            noforwards=protect_content,
            allow_paid_floodskip=allow_paid_broadcast,
            allow_paid_stars=paid_message_star_count,
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
        if business_connection_id:
            r = await session.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    query=rpc,
                    connection_id=business_connection_id
                )
            )
            # await session.stop()
        else:
            r = await self.invoke(rpc, sleep_threshold=60)
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
