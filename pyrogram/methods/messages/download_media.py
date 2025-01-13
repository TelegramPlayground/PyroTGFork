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

import asyncio
import io
import os
import re
from datetime import datetime
from typing import Callable, Optional, Union 

import pyrogram
from pyrogram import enums, types, utils
from pyrogram.file_id import FileId, FileType, PHOTO_TYPES

DEFAULT_DOWNLOAD_DIR = "downloads/"


class DownloadMedia:
    async def download_media(
        self: "pyrogram.Client",
        message: Union[
            "types.Message",
            "types.Audio",
            "types.Document",
            "types.Photo",
            "types.Sticker",
            "types.Video",
            "types.Animation",
            "types.Voice",
            "types.VideoNote",
            # TODO
            "types.Story",
            "types.PaidMediaInfo",
            "types.PaidMediaPhoto",
            "types.PaidMediaVideo",
            "types.Thumbnail",
            "types.StrippedThumbnail",
            "types.PaidMediaPreview",
            str,
        ],
        file_name: str = DEFAULT_DOWNLOAD_DIR,
        in_memory: bool = False,
        block: bool = True,
        idx: int = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> Optional[Union[str, "io.BytesIO", list[str], list["io.BytesIO"]]]:
        """Download the media from a message.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            message (:obj:`~pyrogram.types.Message` | :obj:`~pyrogram.types.Audio` | :obj:`~pyrogram.types.Document` | :obj:`~pyrogram.types.Photo` | :obj:`~pyrogram.types.Sticker` | :obj:`~pyrogram.types.Video` | :obj:`~pyrogram.types.Animation` | :obj:`~pyrogram.types.Voice` | :obj:`~pyrogram.types.VideoNote` | :obj:`~pyrogram.types.Story` | :obj:`~pyrogram.types.PaidMediaInfo` | :obj:`~pyrogram.types.PaidMediaPhoto` | :obj:`~pyrogram.types.PaidMediaVideo` | :obj:`~pyrogram.types.Thumbnail` | :obj:`~pyrogram.types.StrippedThumbnail` | :obj:`~pyrogram.types.PaidMediaPreview` | :obj:`~pyrogram.types.Story` | ``str``):
                Pass a Message containing the media, the media itself (message.audio, message.video, ...) or a file id
                as string.

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

        Example:
            Download media to file

            .. code-block:: python

                # Download from Message
                await app.download_media(message)

                # Download from file id
                await app.download_media(message.photo.file_id)

                # Keep track of the progress while downloading
                async def progress(current, total):
                    print(f"{current * 100 / total:.1f}%")

                await app.download_media(message, progress=progress)

            Download media in-memory

            .. code-block:: python

                file = await app.download_media(message, in_memory=True)

                file_name = file.name
                file_bytes = bytes(file.getbuffer())
        """

        medium = [message]

        if isinstance(message, types.Message):
            if message.new_chat_photo:
                medium = [message.new_chat_photo]

            elif (
                not (self.me and self.me.is_bot) and
                message.story or message.reply_to_story
            ):
                story_media = message.story or message.reply_to_story or None
                if story_media and story_media.media:
                    medium = [getattr(story_media, story_media.media.value, None)]
                else:
                    medium = []

            elif message.paid_media:
                if any([isinstance(paid_media, (types.PaidMediaPhoto, types.PaidMediaVideo)) for paid_media in message.paid_media.paid_media]):
                    medium = [getattr(paid_media, "photo", (getattr(paid_media, "video", None))) for paid_media in message.paid_media.paid_media]
                elif any([isinstance(paid_media, types.PaidMediaPreview) for paid_media in message.paid_media.paid_media]):
                    medium = [getattr(getattr(paid_media, "minithumbnail"), "data", None) for paid_media in message.paid_media.paid_media]
                else:
                    medium = []

            else:
                if message.media:
                    medium = [getattr(message, message.media.value, None)]
                else:
                    medium = []

        elif isinstance(message, types.Story):
            if (self.me and self.me.is_bot):
                raise ValueError("This method cannot be used by bots")
            else:
                if medium.media:
                    medium = [getattr(message, message.media.value, None)]
                else:
                    medium = []

        elif isinstance(message, types.PaidMediaInfo):
            if any([isinstance(paid_media, (types.PaidMediaPhoto, types.PaidMediaVideo)) for paid_media in message.paid_media]):
                medium = [getattr(paid_media, "photo", (getattr(paid_media, "video", None))) for paid_media in message.paid_media]
            elif any([isinstance(paid_media, types.PaidMediaPreview) for paid_media in message.paid_media]):
                medium = [getattr(getattr(paid_media, "minithumbnail"), "data", None) for paid_media in message.paid_media]
            else:
                medium = []

        elif isinstance(message, types.PaidMediaPhoto):
            medium = [message.photo]

        elif isinstance(message, types.PaidMediaVideo):
            medium = [message.video]

        elif isinstance(message, types.PaidMediaPreview):
            medium = [getattr(getattr(message, "minithumbnail"), "data", None)]
            
        elif isinstance(message, types.StrippedThumbnail):
            medium = [message.data]
        
        elif isinstance(message, types.Thumbnail):
            medium = [message]

        elif isinstance(message, str):
            medium = [message]

        medium = types.List(filter(lambda x: x is not None, medium))

        if len(medium) == 0:
            raise ValueError(
                f"The message {message if isinstance(message, str) else message.id} doesn't contain any downloadable media"
            )

        if idx is not None:
            medium = [medium[idx]]

        dledmedia = []

        for media in medium:
            if isinstance(media, bytes):
                thumb = utils.from_inline_bytes(
                    utils.expand_inline_bytes(
                        media
                    )
                )
                if in_memory:
                    dledmedia.append(thumb)
                    continue

                directory, file_name = os.path.split(file_name)
                file_name = file_name or thumb.name

                if not os.path.isabs(file_name):
                    directory = self.PARENT_DIR / (directory or DEFAULT_DOWNLOAD_DIR)

                os.makedirs(directory, exist_ok=True) if not in_memory else None
                temp_file_path = os.path.abspath(re.sub("\\\\", "/", os.path.join(directory, file_name)))

                with open(temp_file_path, "wb") as file:
                    file.write(thumb.getbuffer())

                dledmedia.append(temp_file_path)
                continue

            elif isinstance(media, str):
                file_id_str = media
            else:
                file_id_str = media.file_id

            file_id_obj = FileId.decode(file_id_str)

            file_type = file_id_obj.file_type
            media_file_name = getattr(media, "file_name", "")  # TODO
            file_size = getattr(media, "file_size", 0)
            mime_type = getattr(media, "mime_type", "")
            date = getattr(media, "date", None)

            directory, file_name = os.path.split(file_name)
            # TODO
            file_name = file_name or media_file_name or ""

            if not os.path.isabs(file_name):
                directory = self.WORKDIR / (directory or DEFAULT_DOWNLOAD_DIR)

            if not file_name:
                guessed_extension = self.guess_extension(mime_type)

                if file_type in PHOTO_TYPES:
                    extension = ".jpg"
                elif file_type == FileType.VOICE:
                    extension = guessed_extension or ".ogg"
                elif file_type in (FileType.VIDEO, FileType.ANIMATION, FileType.VIDEO_NOTE):
                    extension = guessed_extension or ".mp4"
                elif file_type == FileType.DOCUMENT:
                    extension = guessed_extension or ".zip"
                elif file_type == FileType.STICKER:
                    extension = guessed_extension or ".webp"
                elif file_type == FileType.AUDIO:
                    extension = guessed_extension or ".mp3"
                else:
                    extension = ".unknown"

                file_name = "{}_{}_{}{}".format(
                    FileType(file_id_obj.file_type).name.lower(),
                    (date or datetime.now()).strftime("%Y-%m-%d_%H-%M-%S"),
                    self.rnd_id(),
                    extension
                )

            downloader = self.handle_download(
                (file_id_obj, directory, file_name, in_memory, file_size, progress, progress_args)
            )

            if block:
                dledmedia.append(await downloader)
            else:
                asyncio.get_event_loop().create_task(downloader)

        return types.List(dledmedia) if block and len(dledmedia) > 1  else dledmedia[0] if block and len(dledmedia) == 1 else None
