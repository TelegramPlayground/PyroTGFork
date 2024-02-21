Changes in this Fork
=========

This page lists all the documented changes of this fork,
in reverse chronological order. You should read this when upgrading
to this fork to know where your code can break, and where
it can take advantage of new goodies!

`For a more detailed description, you can check the commits. <https://github.com/TelegramPlayGround/pyrogram/>`_

+------------------------+
|   Leaked Scheme layer  |
+------------------------+

- Renamed ``placeholder`` to ``input_field_placeholder`` in :obj:`~pyrogram.types.ReplyKeyboardMarkup`
- `#693 <https://github.com/KurimuzonAkuma/pyrogram/pull/693>`_
- Revert `e678c05 <https://github.com/TelegramPlayGround/pyrogram/commit/e678c054d4aa0bbbb7d583eb426ca8753a4c9354>_` and stole squashed unauthored changes from `bcd18d5 <https://github.com/Masterolic/pyrogram/commit/bcd18d5e04f18f949389a03f309816d6f0f9eabe>_`

+------------------------+
| Scheme layer used: 174 |
+------------------------+

- Added the field ``story`` to the class :obj:`~pyrogram.types.Message` for messages with forwarded stories. Currently, it holds no information.
- Added the class :obj:`~pyrogram.types.ChatBoostAdded` and the field ``boost_added`` to the class :obj:`~pyrogram.types.Message` for service messages about a user boosting a chat.
- Added the field ``custom_emoji_sticker_set_name`` to the class :obj:`~pyrogram.types.Chat`.
- Added the field ``unrestrict_boost_count`` to the class :obj:`~pyrogram.types.Chat`.
- Added the field ``sender_boost_count`` to the class :obj:`~pyrogram.types.Message`.

+------------------------+
| Scheme layer used: 173 |
+------------------------+

- Fix ConnectionResetError when only ping task (`#24 <https://github.com/KurimuzonAkuma/pyrogram/pull/24>`_)
- Added ``is_topic_message`` to the :obj:`~pyrogram.types.Message` object.
- Added ``has_visible_history``, ``has_hidden_members``, ``has_aggressive_anti_spam_enabled``, ``message_auto_delete_time``, ``slow_mode_delay``, ``slowmode_next_send_date``, ``is_forum`` to the :obj:`~pyrogram.types.Chat` object.
- Added ``add_to_recent``, ``story_id`` parameters in :obj:`~pyrogram.Client.set_message_reaction`.
- Bug fix in parsing ``Vector<Bool>`` (Thanks to `@AmarnathCJD <https://github.com/AmarnathCJD/>`_ and `@roj1512 <https://github.com/roj1512>`_).
- Documentation Fix of ``max_concurrent_transmissions`` type hint.
- Bug Fix in the ``get_file`` method. (Thanks to `@ALiwoto <https://github.com/ALiwoto>`_).
- Added missing attributes to :obj:`~pyrogram.types.ChatPermissions` and :obj:`~pyrogram.types.ChatPrivileges`.
- `Bug Fix for MIN_CHAT_ID <https://t.me/pyrogramchat/593090>`_.
- Added new parameter ``no_joined_notifications`` to :obj:`~pyrogram.Client`.
- Fix history TTL Service Message Parse.
- Added environment variables ``PYROGRAM_DONOT_LOG_UNKNOWN_ERRORS``. Thanks to `... <https://t.me/pyrogramchat/607757>`_.
- Renamed ``force_document`` to ``disable_content_type_detection`` in :obj:`~pyrogram.Client.send_document` and :obj:`~pyrogram.types.Message.reply_document`.
- Added missing attributes ``added_to_attachment_menu``, ``is_attachment_menu_adding_available``, ``can_join_groups``, ``can_read_all_group_messages``, ``supports_inline_queries``, ``can_be_contacted_with_premium`` to the :obj:`~pyrogram.types.User`.
- Migrate project to ``pyproject.toml`` from ``setup.py``.
- PRs from upstream: `1366 <https://github.com/pyrogram/pyrogram/pull/1366>`_, `1305 <https://github.com/pyrogram/pyrogram/pull/1305>`_, `1288 <https://github.com/pyrogram/pyrogram/pull/1288>`_, `1262 <https://github.com/pyrogram/pyrogram/pull/1262>`_, `1253 <https://github.com/pyrogram/pyrogram/pull/1253>`_, `1234 <https://github.com/pyrogram/pyrogram/pull/1234>`_, `1210 <https://github.com/pyrogram/pyrogram/pull/1210>`_, `1201 <https://github.com/pyrogram/pyrogram/pull/1201>`_, `1197 <https://github.com/pyrogram/pyrogram/pull/1197>`_, `1143 <https://github.com/pyrogram/pyrogram/pull/1143>`_, `1059 <https://github.com/pyrogram/pyrogram/pull/1059>`_.
- Bug fix for :obj:`~pyrogram.Client.send_audio` and :obj:`~pyrogram.Client.send_voice`. (Thanks to `... <https://t.me/c/1220993104/1360174>`_).
- Add `waveform` parameter to :obj:`~pyrogram.Client.send_voice`.
- Added `view_once` parameter to :obj:`~pyrogram.Client.send_photo`, :obj:`~pyrogram.Client.send_video`, :obj:`~pyrogram.Client.send_video_note`, :obj:`~pyrogram.Client.send_voice`.
- Add missing parameters to :obj:`~pyrogram.types.Message.reply_photo`, :obj:`~pyrogram.types.Message.reply_video`, :obj:`~pyrogram.types.Message.reply_video_note`, :obj:`~pyrogram.types.Message.reply_voice`.

+------------------------+
| Scheme layer used: 170 |
+------------------------+

- Stole documentation from `https://github.com/PyrogramMod/PyrogramMod`.
- Removed `send_reaction` and Added `set_message_reaction`.
- Added support for voice, photo, video, animation messages that could be played once.
- Added ``_raw`` to the :obj:`~pyrogram.types.Chat` object.
- Added the field ``via_chat_folder_invite_link`` to the class :obj:`~pyrogram.types.ChatMemberUpdated`.
- **BOTS ONLY**: Added updates about a reaction change on a message with non-anonymous reactions, represented by the class :obj:`~pyrogram.handlers.MessageReactionUpdatedHandler` and the field ``message_reaction`` in the class Update.
- **BOTS ONLY**: Added updates about reaction changes on a message with anonymous reactions, represented by the class :obj:`~pyrogram.handlers.MessageReactionCountUpdatedHandler` and the field ``message_reaction_count`` in the class Update.
- Replaced the parameter ``disable_web_page_preview`` with :obj:`~pyrogram.types.LinkPreviewOptions` in the methods sendMessage and editMessageText.
- Replaced the field ``disable_web_page_preview`` with :obj:`~pyrogram.types.LinkPreviewOptions` in the class InputTextMessageContent.
- Added missing parameters to :obj:`~pyrogram.Client.forward_messages`.
- Added the class :obj:`~pyrogram.types.ReplyParameters` and replaced parameters ``reply_to_message_id`` in the methods :meth:`~pyrogram.Client.copy_message`, :meth:`~pyrogram.Client.forward_messages`, :meth:`~pyrogram.Client.send_message`, :meth:`~pyrogram.Client.send_photo`, :meth:`~pyrogram.Client.send_video`, :meth:`~pyrogram.Client.send_animation`, :meth:`~pyrogram.Client.send_audio`, :meth:`~pyrogram.Client.send_document`, :meth:`~pyrogram.Client.send_sticker`, :meth:`~pyrogram.Client.send_video_note`, :meth:`~pyrogram.Client.send_voice`, :meth:`~pyrogram.Client.send_location`, :meth:`~pyrogram.Client.send_venue`, :meth:`~pyrogram.Client.send_contact`, :meth:`~pyrogram.Client.send_poll`, :meth:`~pyrogram.Client.send_dice`, :meth:`~pyrogram.Client.send_game`, :meth:`~pyrogram.Client.send_media_group`, :meth:`~pyrogram.Client.copy_media_group`, :meth:`~pyrogram.Client.send_inline_bot_result`, :meth:`~pyrogram.Client.send_cached_media`, and the corresponding reply_* methods with the field ``reply_parameters`` of type :obj:`~pyrogram.types.ReplyParameters`.
- Bug fixes for sending ``ttl_seconds`` and ``has_spoiler``.

+------------------------+
| Scheme layer used: 169 |
+------------------------+

- Changed condition in :meth:`~pyrogram.Client.join_chat` and :meth:`~pyrogram.Client.get_chat`.
- Added ``nosound_video`` parameter to :obj:`~pyrogram.types.InputMediaVideo`.
- Added ``has_spoiler`` parameter to :meth:`~pyrogram.Client.copy_message`.
- Improved :meth:`~pyrogram.Client.get_chat_history`: add ``min_id`` and ``max_id`` params.
- Improved ``send_reaction`` for Telegram Premium Users.
- `Prevent connection to dc every time in get_file <https://github.com/TelegramPlayGround/pyrogram/commit/f2581fd7ab84ada7685645a6f80475fbea5e743a>`_
- Added ``_raw`` to the :obj:`~pyrogram.types.Chat`, :obj:`~pyrogram.types.Dialog`, and :obj:`~pyrogram.types.User` objects.
- Fix downloading media to ``WORKDIR`` when ``WORKDIR`` was not specified.
- `Update multiple fragment chat usernames <https://github.com/TelegramPlayGround/pyrogram/commit/39aea4831ee18e5263bf6755306f0ca49f075bda>`_
- `Custom Storage Engines <https://github.com/TelegramPlayGround/pyrogram/commit/cd937fff623759dcac8f437a8c524684868590a4>`_
- Documentation fix for ``user.mention`` in :obj:`~pyrogram.types.User`.

+------------------------+
| Scheme layer used: 167 |
+------------------------+

- Fixed the TL flags being Python reserved keywords: ``from`` and ``self``.

+------------------------+
| Scheme layer used: 164 |
+------------------------+

- Added ``_raw`` to the :obj:`~pyrogram.types.Message` object.

+------------------------+
| Scheme layer used: 161 |
+------------------------+

- Added ``my_stories_from`` to the :meth:`~pyrogram.Client.block_user` and :meth:`~pyrogram.Client.unblock_user` methods.

+------------------------+
| Scheme layer used: 160 |
+------------------------+

- Added ``message_thread_id`` to the methods :meth:`~pyrogram.Client.copy_message`, :meth:`~pyrogram.Client.forward_messages`, :meth:`~pyrogram.Client.send_message`, :meth:`~pyrogram.Client.send_photo`, :meth:`~pyrogram.Client.send_video`, :meth:`~pyrogram.Client.send_animation`, :meth:`~pyrogram.Client.send_audio`, :meth:`~pyrogram.Client.send_document`, :meth:`~pyrogram.Client.send_sticker`, :meth:`~pyrogram.Client.send_video_note`, :meth:`~pyrogram.Client.send_voice`, :meth:`~pyrogram.Client.send_location`, :meth:`~pyrogram.Client.send_venue`, :meth:`~pyrogram.Client.send_contact`, :meth:`~pyrogram.Client.send_poll`, :meth:`~pyrogram.Client.send_dice`, :meth:`~pyrogram.Client.send_game`, :meth:`~pyrogram.Client.send_media_group`, :meth:`~pyrogram.Client.copy_media_group`, :meth:`~pyrogram.Client.send_inline_bot_result`, :meth:`~pyrogram.Client.send_cached_media`.
