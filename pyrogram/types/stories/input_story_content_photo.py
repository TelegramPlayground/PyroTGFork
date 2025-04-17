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

import io
from typing import Union

from .input_story_content import InputStoryContent


class InputStoryContentPhoto(InputStoryContent):
    """Describes a photo to post as a story.

    It is intended to be used with :obj:`~pyrogram.Client.send_story` or :obj:`~pyrogram.Client.post_story`.

    Parameters:
        photo (``str`` | :obj:`io.BytesIO`):
            File to send.
            Pass a file_id as string to send a video that exists on the Telegram servers or
            pass a file path as string to upload a new video that exists on your local machine or
            pass a binary file-like object with its attribute “.name” set for in-memory uploads or
            pass an HTTP URL as a string for Telegram to get a video from the Internet.

        thumbnail (``str`` | :obj:`io.BytesIO`):
            Thumbnail of the photo sent.
            The thumbnail should be in JPEG format and less than 200 KB in size.
            A thumbnail's width and height should not exceed 320 pixels.
            Thumbnails can't be reused and can be only uploaded as a new file.

    """

    def __init__(
        self,
        photo: Union[str, "io.BytesIO"],
        thumbnail: Union[str, "io.BytesIO"] = None,
    ):
        super().__init__()

        self.photo = photo
        self.thumbnail = thumbnail
