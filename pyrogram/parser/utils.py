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

import re
from struct import unpack

# SMP = Supplementary Multilingual Plane: https://en.wikipedia.org/wiki/Plane_(Unicode)#Overview
SMP_RE = re.compile(r"[\U00010000-\U0010FFFF]")


def add_surrogates(text):
    # Replace each SMP code point with a surrogate pair
    return SMP_RE.sub(
        lambda match:  # Split SMP in two surrogates
        "".join(chr(i) for i in unpack("<HH", match.group().encode("utf-16le"))),
        text
    )


def remove_surrogates(text):
    # Replace each surrogate pair with a SMP code point
    return text.encode("utf-16", "surrogatepass").decode("utf-16", "ignore")


def replace_once(source: str, old: str, new: str, start: int):
    return source[:start] + source[start:].replace(old, new, 1)


def within_surrogate(text, index, *, length=None):
    """
    https://github.com/LonamiWebs/Telethon/blob/63d9b26/telethon/helpers.py#L52-L63

    `True` if ``index`` is within a surrogate (before and after it, not at!).
    """
    if length is None:
        length = len(text)

    return (
            1 < index < len(text) and  # in bounds
            '\ud800' <= text[index - 1] <= '\udbff' and  # previous is
            '\ud800' <= text[index] <= '\udfff'  # current is
    )


dtf_reegex = r"r|w?[dD]?[tT]?"


def parse_date_time_format_tl(args, date_time_format: str):
    # Initialize all flags to False (matches the empty string behavior)
    args["relative"] = False
    args["short_time"] = False
    args["long_time"] = False
    args["short_date"] = False
    args["long_date"] = False
    args["day_of_week"] = False

    if date_time_format:
        # Strictly validate against TDLib's required regex
        if not re.fullmatch(dtf_reegex, date_time_format):
            raise ValueError(f"Invalid date-time format string: '{date_time_format}'")
        
        # Handle the mutually exclusive relative flag
        if date_time_format == "r":
            args["relative"] = True
        else:
            # Map the remaining control characters
            if "w" in date_time_format:
                args["day_of_week"] = True
                
            if "d" in date_time_format:
                args["short_date"] = True
            elif "D" in date_time_format:
                args["long_date"] = True
                
            if "t" in date_time_format:
                args["short_time"] = True
            elif "T" in date_time_format:
                args["long_time"] = True
    
    return args
