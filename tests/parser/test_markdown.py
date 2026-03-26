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

import pyrogram
from pyrogram.parser.markdown import Markdown


# expected: the expected unparsed Markdown
# text: original text without entities
# entities: message entities coming from the server

def test_markdown_unparse_bold():
    expected = "**bold**"
    text = "bold"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.BOLD, offset=0, length=4)])

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_italic():
    expected = "__italic__"
    text = "italic"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.ITALIC, offset=0, length=6)])

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_italic_html():
    expected = "__This works, it's ok__ <b>This shouldn't</b>"
    text = "This works, it's ok <b>This shouldn't</b>"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.ITALIC, offset=0, length=19)])

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_underline():
    expected = "--underline--"
    text = "underline"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.UNDERLINE, offset=0, length=9)])

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_strike():
    expected = "~~strike~~"
    text = "strike"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.STRIKETHROUGH, offset=0, length=6)])

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_spoiler():
    expected = "||spoiler||"
    text = "spoiler"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.SPOILER, offset=0, length=7)])

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_url():
    expected = '[URL](https://pyrogram.org/)'
    text = "URL"
    entities = pyrogram.types.List([pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.TEXT_LINK,
                                                                 offset=0, length=3, url='https://pyrogram.org/')])

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_emoji():
    expected = '![🥲](tg://emoji?id=5195264424893488796) im crying'
    text = "🥲 im crying"
    entities = pyrogram.types.List([
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.CUSTOM_EMOJI,
        offset=0, length=2,
        custom_emoji_id=5195264424893488796)
    ])

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_code():
    expected = '`code`'
    text = "code"
    entities = pyrogram.types.List(
        [pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.CODE, offset=0, length=4)])

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_pre():
    expected = """```python
for i in range(10):
    print(i)```"""

    text = """for i in range(10):
    print(i)"""
    entities = pyrogram.types.List([
        pyrogram.types.MessageEntity(
            type=pyrogram.enums.MessageEntityType.PRE,
            offset=0, length=32,
            language="python"
        )
    ])

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_pre_2():
    expected = """```...```"""

    text = """..."""
    entities = pyrogram.types.List([
        pyrogram.types.MessageEntity(
            type=pyrogram.enums.MessageEntityType.PRE,
            offset=0, length=3,
            language=""
        )
    ])

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_blockquote():
    expected = """>Block quotation started
>Block quotation continued
>The last line of the block quotation
**>Expandable block quotation started
>Expandable block quotation continued
>Expandable block quotation continued
>Hidden by default part of the block quotation started
>Expandable block quotation continued
>The last line of the block quotation||"""

    text = """Block quotation started\nBlock quotation continued\nThe last line of the block quotation\nExpandable block quotation started\nExpandable block quotation continued\nExpandable block quotation continued\nHidden by default part of the block quotation started\nExpandable block quotation continued\nThe last line of the block quotation"""

    entities = pyrogram.types.List([
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.BLOCKQUOTE, offset=0, length=86),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.EXPANDABLE_BLOCKQUOTE, offset=87, length=236)
    ])

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_mixed():
    expected = "**aaaaaaa__aaabbb__**~~dddddddd||ddeee||~~||eeeeeeefff||ffff`fffggggggg`ggghhhhhhhhhh"
    text = "aaaaaaaaaabbbddddddddddeeeeeeeeeeffffffffffgggggggggghhhhhhhhhh"
    entities = pyrogram.types.List([
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.BOLD, offset=0, length=13),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.ITALIC, offset=7, length=6),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.STRIKETHROUGH, offset=13, length=13),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.SPOILER, offset=21, length=5),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.SPOILER, offset=26, length=10),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.CODE, offset=40, length=10)
    ])

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_mixed_2():
    expected = """**bold**, **bold**
__italic__, __italic__
--underline--, --underline--
~~strikethrough~~, ~~strikethrough~~, ~~strikethrough~~
||spoiler||, ||spoiler||
**bold __italic bold ~~italic bold strikethrough ||italic bold strikethrough spoiler||~~ --underline italic bold--__ bold**
[inline URL](http://www.example.com/)
![👍](tg://emoji?id=5368324170671202286)
![22:45 tomorrow](tg://time?unix=1647531900&format=wDT)
![22:45 tomorrow](tg://time?unix=1647531900&format=t)
![22:45 tomorrow](tg://time?unix=1647531900&format=r)
![22:45 tomorrow](tg://time?unix=1647531900)
`inline fixed-width code`
```
pre-formatted fixed-width code block```
```python
pre-formatted fixed-width code block written in the Python programming language```
>Block quotation started
>Block quotation continued
>The last line of the block quotation
**>Expandable block quotation started
**>Expandable block quotation continued
**>Expandable block quotation continued
**>Hidden by default part of the block quotation started
**>Expandable block quotation continued
**>The last line of the block quotation"""

    text = """bold, bold
italic, italic
underline, underline
strikethrough, strikethrough, strikethrough
spoiler, spoiler
bold italic bold italic bold strikethrough italic bold strikethrough spoiler underline italic bold bold
inline URL
👍
22:45 tomorrow
22:45 tomorrow
22:45 tomorrow
22:45 tomorrow
inline fixed-width code

pre-formatted fixed-width code block

pre-formatted fixed-width code block written in the Python programming language
Block quotation started
Block quotation continued
The last line of the block quotation
Expandable block quotation started
Expandable block quotation continued
Expandable block quotation continued
Hidden by default part of the block quotation started
Expandable block quotation continued
The last line of the block quotation"""
    entities = entities = pyrogram.types.List([
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.BOLD, offset=0, length=4),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.BOLD, offset=6, length=4),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.ITALIC, offset=11, length=6),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.ITALIC, offset=19, length=6),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.UNDERLINE, offset=26, length=9),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.UNDERLINE, offset=37, length=9),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.STRIKETHROUGH, offset=47, length=13),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.STRIKETHROUGH, offset=62, length=13),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.STRIKETHROUGH, offset=77, length=13),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.SPOILER, offset=91, length=7),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.SPOILER, offset=100, length=7),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.BOLD, offset=108, length=103),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.ITALIC, offset=113, length=93),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.STRIKETHROUGH, offset=125, length=59),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.SPOILER, offset=151, length=33),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.UNDERLINE, offset=185, length=21),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.TEXT_LINK, offset=212, length=10, url="http://www.example.com/"),
        # TODO
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.DATE_TIME, offset=251, length=14, unix_time=1647531900, date_time_format="wDT"),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.DATE_TIME, offset=266, length=14, unix_time=1647531900, date_time_format="t"),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.DATE_TIME, offset=281, length=14, unix_time=1647531900, date_time_format="r"),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.DATE_TIME, offset=296, length=14, unix_time=1647531900, date_time_format=""),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.CODE, offset=311, length=23),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.PRE, offset=335, length=37, language=""),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.PRE, offset=373, length=80, language="python"),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.BLOCKQUOTE, offset=454, length=86),
        pyrogram.types.MessageEntity(type=pyrogram.enums.MessageEntityType.EXPANDABLE_BLOCKQUOTE, offset=541, length=236),
    ])

    assert Markdown.unparse(text=text, entities=entities) == expected


def test_markdown_unparse_no_entities():
    expected = "text"
    text = "text"
    entities = []

    assert Markdown.unparse(text=text, entities=entities) == expected
