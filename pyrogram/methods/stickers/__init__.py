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

from .delete_sticker_from_set import DeleteStickerFromSet
from .delete_sticker_set import DeleteStickerSet
from .get_custom_emoji_stickers import GetCustomEmojiStickers
from .get_message_effects import GetMessageEffects
from .get_stickers import GetStickers
from .get_suggested_sticker_set_name import GetSuggestedStickerSetName
from .set_sticker_position_in_set import SetStickerPositionInSet
from .set_sticker_set_title import SetStickerSetTitle
from .upload_sticker_file import UploadStickerFile


class Stickers(
    DeleteStickerFromSet,
    DeleteStickerSet,
    GetCustomEmojiStickers,
    GetMessageEffects,
    GetStickers,
    GetSuggestedStickerSetName,
    SetStickerPositionInSet,
    SetStickerSetTitle,
    UploadStickerFile,
):
    pass
