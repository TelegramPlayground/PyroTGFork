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
from typing import Callable, Optional, Union

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.file_id import FileType

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

from .input_media import InputMedia

log = logging.getLogger(__name__)


class InputMediaPhoto(InputMedia):
    """A photo to be sent.

    Parameters:
        media (``str`` | :obj:`io.BytesIO`):
            Photo to send.
            Pass a file_id as string to send a photo that exists on the Telegram servers or
            pass a file path as string to upload a new photo that exists on your local machine or
            pass a binary file-like object with its attribute “.name” set for in-memory uploads or
            pass an HTTP URL as a string for Telegram to get a photo from the Internet.

            .. note::

                The photo must be at most 10 MB in size.
                The photo's width and height must not exceed 10000 in total.
                The photo's width and height ratio must be at most 20.

        caption (``str``, *optional*):
            Caption of the photo to be sent, 0-1024 characters.
            If not specified, the original caption is kept. Pass "" (empty string) to remove the caption.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        show_caption_above_media (``bool``, *optional*):
            Pass True, if the caption must be shown above the message media.

        has_spoiler (``bool``, *optional*):
            Pass True if the photo needs to be covered with a spoiler animation.
        
        is_high_quality (``bool``, *optional*):
            Pass ``True`` to locally compress the photo to High Definition quality (up to 2560x2560 resolution). 
            Pass ``False`` to locally compress the photo to Standard Definition quality (up to 1280x1280 resolution).
            Pass ``None`` to bypass local compression entirely and upload the original file unaltered.

            .. note::

                This local compression feature requires the ``Pillow`` library to be installed and 
                only applies when uploading local file paths or in-memory objects.

    """

    def __init__(
        self,
        media: Union[str, "io.BytesIO"],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: list["types.MessageEntity"] = None,
        show_caption_above_media: bool = None,
        has_spoiler: bool = None,
        is_high_quality: bool = None,
    ):
        super().__init__(media, caption, parse_mode, caption_entities)

        self.show_caption_above_media = show_caption_above_media
        self.has_spoiler = has_spoiler
        self.is_high_quality = is_high_quality

    async def write(
        self,
        client: "pyrogram.Client",
        chat_id: Optional[Union[int, str]] = None,
        business_connection_id: Optional[str] = None,
        progress: Optional[Callable] = None,
        progress_args: tuple = (),
    ) -> tuple[
        Union[
            "InputMediaPhoto",
            "InputMediaPhotoExternal",
        ],
        bool
    ]:
        is_bytes_io = isinstance(self.media, io.BytesIO)
        is_uploaded_file = is_bytes_io or os.path.isfile(self.media)
        is_external_url = not is_uploaded_file and re.match("^https?://", self.media)

        if is_bytes_io and not hasattr(self.media, "name"):
            self.media.name = "media"

        if is_uploaded_file:
            # Attempt to process the image locally
            optimized_stream = self.scale_tandroid_photo()
            if optimized_stream:
                self.media = optimized_stream
            uploaded_media = await client.invoke(
                raw.functions.messages.UploadMedia(
                    business_connection_id=None,  # TODO
                    peer=await client.resolve_peer(chat_id or "me"),
                    media=raw.types.InputMediaUploadedPhoto(
                        file=await client.save_file(self.media),
                        spoiler=self.has_spoiler
                    )
                )
            )
            media = raw.types.InputMediaPhoto(
                id=raw.types.InputPhoto(
                    id=uploaded_media.photo.id,
                    access_hash=uploaded_media.photo.access_hash,
                    file_reference=uploaded_media.photo.file_reference
                ),
                spoiler=self.has_spoiler
            )
        elif is_external_url:
            media = raw.types.InputMediaPhotoExternal(
                url=self.media,
                spoiler=self.has_spoiler
            )
        else:
            media = utils.get_input_media_from_file_id(
                self.media,
                FileType.PHOTO,
                has_spoiler=self.has_spoiler
            )
        return media, self.show_caption_above_media

    def scale_tandroid_photo(self) -> Optional["io.BytesIO"]:
        """
        Scales and compresses an image matching Telegram Android's internal logic,
        returning an in-memory BytesIO stream ready for Pyrogram.
        Returns None if Pillow is not installed or if processing fails.
        """
        if self.is_high_quality is None:
            return None
        if not HAS_PILLOW:
            log.warning(
                "Pillow is not installed. High Quality photo scaling will be skipped. "
                "Run 'pip install Pillow' for faster, optimized uploads."
            )
            return None

        max_size = 2560.0 if self.is_high_quality else 1280.0
        quality = 99 if self.is_high_quality else 87
        min_width = 101
        min_height = 101

        # Image.open accepts both file paths and BytesIO streams
        with Image.open(self.media) as img:
            # Ensure image is in RGB mode for JPEG saving (handles PNG transparency)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
                
            photo_w, photo_h = float(img.width), float(img.height)

            if photo_w == 0 or photo_h == 0:
                return None

            scale_anyway = False
            
            # Calculate initial scale factor to fit within max_size
            scale_factor = max(photo_w / max_size, photo_h / max_size)

            # Handle minimum dimension constraints
            if min_width != 0 and min_height != 0 and (photo_w < min_width or photo_h < min_height):
                if photo_w < min_width and photo_h > min_height:
                    scale_factor = photo_w / min_width
                elif photo_w > min_width and photo_h < min_height:
                    scale_factor = photo_h / min_height
                else:
                    scale_factor = max(photo_w / min_width, photo_h / min_height)
                scale_anyway = True

            # Calculate final dimensions
            w = int(photo_w / scale_factor)
            h = int(photo_h / scale_factor)

            if w == 0 or h == 0:
                return None

            # Resize the image if it exceeds max size OR if it's smaller than min size
            if scale_factor > 1.0 or scale_anyway:
                img = img.resize((w, h), Image.Resampling.LANCZOS)

            # Create the in-memory byte buffer
            photo_stream = io.BytesIO()
            
            # Pyrogram requires a name to guess the mime-type
            photo_stream.name = "photo.jpg"
            
            # Save the image data into the buffer using Telegram's compression rules
            img.save(photo_stream, format="JPEG", quality=quality, optimize=True)

            photo_stream.seek(0)            
            return photo_stream
        return None
