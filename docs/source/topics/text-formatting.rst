Text Formatting
===============

.. role:: strike
    :class: strike

.. role:: underline
    :class: underline

.. role:: bold-underline
    :class: bold-underline

.. role:: strike-italic
    :class: strike-italic

Pyrogram uses a custom Markdown dialect for text formatting which adds some unique features that make writing styled
texts easier in both Markdown and HTML. You can send sophisticated text messages and media captions using a
variety of decorations that can also be nested in order to combine multiple styles together.


-----

Basic Styles
------------

When formatting your messages, you can choose between Markdown-style, HTML-style or both (default). The following is a
list of the basic styles currently supported by Pyrogram.

- **bold**
- *italic*
- :underline:`underline`
- :strike:`strike`
- blockquote
- ``inline fixed-width code``
- .. code-block:: text

    pre-formatted
      fixed-width
        code block
- spoiler
- `text URL <https://telegramplayground.github.io/pyrogram/>`_
- `user text mention <tg://user?id=123456789>`_



Markdown Style
--------------

To strictly use this mode, pass :obj:`~pyrogram.enums.ParseMode.MARKDOWN` to the *parse_mode* parameter when using
:meth:`~pyrogram.Client.send_message`. Use the following syntax in your message:

.. code-block:: text

    **bold**

    __italic__

    --underline--

    ~~strike~~

    >blockquote

    |>escaped blockquote 

    >Fist line of multi line blockquote 
    >Block quotation continued
    >Block quotation continued
    >Block quotation continued
    >The last line of the block quotation

    **>
    The expandable block quotation started right after the previous block quotation
    It is separated from the previous block quotation by expandable syntax 
    Expandable block quotation continued
    Hidden by default part of the expandable block quotation started
    Expandable block quotation continued
    The last line of the expandable block quotation with the expandability mark<**

    `inline fixed-width code`

    ```
    pre-formatted
      fixed-width
        code block
    ```

    ||spoiler||

    [text URL](https://telegramplayground.github.io/pyrogram/)

    [text user mention](tg://user?id=123456789)


**Example**:

.. code-block:: python

    from pyrogram import enums

    await app.send_message(
        chat_id="me",
        text=(
            "**bold**, "
            "__italic__, "
            "--underline--, "
            "~~strike~~, "
            "||spoiler||, "
            "[URL](https://telegramplayground.github.io/pyrogram/), "
            "`code`, "
            "```"
            "for i in range(10):\n"
            "    print(i)"
            "```"

            ">blockquote\n"

            "|>escaped blockquote\n"

            ">Fist line of multi line blockquote\n"
            ">Block quotation continued\n"
            ">Block quotation continued\n"
            ">Block quotation continued\n"
            ">The last line of the block quotation"

            "**>\n"
            "The expandable block quotation started right after the previous block quotation\n"
            "It is separated from the previous block quotation by expandable syntax\n"
            "Expandable block quotation continued\n"
            "Hidden by default part of the expandable block quotation started\n"
            "Expandable block quotation continued\n"
            "The last line of the expandable block quotation with the expandability mark<**"

        ),
        parse_mode=enums.ParseMode.MARKDOWN
    )

HTML Style
----------

To strictly use this mode, pass :obj:`~pyrogram.enums.HTML` to the *parse_mode* parameter when using
:meth:`~pyrogram.Client.send_message`. The following tags are currently supported:

.. code-block:: text

    <b>bold</b>, <strong>bold</strong>

    <i>italic</i>, <em>italic</em>

    <u>underline</u>

    <s>strike</s>, <del>strike</del>, <strike>strike</strike>

    <spoiler>spoiler</spoiler>

    <a href="https://telegramplayground.github.io/pyrogram/">text URL</a>

    <a href="tg://user?id=123456789">inline mention</a>

    <code>inline fixed-width code</code>

    <emoji id="12345678901234567890">🔥</emoji>

    <pre language="py">
    pre-formatted
      fixed-width
        code block
    </pre>

**Example**:

.. code-block:: python

    from pyrogram import enums

    await app.send_message(
        chat_id="me",
        text=(
            "<b>bold</b>, "
            "<i>italic</i>, "
            "<u>underline</u>, "
            "<s>strike</s>, "
            "<spoiler>spoiler</spoiler>, "
            "<a href=\"https://telegramplayground.github.io/pyrogram/\">URL</a>, "
            "<code>code</code>\n\n"
            "<pre language='py'>"
            "for i in range(10):\n"
            "    print(i)"
            "</pre>"
        ),
        parse_mode=enums.ParseMode.HTML
    )

.. note::

    All ``<``, ``>`` and ``&`` symbols that are not a part of a tag or an HTML entity must be replaced with the
    corresponding HTML entities (``<`` with ``&lt;``, ``>`` with ``&gt;`` and ``&`` with ``&amp;``). You can use this
    snippet to quickly escape those characters:

    .. code-block:: python

        import html

        text = "<my text>"
        text = html.escape(text)

        print(text)

    .. code-block:: text

        &lt;my text&gt;

Different Styles
----------------

By default, when ignoring the *parse_mode* parameter, both Markdown and HTML styles are enabled together.
This means you can combine together both syntaxes in the same text:

.. code-block:: python

    await app.send_message(chat_id="me", text="**bold**, <i>italic</i>")

Result:

    **bold**, *italic*

If you don't like this behaviour you can always choose to only enable either Markdown or HTML in strict mode by passing
:obj:`~pyrogram.enums.MARKDOWN` or :obj:`~pyrogram.enums.HTML` as argument to the *parse_mode* parameter.

.. code-block:: python

    from pyrogram import enums

    await app.send_message(chat_id="me", text="**bold**, <i>italic</i>", parse_mode=enums.ParseMode.MARKDOWN)
    await app.send_message(chat_id="me", text="**bold**, <i>italic</i>", parse_mode=enums.ParseMode.HTML)

Result:

    **bold**, <i>italic</i>

    \*\*bold**, *italic*

In case you want to completely turn off the style parser, simply pass :obj:`~pyrogram.enums.DISABLED` to *parse_mode*.
The text will be sent as-is.

.. code-block:: python

    from pyrogram import enums

    await app.send_message(chat_id="me", text="**bold**, <i>italic</i>", parse_mode=enums.ParseMode.DISABLED)

Result:

    \*\*bold**, <i>italic</i>

Nested and Overlapping Entities
-------------------------------

You can also style texts with more than one decoration at once by nesting entities together. For example, you can send
a text message with both :bold-underline:`bold and underline` styles, or a text that has both :strike-italic:`italic and
strike` styles, and you can still combine both Markdown and HTML together.

Here there are some example texts you can try sending:

**Markdown**:

- ``**bold, --underline--**``
- ``**bold __italic --underline ~~strike~~--__**``
- ``**bold __and** italic__``

**HTML**:

- ``<b>bold, <u>underline</u></b>``
- ``<b>bold <i>italic <u>underline <s>strike</s></u></i></b>``
- ``<b>bold <i>and</b> italic</i>``

**Combined**:

- ``--you can combine <i>HTML</i> with **Markdown**--``
- ``**and also <i>overlap** --entities</i> this way--``
