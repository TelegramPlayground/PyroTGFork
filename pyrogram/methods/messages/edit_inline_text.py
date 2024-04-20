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
from typing import Optional, List

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from pyrogram import utils
from .inline_session import get_session

log = logging.getLogger(__name__)


class EditInlineText:
    async def edit_inline_text(
        self: "pyrogram.Client",
        inline_message_id: str,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        link_preview_options: "types.LinkPreviewOptions" = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        disable_web_page_preview: bool = None
    ) -> bool:
        """Edit the text of inline messages.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            inline_message_id (``str``):
                Identifier of the inline message.

            text (``str``):
                New text of the message.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            link_preview_options (:obj:`~pyrogram.types.LinkPreviewOptions`, *optional*):
                Link preview generation options for the message

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Bots only

                # Simple edit text
                await app.edit_inline_text(inline_message_id, "new text")

                # Take the same text message, remove the web page preview only
                await app.edit_inline_text(
                    inline_message_id, message.text,
                    link_preview_options=types.LinkPreviewOptions(
                        is_disabled=True
                    )
                )
        """
        if disable_web_page_preview and link_preview_options:
            raise ValueError(
                "Parameters `disable_web_page_preview` and `link_preview_options` are mutually "
                "exclusive."
            )

        if disable_web_page_preview is not None:
            log.warning(
                "This property is deprecated. "
                "Please use link_preview_options instead"
            )
            link_preview_options = types.LinkPreviewOptions(is_disabled=disable_web_page_preview)

        unpacked = utils.unpack_inline_message_id(inline_message_id)
        dc_id = unpacked.dc_id

        session = await get_session(self, dc_id)

        return await session.invoke(
            raw.functions.messages.EditInlineBotMessage(
                id=unpacked,
                no_webpage=link_preview_options.is_disabled if link_preview_options else None,
                invert_media=link_preview_options.show_above_text if link_preview_options else None,
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                **await utils.parse_text_entities(self, text, parse_mode, entities)
            ),
            sleep_threshold=self.sleep_threshold
        )
