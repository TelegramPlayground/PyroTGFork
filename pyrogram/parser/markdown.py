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

import html
import re
from typing import Optional, Union

import pyrogram
from pyrogram.enums import MessageEntityType

from . import utils
from .html import HTML

BOLD_DELIM = "**"
ITALIC_DELIM = "__"
UNDERLINE_DELIM = "--"
STRIKE_DELIM = "~~"
SPOILER_DELIM = "||"
CODE_DELIM = "`"
PRE_DELIM = "```"
BLOCKQUOTE_DELIM = ">"
BLOCKQUOTE_ESCAPE_DELIM = "|>"
BLOCKQUOTE_EXPANDABLE_DELIM = "**>"
BLOCKQUOTE_EXPANDABLE_END_DELIM = "<**"


MARKDOWN_RE = re.compile(
    r"({d})|(!?)\[(.+?)\]\((.+?)\)".format(
        d="|".join(
            [
                "".join(i)
                for i in [
                    [rf"\{j}" for j in i]
                    for i in [
                        PRE_DELIM,
                        CODE_DELIM,
                        STRIKE_DELIM,
                        UNDERLINE_DELIM,
                        ITALIC_DELIM,
                        BOLD_DELIM,
                        SPOILER_DELIM,
                    ]
                ]
            ]
        )
    )
)

OPENING_TAG = "<{}>"
CLOSING_TAG = "</{}>"
URL_MARKUP = '<a href="{}">{}</a>'
EMOJI_MARKUP = "<emoji id={}>{}</emoji>"
FIXED_WIDTH_DELIMS = [CODE_DELIM, PRE_DELIM]
CODE_TAG_RE = re.compile(r"<code>.*?</code>")
URL_RE = re.compile(r"(!?)\[(.+?)\]\((.+?)\)")


class Markdown:
    def __init__(self, client: Optional["pyrogram.Client"]):
        self.html = HTML(client)

    @staticmethod
    def escape_and_create_quotes(text: str, strict: bool):
        text_lines: list[Union[str, None]] = text.splitlines()

        # Indexes of Already escaped lines
        html_escaped_list: list[int] = []

        # Temporary Queue to hold lines to be quoted
        to_quote_list: list[tuple[int, str]] = []

        def create_blockquote(quote_type: str = "") -> None:
            """
            Merges all lines in quote_queue into first line of queue
            Encloses that line in html quote
            Replaces rest of the lines with None placeholders to preserve indexes
            """
            if len(to_quote_list) == 0:
                return

            joined_lines = "\n".join([i[1] for i in to_quote_list])

            first_line_index, _ = to_quote_list[0]
            text_lines[first_line_index] = (
                f"<blockquote{quote_type}>{joined_lines}</blockquote>"
            )

            for line_to_remove in to_quote_list[1:]:
                text_lines[line_to_remove[0]] = None

            to_quote_list.clear()

        # Handle Expandable Quote
        inside_blockquote = False
        for index, line in enumerate(text_lines):
            if line.startswith(BLOCKQUOTE_EXPANDABLE_DELIM) and not inside_blockquote:
                delim_stripped_line = line[3:]
                parsed_line = (
                    html.escape(delim_stripped_line) if strict else delim_stripped_line
                )

                to_quote_list.append((index, parsed_line))
                html_escaped_list.append(index)

                inside_blockquote = True
                continue

            elif line.endswith(BLOCKQUOTE_EXPANDABLE_END_DELIM) and inside_blockquote:
                delim_stripped_line = line[:-3]
                parsed_line = (
                    html.escape(delim_stripped_line) if strict else delim_stripped_line
                )

                to_quote_list.append((index, parsed_line))
                html_escaped_list.append(index)

                inside_blockquote = False

                create_blockquote(quote_type=" expandable")

            if inside_blockquote:
                parsed_line = html.escape(line) if strict else line
                to_quote_list.append((index, parsed_line))
                html_escaped_list.append(index)

        # Handle Single line/Continued Quote
        for index, line in enumerate(text_lines):
            if line is None:
                continue 

            if line.startswith(BLOCKQUOTE_ESCAPE_DELIM):
                text_lines[index] = line[1:]
                create_blockquote()
                continue

            if line.startswith(BLOCKQUOTE_DELIM):
                delim_stripped_line = line[1:]
                parsed_line = (
                    html.escape(delim_stripped_line) if strict else delim_stripped_line
                )

                to_quote_list.append((index, parsed_line))
                html_escaped_list.append(index)

            elif len(to_quote_list) > 0:
                create_blockquote()
        else:
            create_blockquote()

        if strict:
            for idx, line in enumerate(text_lines):
                if idx not in html_escaped_list:
                    text_lines[idx] = html.escape(line)

        return "\n".join(
            [valid_line for valid_line in text_lines if valid_line is not None]
        )

    async def parse(self, text: str, strict: bool = False):
        text = self.escape_and_create_quotes(text, strict=strict)
        delims = set()
        is_fixed_width = False

        for i, match in enumerate(re.finditer(MARKDOWN_RE, text)):
            start, _ = match.span()
            delim, is_emoji, text_url, url = match.groups()
            full = match.group(0)

            if delim in FIXED_WIDTH_DELIMS:
                is_fixed_width = not is_fixed_width

            if is_fixed_width and delim not in FIXED_WIDTH_DELIMS:
                continue

            if not is_emoji and text_url:
                text = utils.replace_once(
                    text, full, URL_MARKUP.format(url, text_url), start
                )
                continue

            if is_emoji:
                emoji = text_url
                emoji_id = url.lstrip("tg://emoji?id=")
                text = utils.replace_once(
                    text, full, EMOJI_MARKUP.format(emoji_id, emoji), start
                )
                continue

            if delim == BOLD_DELIM:
                tag = "b"
            elif delim == ITALIC_DELIM:
                tag = "i"
            elif delim == UNDERLINE_DELIM:
                tag = "u"
            elif delim == STRIKE_DELIM:
                tag = "s"
            elif delim == CODE_DELIM:
                tag = "code"
            elif delim == PRE_DELIM:
                tag = "pre"
            elif delim == SPOILER_DELIM:
                tag = "spoiler"
            else:
                continue

            if delim not in delims:
                delims.add(delim)
                tag = OPENING_TAG.format(tag)
            else:
                delims.remove(delim)
                tag = CLOSING_TAG.format(tag)

            if delim == PRE_DELIM and delim in delims:
                delim_and_language = text[text.find(PRE_DELIM) :].split("\n")[0]
                language = delim_and_language[len(PRE_DELIM) :]
                text = utils.replace_once(
                    text, delim_and_language, f'<pre language="{language}">', start
                )
                continue

            text = utils.replace_once(text, delim, tag, start)

        return await self.html.parse(text)

    @staticmethod
    def unparse(text: str, entities: list):
        """
        https://github.com/LonamiWebs/Telethon/blob/141b620/telethon/extensions/markdown.py#L137-L193

        Performs the reverse operation to .parse(), effectively returning
        markdown-like syntax given a normal text and its MessageEntity's.

        :param text: the text to be reconverted into markdown.
        :param entities: list of MessageEntity's applied to the text.
        :return: a markdown-like text representing the combination of both inputs.
        """
        delimiters = {
            MessageEntityType.BOLD: BOLD_DELIM,
            MessageEntityType.ITALIC: ITALIC_DELIM,
            MessageEntityType.UNDERLINE: UNDERLINE_DELIM,
            MessageEntityType.STRIKETHROUGH: STRIKE_DELIM,
            MessageEntityType.CODE: CODE_DELIM,
            MessageEntityType.PRE: PRE_DELIM,
            MessageEntityType.BLOCKQUOTE: BLOCKQUOTE_DELIM,
            MessageEntityType.EXPANDABLE_BLOCKQUOTE: BLOCKQUOTE_EXPANDABLE_DELIM,
            MessageEntityType.SPOILER: SPOILER_DELIM
        }

        text = utils.add_surrogates(text)

        insert_at = []
        for i, entity in enumerate(entities):
            s = entity.offset
            e = entity.offset + entity.length
            delimiter = delimiters.get(entity.type, None)
            if delimiter:
                if entity.type == MessageEntityType.PRE:
                    inside_blockquote = any(
                        blk_entity.offset <= s < blk_entity.offset + blk_entity.length and
                        blk_entity.offset < e <= blk_entity.offset + blk_entity.length
                        for blk_entity in entities
                        if blk_entity.type == MessageEntityType.BLOCKQUOTE
                    )
                    is_expandable = any(
                        blk_entity.offset <= s < blk_entity.offset + blk_entity.length and
                        blk_entity.offset < e <= blk_entity.offset + blk_entity.length and
                        blk_entity.collapsed
                        for blk_entity in entities
                        if blk_entity.type == MessageEntityType.EXPANDABLE_BLOCKQUOTE
                    )
                    if inside_blockquote:
                        if is_expandable:
                            if entity.language:
                                open_delimiter = f"{delimiter}{entity.language}\n**>"
                            else:
                                open_delimiter = f"{delimiter}\n**>"
                            close_delimiter = f"\n**>{delimiter}"
                        else:
                            if entity.language:
                                open_delimiter = f"{delimiter}{entity.language}\n>"
                            else:
                                open_delimiter = f"{delimiter}\n>"
                            close_delimiter = f"\n>{delimiter}"
                    else:
                        if entity.language:
                            open_delimiter = f"{delimiter}{entity.language}"
                        else:
                            open_delimiter = delimiter
                        close_delimiter = delimiter
                    insert_at.append((s, i, open_delimiter))
                    insert_at.append((e, -i, close_delimiter))
                elif entity.type != MessageEntityType.BLOCKQUOTE and entity.type != MessageEntityType.EXPANDABLE_BLOCKQUOTE:
                    open_delimiter = delimiter
                    close_delimiter = delimiter
                    insert_at.append((s, i, open_delimiter))
                    insert_at.append((e, -i, close_delimiter))
                else:
                    # Handle multiline blockquotes
                    text_subset = text[s:e]
                    lines = text_subset.splitlines()
                    for line_num, line in enumerate(lines):
                        line_start = s + sum(len(l) + 1 for l in lines[:line_num])
                        if entity.type == MessageEntityType.EXPANDABLE_BLOCKQUOTE:
                            insert_at.append((line_start, i, BLOCKQUOTE_EXPANDABLE_DELIM))
                        else:
                            insert_at.append((line_start, i, BLOCKQUOTE_DELIM))
            # No closing delimiter for blockquotes
            else:
                url = None
                is_emoji = False
                if entity.type == MessageEntityType.TEXT_LINK:
                    url = entity.url
                elif entity.type == MessageEntityType.TEXT_MENTION:
                    url = f'tg://user?id={entity.user.id}'
                elif entity.type == MessageEntityType.CUSTOM_EMOJI:
                    url = f"tg://emoji?id={entity.custom_emoji_id}"
                    is_emoji = True
                if url:
                    if is_emoji:
                        insert_at.append((s, i, '!'))
                    else:
                        insert_at.append((s, i, '['))
                    insert_at.append((e, -i, f''))

        insert_at.sort(key=lambda t: (t[0], t[1]))
        while insert_at:
            at, _, what = insert_at.pop()

            # If we are in the middle of a surrogate nudge the position by -1.
            # Otherwise we would end up with malformed text and fail to encode.
            # For example of bad input: "Hi \ud83d\ude1c"
            # https://en.wikipedia.org/wiki/UTF-16#U+010000_to_U+10FFFF
            while utils.within_surrogate(text, at):
                at += 1

            text = text[:at] + what + text[at:]

        return utils.remove_surrogates(text)
