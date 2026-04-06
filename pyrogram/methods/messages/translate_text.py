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

from typing import Optional, Union

import pyrogram
from pyrogram import enums, raw, types, utils


class TranslateText:
    async def translate_message_text(
        self: "pyrogram.Client",
        to_language_code: str,
        chat_id: Union[int, str],
        message_ids: Union[int, list[int]],
        tone: str = "",
    ) -> Union["types.FormattedText", list["types.FormattedText"]]:
        """Extracts text or caption of the given message and translates it to the given language. If the current user is a Telegram Premium user, then text formatting is preserved.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            to_language_code (``str``):
                Language code of the language to which the message is translated.
                Must be one of "af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "zh-CN", "zh", "zh-Hans", "zh-TW", "zh-Hant", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "he", "iw", "hi", "hmn", "hu", "is", "ig", "id", "in", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "ko", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ny", "or", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tl", "tg", "ta", "tt", "te", "th", "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy", "xh", "yi", "ji", "yo", "zu".

            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_ids (``int`` | List of ``int``):
                Identifier or list of message identifiers of the target message.

            tone (``str``, *optional*):
                Tone of the translation.

        Returns:
            :obj:`~pyrogram.types.FormattedText` | List of :obj:`~pyrogram.types.FormattedText`: In case *message_ids* was not
            a list, a single result is returned, otherwise a list of results is returned.

        Example:
            .. code-block:: python

                await app.translate_message_text("en", chat_id, message_id)
        """
        ids = [message_ids] if not isinstance(message_ids, list) else message_ids

        r = await self.invoke(
            raw.functions.messages.TranslateText(
                to_lang=to_language_code,
                peer=await self.resolve_peer(chat_id),
                id=ids,
                tone=tone,
            )
        )

        return (
            types.FormattedText._parse(self, r.result[0])
            if len(r.result) == 1
            else [
                types.FormattedText._parse(self, i)
                for i in r.result
            ]
        )


    async def translate_text(
        self: "pyrogram.Client",
        to_language_code: str,
        text: "types.FormattedText",
        tone: str = "",
    ) -> Union["types.FormattedText", list["types.FormattedText"]]:
        """Translates a text to the given language. If the current user is a Telegram Premium user, then text formatting is preserved.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            to_language_code (``str``):
                Language code of the language to which the message is translated.
                Must be one of "af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "zh-CN", "zh", "zh-Hans", "zh-TW", "zh-Hant", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "he", "iw", "hi", "hmn", "hu", "is", "ig", "id", "in", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "ko", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ny", "or", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tl", "tg", "ta", "tt", "te", "th", "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy", "xh", "yi", "ji", "yo", "zu".

            text (:obj:`~pyrogram.types.FormattedText`):
                Text to translate.

            tone (``str``, *optional*):
                Tone of the translation.

        Returns:
            :obj:`~pyrogram.types.FormattedText` | List of :obj:`~pyrogram.types.FormattedText`: In case *message_ids* was not
            a list, a single result is returned, otherwise a list of results is returned.

        Example:
            .. code-block:: python

                await app.translate_text("fa", "Pyrogram")
        """
        if isinstance(text, str):
            text = types.FormattedText(text=text)
        r = await self.invoke(
            raw.functions.messages.TranslateText(
                to_lang=to_language_code,
                text=[await text.write(self)],
                tone=tone,
            )
        )

        return (
            types.FormattedText._parse(self, r.result[0])
            if len(r.result) == 1
            else [
                types.FormattedText._parse(self, i)
                for i in r.result
            ]
        )
