#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2024 Dan <https://github.com/delivrance>
#  Copyright (C) 2026-present <https://github.com/TelegramPlayGround>
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
import urllib.parse

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
BLOCKQUOTE_EXPANDABLE_OPTIONAL_END_DELIM = "<**"  # Kept for backwards compatibility if imported elsewhere

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
EMOJI_MARKUP = "<tg-emoji emoji-id={}>{}</tg-emoji>"
DATE_TIME_MARKUP = "<tg-time unix={}>{}</tg-time>"
DATE_TIME_FORMAT_MARKUP = "<tg-time unix={} format={}>{}</tg-time>"
FIXED_WIDTH_DELIMS = [CODE_DELIM, PRE_DELIM]
CODE_TAG_RE = re.compile(r"<code>.*?</code>")
URL_RE = re.compile(r"(!?)\[(.+?)\]\((.+?)\)")


class Markdown:
    def __init__(self, client: Optional["pyrogram.Client"]):
        self.html = HTML(client)

    @staticmethod
    def escape_and_create_quotes(text: str, strict: bool):
        text_lines: list[Union[str, None]] = text.splitlines()
        html_escaped_list: list[int] = []

        i = 0
        while i < len(text_lines):
            line = text_lines[i]

            if line is None:
                i += 1
                continue

            # Ignore Escaped >
            if line.startswith(BLOCKQUOTE_ESCAPE_DELIM):
                text_lines[i] = html.escape(line[1:]) if strict else line[1:]
                html_escaped_list.append(i)
                i += 1
                continue

            # Check if line starts a blockquote
            is_bq = False
            started_as_expandable = False

            if line.startswith(BLOCKQUOTE_EXPANDABLE_DELIM):
                is_bq = True
                started_as_expandable = True
            elif line.startswith(BLOCKQUOTE_DELIM):
                is_bq = True

            if is_bq:
                start_index = i
                bq_lines = []

                # Collect all consecutive blockquote lines
                while i < len(text_lines):
                    curr_line = text_lines[i]

                    # Detect boundaries between consecutive blockquotes
                    if i > start_index:
                        # Boundary 1: `**>` explicitly starts a NEW expandable blockquote
                        if curr_line.startswith(BLOCKQUOTE_EXPANDABLE_DELIM):
                            break

                    curr_prefix_len = 0
                    if curr_line.startswith(BLOCKQUOTE_EXPANDABLE_DELIM):
                        curr_prefix_len = len(BLOCKQUOTE_EXPANDABLE_DELIM)
                    elif curr_line.startswith(BLOCKQUOTE_DELIM):
                        curr_prefix_len = len(BLOCKQUOTE_DELIM)
                    else:
                        break  # No longer in a blockquote

                    # Strip the delimiter
                    bq_lines.append(curr_line[curr_prefix_len:])
                    i += 1

                # Check if it properly closes as an expandable blockquote
                is_expandable = False
                # Strict Bot API requirement: Must have started with **> AND end with ||
                if started_as_expandable and bq_lines and bq_lines[-1].endswith(SPOILER_DELIM):
                    is_expandable = True
                    # Strip the || from the final line
                    bq_lines[-1] = bq_lines[-1][:-len(SPOILER_DELIM)]

                # Escape if strict
                if strict:
                    bq_lines = [html.escape(l) for l in bq_lines]

                # Create the merged blockquote entity
                joined_lines = "\n".join(bq_lines)
                quote_type = " expandable" if is_expandable else ""

                text_lines[start_index] = f"<blockquote{quote_type}>{joined_lines}</blockquote>"
                html_escaped_list.append(start_index)

                # Clear out the consumed lines
                for j in range(start_index + 1, i):
                    text_lines[j] = None
            else:
                i += 1

        # Escape remaining text lines if strict
        if strict:
            for idx, line in enumerate(text_lines):
                if line is not None and idx not in html_escaped_list:
                    text_lines[idx] = html.escape(line)

        return "\n".join(filter(lambda x: x is not None, text_lines))

    async def parse(self, text: str, strict: bool = False):
        text = self.escape_and_create_quotes(text, strict=strict)
        
        matches = list(re.finditer(MARKDOWN_RE, text))
        valid_delims = set()
        opened = {}
        active_fixed_width = None
        
        # --- Pass 1: Identify paired delimiters ---
        for i, match in enumerate(matches):
            delim, is_emoji_or_date, text_url, url = match.groups()
            
            if not delim:
                continue
                
            # If we are inside a code block, ignore all other formatting
            if active_fixed_width:
                if delim == active_fixed_width:
                    # Closing the code block
                    valid_delims.add(opened[delim])
                    valid_delims.add(i)
                    del opened[delim]
                    active_fixed_width = None
                continue
                
            # Opening a new code block
            if delim in FIXED_WIDTH_DELIMS:
                active_fixed_width = delim
                opened[delim] = i
                continue
                
            # Standard formatting delimiters
            if delim in [BOLD_DELIM, ITALIC_DELIM, UNDERLINE_DELIM, STRIKE_DELIM, SPOILER_DELIM]:
                if delim not in opened:
                    opened[delim] = i
                else:
                    # Valid pair found!
                    valid_delims.add(opened[delim])
                    valid_delims.add(i)
                    del opened[delim]
                    
        # --- Pass 2: Apply replacements ---
        delims = set()
        
        for i, match in enumerate(matches):
            start, _ = match.span()
            delim, is_emoji_or_date, text_url, url = match.groups()
            full = match.group(0)

            # 1. Handle Links
            if not is_emoji_or_date and text_url:
                text = utils.replace_once(text, full, URL_MARKUP.format(url, text_url), start)
                continue

            # 2. Handle Emojis and Dates
            if is_emoji_or_date:
                emoji = text_url
                parsed_url = urllib.parse.urlparse(url)
                # Parse the query parameters into a dictionary-like object
                query_params = urllib.parse.parse_qs(parsed_url.query)
                # Branch 1: Custom Emoji
                if parsed_url.netloc == "emoji":
                    emoji_id = query_params.get("id", ["0"])[0]
                    text = utils.replace_once(text, full, EMOJI_MARKUP.format(emoji_id, emoji), start)
                # Branch 2: Custom Time
                elif parsed_url.netloc == "time":
                    unix_time = query_params.get("unix", ["0"])[0]
                    fmt_string = query_params.get("format", [""])[0]
                    if fmt_string:
                        text = utils.replace_once(text, full, DATE_TIME_FORMAT_MARKUP.format(unix_time, fmt_string, emoji), start)
                    else:
                        text = utils.replace_once(text, full, DATE_TIME_MARKUP.format(unix_time, emoji), start)
                continue

            # 3. Handle Formatting Delimiters
            if delim:
                # If this delimiter is unclosed (or suppressed by a code block), leave it as literal text!
                if i not in valid_delims:
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

                # Special handling for PRE language definition
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
            MessageEntityType.SPOILER: SPOILER_DELIM,
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
                        blk_entity.offset <= s < blk_entity.offset + blk_entity.length
                        and blk_entity.offset < e <= blk_entity.offset + blk_entity.length
                        for blk_entity in entities
                        if blk_entity.type == MessageEntityType.BLOCKQUOTE
                        or blk_entity.type == MessageEntityType.EXPANDABLE_BLOCKQUOTE
                    )
                    
                    if inside_blockquote:
                        # Inside any blockquote, inner lines use ">"
                        if entity.language:
                            open_delimiter = f"{delimiter}{entity.language}\n>"
                        else:
                            open_delimiter = f"{delimiter}\n>"
                        close_delimiter = f"\n>{delimiter}"
                    else:
                        if entity.language:
                            open_delimiter = f"{delimiter}{entity.language}\n"
                        else:
                            open_delimiter = f"{delimiter}\n"
                        close_delimiter = delimiter
                    insert_at.append((s, i, open_delimiter))
                    insert_at.append((e, -i, close_delimiter))
                elif (
                    entity.type != MessageEntityType.BLOCKQUOTE
                    and entity.type != MessageEntityType.EXPANDABLE_BLOCKQUOTE
                ):
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
                        
                        # Blockquote prefixes MUST be placed at the absolute start of the line.
                        # We use `-10000 + i` to ensure they are popped last and end up on the far left,
                        # wrapping perfectly around any inline entities sharing the same offset.
                        prefix_priority = -10000 + i
                        
                        if entity.type == MessageEntityType.EXPANDABLE_BLOCKQUOTE:
                            if line_num == 0:
                                insert_at.append((line_start, prefix_priority, BLOCKQUOTE_EXPANDABLE_DELIM))
                            else:
                                insert_at.append((line_start, prefix_priority, BLOCKQUOTE_DELIM))
                        else:
                            insert_at.append((line_start, prefix_priority, BLOCKQUOTE_DELIM))

                    # Append expandability mark for expandable blockquotes
                    if entity.type == MessageEntityType.EXPANDABLE_BLOCKQUOTE:
                        # Expandability marks MUST be at the absolute end of the blockquote.
                        # We use `10000 - i` to ensure it is popped first and ends up on the far right.
                        insert_at.append((e, 10000 - i, SPOILER_DELIM))

            # No closing delimiter for blockquotes (handled by lines above)
            else:
                url = None
                is_emoji_or_date = False
                if entity.type == MessageEntityType.TEXT_LINK:
                    url = entity.url
                elif entity.type == MessageEntityType.TEXT_MENTION:
                    url = f"tg://user?id={entity.user.id}"
                elif entity.type == MessageEntityType.CUSTOM_EMOJI:
                    url = f"tg://emoji?id={entity.custom_emoji_id}"
                    is_emoji_or_date = True
                elif entity.type == MessageEntityType.DATE_TIME:
                    if entity.date_time_format:
                        url = f"tg://time?unix={entity.unix_time}&format={entity.date_time_format}"
                    else:
                        url = f"tg://time?unix={entity.unix_time}"
                    is_emoji_or_date = True
                if url:
                    if is_emoji_or_date:
                        insert_at.append((s, i, "!["))
                    else:
                        insert_at.append((s, i, "["))
                    insert_at.append((e, -i, f"]({url})"))

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
