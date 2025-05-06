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

from typing import Union

import pyrogram
from pyrogram import raw, types

from ..object import Object


class PaidMedia(Object):
    """This object describes paid media.

    Currently, it can be one of:

    - :obj:`~pyrogram.types.PaidMediaPreview`
    - :obj:`~pyrogram.types.PaidMediaPhoto`
    - :obj:`~pyrogram.types.PaidMediaVideo`
    """

    def __init__(
        self
    ):
        super().__init__()


    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        extended_media: Union[
            "raw.types.MessageExtendedMediaPreview",
            "raw.types.MessageExtendedMedia"
        ]
    ) -> "PaidMedia":
        if isinstance(extended_media, raw.types.MessageExtendedMediaPreview):
            return types.PaidMediaPreview(
                width=getattr(extended_media, "w", None),
                height=getattr(extended_media, "h", None),
                duration=getattr(extended_media, "video_duration", None),
                minithumbnail=types.StrippedThumbnail(
                    client=client,
                    # TODO
                    data=getattr(getattr(extended_media, "thumb"), "bytes", None)
                ) if getattr(extended_media, "thumb", None) else None
            )
        if isinstance(extended_media, raw.types.MessageExtendedMedia):
            media = extended_media.media

            has_media_spoiler = getattr(media, "spoiler", None)
            ttl_seconds = getattr(media, "ttl_seconds", None)

            if isinstance(media, raw.types.MessageMediaPhoto):
                photo = types.Photo._parse(client, media.photo, ttl_seconds, has_media_spoiler)
                
                return types.PaidMediaPhoto(
                    photo=photo
                )
            
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

                        if not video_attributes.round_message:
                            video = types.Video._parse(client, media, video_attributes, file_name, ttl_seconds)

                            return types.PaidMediaVideo(
                                video=video
                            )
