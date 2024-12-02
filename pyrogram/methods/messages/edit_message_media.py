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
import io
import os
import re
from typing import Union

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.file_id import FileType

from .inline_session import get_session


class EditMessageMedia:
    async def edit_message_media(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        media: "types.InputMedia",
        reply_markup: "types.InlineKeyboardMarkup" = None,
        file_name: str = None,
        schedule_date: datetime = None,
        business_connection_id: str = None
    ) -> "types.Message":
        """Edit animation, audio, document, photo or video messages, or to add media to text messages.

        If a message is part of a message album, then it can be edited only to an audio for audio albums, only to a document for document albums and to a photo or a video otherwise. Otherwise, the
        message type can be changed arbitrarily.

        Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Message identifier in the chat specified in chat_id.

            media (:obj:`~pyrogram.types.InputMedia`):
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            file_name (``str``, *optional*):
                File name of the media to be sent. Not applicable to photos.
                Defaults to file's path basename.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message to be edited was sent

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the edited message is returned.

        Example:
            .. code-block:: python

                from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio

                # Replace the current media with a local photo
                await app.edit_message_media(chat_id, message_id,
                    InputMediaPhoto("new_photo.jpg"))

                # Replace the current media with a local video
                await app.edit_message_media(chat_id, message_id,
                    InputMediaVideo("new_video.mp4"))

                # Replace the current media with a local audio
                await app.edit_message_media(chat_id, message_id,
                    InputMediaAudio("new_audio.mp3"))
        """
        caption = media.caption
        parse_mode = media.parse_mode
        caption_entities = media.caption_entities

        show_caption_above_media = []

        message, entities = None, None

        if caption is not None:
            message, entities = (await utils.parse_text_entities(self, caption, parse_mode, caption_entities)).values()

        is_bytes_io = isinstance(media.media, io.BytesIO)
        is_uploaded_file = is_bytes_io or os.path.isfile(media.media)

        is_external_url = not is_uploaded_file and re.match("^https?://", media.media)

        if is_bytes_io and not hasattr(media.media, "name"):
            media.media.name = "media"

        if is_uploaded_file:
            filename_attribute = [
                raw.types.DocumentAttributeFilename(
                    file_name=file_name or (media.media.name if is_bytes_io else os.path.basename(media.media))
                )
            ]
        else:
            filename_attribute = []

        if isinstance(media, types.InputMediaPhoto):
            show_caption_above_media.append(media.show_caption_above_media)
            if is_uploaded_file:
                uploaded_media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        business_connection_id=None,  # TODO
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedPhoto(
                            file=await self.save_file(media.media),
                            spoiler=media.has_spoiler
                        )
                    )
                )

                media = raw.types.InputMediaPhoto(
                    id=raw.types.InputPhoto(
                        id=uploaded_media.photo.id,
                        access_hash=uploaded_media.photo.access_hash,
                        file_reference=uploaded_media.photo.file_reference
                    ),
                    spoiler=media.has_spoiler
                )
            elif is_external_url:
                media = raw.types.InputMediaPhotoExternal(
                    url=media.media,
                    spoiler=media.has_spoiler
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.PHOTO, has_spoiler=media.has_spoiler)
        elif isinstance(media, types.InputMediaVideo):
            show_caption_above_media.append(media.show_caption_above_media)
            if is_uploaded_file:
                uploaded_media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        business_connection_id=None,  # TODO
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedDocument(
                            mime_type=(None if is_bytes_io else self.guess_mime_type(media.media)) or "video/mp4",
                            thumb=await self.save_file(media.thumb),
                            spoiler=media.has_spoiler,
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.types.DocumentAttributeVideo(
                                    supports_streaming=media.supports_streaming or None,
                                    duration=media.duration,
                                    w=media.width,
                                    h=media.height
                                ),
                            ] + filename_attribute,
                            nosound_video=not media.disable_content_type_detection,
                            force_file=media.disable_content_type_detection or None,
                        )
                    )
                )

                media = raw.types.InputMediaDocument(
                    id=raw.types.InputDocument(
                        id=uploaded_media.document.id,
                        access_hash=uploaded_media.document.access_hash,
                        file_reference=uploaded_media.document.file_reference
                    ),
                    spoiler=media.has_spoiler
                )
            elif is_external_url:
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media,
                    spoiler=media.has_spoiler
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.VIDEO, has_spoiler=media.has_spoiler)
        elif isinstance(media, types.InputMediaAudio):
            if is_uploaded_file:
                media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        business_connection_id=None,  # TODO
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedDocument(
                            mime_type=(None if is_bytes_io else self.guess_mime_type(media.media)) or "audio/mpeg",
                            thumb=await self.save_file(media.thumb),
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.types.DocumentAttributeAudio(
                                    duration=media.duration,
                                    performer=media.performer,
                                    title=media.title
                                ),
                            ] + filename_attribute,
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
            elif is_external_url:
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.AUDIO)
        elif isinstance(media, types.InputMediaAnimation):
            show_caption_above_media.append(media.show_caption_above_media)
            if is_uploaded_file:
                uploaded_media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        business_connection_id=None,  # TODO
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedDocument(
                            mime_type=(None if is_bytes_io else self.guess_mime_type(media.media)) or "video/mp4",
                            thumb=await self.save_file(media.thumb),
                            spoiler=media.has_spoiler,
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.types.DocumentAttributeVideo(
                                    supports_streaming=True,
                                    duration=media.duration,
                                    w=media.width,
                                    h=media.height
                                ),
                                raw.types.DocumentAttributeAnimated(),
                            ] + filename_attribute,
                        )
                    )
                )

                media = raw.types.InputMediaDocument(
                    id=raw.types.InputDocument(
                        id=uploaded_media.document.id,
                        access_hash=uploaded_media.document.access_hash,
                        file_reference=uploaded_media.document.file_reference
                    ),
                    spoiler=media.has_spoiler
                )
            elif is_external_url:
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media,
                    spoiler=media.has_spoiler
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.ANIMATION, has_spoiler=media.has_spoiler)
        elif isinstance(media, types.InputMediaDocument):
            if is_uploaded_file:
                media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        business_connection_id=None,  # TODO
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedDocument(
                            mime_type=(None if is_bytes_io else self.guess_mime_type(media.media)) or "application/zip",
                            thumb=await self.save_file(media.thumb),
                            file=await self.save_file(media.media),
                            attributes=filename_attribute,
                            force_file=True
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
            elif is_external_url:
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.DOCUMENT)

        rpc = raw.functions.messages.EditMessage(
            peer=await self.resolve_peer(chat_id),
            id=message_id,
            media=media,
            reply_markup=await reply_markup.write(self) if reply_markup else None,
            message=message,
            entities=entities,
            invert_media=any(show_caption_above_media),
            schedule_date=utils.datetime_to_timestamp(schedule_date)
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
            r = await self.invoke(rpc)

        for i in r.updates:
            if isinstance(
                i,
                (
                    raw.types.UpdateEditMessage,
                    raw.types.UpdateEditChannelMessage,
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
                    raw.types.UpdateBotEditBusinessMessage
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
