#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2017-present bakatrouble <https://github.com/bakatrouble>
#  Copyright (C) 2017-present cavallium <https://github.com/cavallium>
#  Copyright (C) 2017-present andrew-ld <https://github.com/andrew-ld>
#  Copyright (C) 2017-present 01101sam <https://github.com/01101sam>
#  Copyright (C) 2017-present KurimuzonAkuma <https://github.com/KurimuzonAkuma>
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

import asyncio
import base64
import inspect
import logging
import sqlite3
import struct
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import Any, Optional

from pyrogram import raw
from .storage import Storage
from .. import utils

log = logging.getLogger(__name__)


# language=SQLite
SCHEMA = """
CREATE TABLE sessions
(
    dc_id     INTEGER PRIMARY KEY,
    api_id    INTEGER,
    test_mode INTEGER,
    auth_key  BLOB,
    date      INTEGER NOT NULL,
    user_id   INTEGER,
    is_bot    INTEGER
);

CREATE TABLE peers
(
    id             INTEGER PRIMARY KEY,
    access_hash    INTEGER,
    type           INTEGER NOT NULL,
    phone_number   TEXT,
    last_update_on INTEGER NOT NULL DEFAULT (CAST(STRFTIME('%s', 'now') AS INTEGER))
);

CREATE TABLE usernames
(
    id       INTEGER,
    username TEXT,
    FOREIGN KEY (id) REFERENCES peers(id)
);

CREATE TABLE update_state
(
    id   INTEGER PRIMARY KEY,
    pts  INTEGER,
    qts  INTEGER,
    date INTEGER,
    seq  INTEGER
);

CREATE TABLE version
(
    number INTEGER PRIMARY KEY
);

CREATE INDEX IF NOT EXISTS idx_peers_id ON peers (id);
CREATE INDEX IF NOT EXISTS idx_peers_phone_number ON peers (phone_number);
CREATE INDEX IF NOT EXISTS idx_usernames_id ON usernames (id);
CREATE INDEX IF NOT EXISTS idx_usernames_username ON usernames (username);

CREATE TRIGGER trg_peers_last_update_on
    AFTER UPDATE
    ON peers
BEGIN
    UPDATE peers
    SET last_update_on = CAST(STRFTIME('%s', 'now') AS INTEGER)
    WHERE id = NEW.id;
END;
"""


def get_input_peer(peer_id: int, access_hash: int, peer_type: str):
    if peer_type in ["user", "bot"]:
        return raw.types.InputPeerUser(
            user_id=peer_id,
            access_hash=access_hash
        )

    if peer_type == "group":
        return raw.types.InputPeerChat(
            chat_id=-peer_id
        )

    if peer_type in ["channel", "supergroup"]:
        return raw.types.InputPeerChannel(
            channel_id=utils.get_channel_id(peer_id),
            access_hash=access_hash
        )

    raise ValueError(f"Invalid peer type: {peer_type}")


class SQLiteStorage(Storage):
    VERSION = 6
    USERNAME_TTL = 8 * 60 * 60
    FILE_EXTENSION = ".session"

    def __init__(
        self,
        name: str,
        workdir: Path,
        session_string: Optional[str] = None,
        in_memory: Optional[bool] = False,
        use_wal: Optional[bool] = True,
    ):
        super().__init__(name)

        self._executor = None
        self.loop = utils.get_event_loop()
        self.conn = None  # type: sqlite3.Connection | None

        self.session_string = session_string
        self.in_memory = in_memory
        self.use_wal = use_wal

        if self.in_memory:
            self.database = ":memory:"
        else:
            self.database = workdir / (self.name + self.FILE_EXTENSION)

    @property
    def executor(self):
        if self._executor is None:
           self._executor = ThreadPoolExecutor(1)
        return self._executor

    def _vacuum(self):
        with self.conn:
            self.conn.execute("VACUUM")

    def _update_from_one_impl(self):
        with self.conn:
            self.conn.execute("DELETE FROM peers")

    def _update_from_two_impl(self):
        with self.conn:
            self.conn.execute("ALTER TABLE sessions ADD api_id INTEGER")

    def _update_from_three_impl(self):
        with self.conn:
            self.conn.executescript("""
CREATE TABLE usernames
(
    id       INTEGER,
    username TEXT,
    FOREIGN KEY (id) REFERENCES peers(id)
);

CREATE INDEX idx_usernames_username ON usernames (username);
""")

    def _update_from_four_impl(self):
        with self.conn:
            self.conn.executescript("""
CREATE TABLE update_state
(
    id   INTEGER PRIMARY KEY,
    pts  INTEGER,
    qts  INTEGER,
    date INTEGER,
    seq  INTEGER
);
""")

    def _update_from_five_impl(self):
        with self.conn:
            self.conn.executescript("CREATE INDEX idx_usernames_id ON usernames (id);")

    async def update(self):
        version = await self.version()

        if version == 1:
            await self.loop.run_in_executor(self.executor, self._update_from_one_impl)
            version += 1

        if version == 2:
            await self.loop.run_in_executor(self.executor, self._update_from_two_impl)
            version += 1

        if version == 3:
            await self.loop.run_in_executor(self.executor, self._update_from_three_impl)
            version += 1

        if version == 4:
            await self.loop.run_in_executor(self.executor, self._update_from_four_impl)
            version += 1

        if version == 5:
            await self.loop.run_in_executor(self.executor, self._update_from_five_impl)
            version += 1

        await self.version(version)

    def _connect_impl(self, path):
        self.conn = sqlite3.connect(str(path), timeout=1, check_same_thread=False)

        with self.conn:
            if self.use_wal:
                self.conn.execute("PRAGMA journal_mode=WAL").close()
            else:
                self.conn.execute("PRAGMA journal_mode=DELETE").close()
            self.conn.execute("PRAGMA synchronous=NORMAL").close()
            self.conn.execute("PRAGMA temp_store=1").close()

    def _create_impl(self):
        with self.conn:
            self.conn.executescript(SCHEMA)

            self.conn.execute(
                "INSERT INTO version VALUES (?)",
                (self.VERSION,)
            )

            self.conn.execute(
                "INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?, ?)",
                (2, None, None, None, 0, None, None)
            )

    async def create(self):
        return await self.loop.run_in_executor(self.executor, self._create_impl)

    async def open(self):
        if self.in_memory:
            connfunc = partial(sqlite3.connect, ":memory:", timeout=1, check_same_thread=False)
            self.conn = await self.loop.run_in_executor(self.executor, connfunc)
            await self.create()

            if self.session_string:
                # Old format
                if len(self.session_string) in [
                    self.SESSION_STRING_SIZE,
                    self.SESSION_STRING_SIZE_64,
                ]:
                    dc_id, test_mode, auth_key, user_id, is_bot = struct.unpack(
                        (
                            self.OLD_SESSION_STRING_FORMAT
                            if len(self.session_string) == self.SESSION_STRING_SIZE
                            else self.OLD_SESSION_STRING_FORMAT_64
                        ),
                        base64.urlsafe_b64decode(
                            self.session_string + "=" * (-len(self.session_string) % 4)
                        ),
                    )

                    await self.dc_id(dc_id)
                    await self.test_mode(test_mode)
                    await self.auth_key(auth_key)
                    await self.user_id(user_id)
                    await self.is_bot(is_bot)
                    await self.date(0)

                    log.warning(
                        "You are using an old session string format. Use export_session_string to update"
                    )
                    return

                dc_id, api_id, test_mode, auth_key, user_id, is_bot = struct.unpack(
                    self.SESSION_STRING_FORMAT,
                    base64.urlsafe_b64decode(
                        self.session_string + "=" * (-len(self.session_string) % 4)
                    ),
                )

                await self.dc_id(dc_id)
                await self.api_id(api_id)
                await self.test_mode(test_mode)
                await self.auth_key(auth_key)
                await self.user_id(user_id)
                await self.is_bot(is_bot)
                await self.date(0)

            return

        path = self.database
        file_exists = isinstance(path, Path) and path.is_file()

        self.executor.submit(self._connect_impl, path).result()

        if not file_exists:
            await self.create()
        else:
            await self.update()

        await self.loop.run_in_executor(self.executor, self._vacuum)

    async def save(self):
        await self.date(int(time.time()))
        await self.loop.run_in_executor(self.executor, self.conn.commit)

    async def close(self):
        await self.loop.run_in_executor(self.executor, self.conn.close)
        self.executor.shutdown()
        self._executor = None 
        
    async def delete(self):
        if not self.in_memory:
            Path(self.database).unlink()

    def _update_peers_impl(self, peers):
        with self.conn:
            peers_data = []
            usernames_data = []
            ids_to_delete = []
            for id, access_hash, type, usernames, phone_number in peers:
                ids_to_delete.append((id,))
                peers_data.append((id, access_hash, type, phone_number))

                if usernames:
                    usernames_data.extend([(id, username) for username in usernames])

            self.conn.executemany(
                "REPLACE INTO peers (id, access_hash, type, phone_number) VALUES (?, ?, ?, ?)",
                peers_data
            )

            self.conn.executemany(
                "DELETE FROM usernames WHERE id = ?",
                ids_to_delete
            )

            if usernames_data:
                self.conn.executemany(
                    "REPLACE INTO usernames (id, username) VALUES (?, ?)",
                    usernames_data
                )

    async def update_peers(self, peers: list[tuple[int, int, str, list[str], str]]):
        return await self.loop.run_in_executor(self.executor, self._update_peers_impl, peers)

    def _update_usernames_impl(self, usernames: list[tuple[int, list[str]]]):
        with self.conn:
            self.conn.executemany("DELETE FROM usernames WHERE id = ?", [(id,) for id, _ in usernames])

            self.conn.executemany(
                "REPLACE INTO usernames (id, username) VALUES (?, ?)",
                [(id, username) for id, usernames in usernames for username in usernames],
            )

    async def update_usernames(self, usernames: list[tuple[int, list[str]]]):
        return await self.loop.run_in_executor(self.executor, self._update_usernames_impl, usernames)

    def _update_state_impl(self, value: tuple[int, int, int, int, int] = object):
        if value == object:
            return self.conn.execute(
                "SELECT id, pts, qts, date, seq FROM update_state "
                "ORDER BY date ASC"
            ).fetchall()
        else:
            with self.conn:
                if isinstance(value, int):
                    self.conn.execute(
                        "DELETE FROM update_state WHERE id = ?",
                        (value,)
                    )
                else:
                    self.conn.execute(
                        "REPLACE INTO update_state (id, pts, qts, date, seq)"
                        "VALUES (?, ?, ?, ?, ?)",
                        value
                    )

    async def update_state(self, value: tuple[int, int, int, int, int] = object):
        return await self.loop.run_in_executor(self.executor, self._update_state_impl, value)

    def _get_peer_by_id_impl(self, peer_id: int):
        with self.conn:
            return self.conn.execute(
                "SELECT id, access_hash, type FROM peers WHERE id = ?",
                (peer_id,)
            ).fetchone()

    async def get_peer_by_id(self, peer_id: int):
        r = await self.loop.run_in_executor(self.executor, self._get_peer_by_id_impl, peer_id)

        if r is None:
            raise KeyError(f"ID not found: {peer_id}")

        return get_input_peer(*r)

    def _get_peer_by_username_impl(self, username: str):
        with self.conn:
            return self.conn.execute(
                "SELECT p.id, p.access_hash, p.type, p.last_update_on FROM peers p "
                "JOIN usernames u ON p.id = u.id "
                "WHERE u.username = ? "
                "ORDER BY p.last_update_on DESC",
                (username,)
            ).fetchone()

    async def get_peer_by_username(self, username: str):
        r = await self.loop.run_in_executor(self.executor, self._get_peer_by_username_impl, username)

        if r is None:
            raise KeyError(f"Username not found: {username}")

        if abs(time.time() - r[3]) > self.USERNAME_TTL:
            raise KeyError(f"Username expired: {username}")

        return get_input_peer(*r[:3])

    def _get_peer_by_phone_number_impl(self, phone_number: str):
        with self.conn:
            return self.conn.execute(
                "SELECT id, access_hash, type FROM peers WHERE phone_number = ?",
                (phone_number,)
            ).fetchone()

    async def get_peer_by_phone_number(self, phone_number: str):
        r = await self.loop.run_in_executor(self.executor, self._get_peer_by_phone_number_impl, phone_number)

        if r is None:
            raise KeyError(f"Phone number not found: {phone_number}")

        return get_input_peer(*r)

    def _get_impl(self, attr: str):
        with self.conn:
            return self.conn.execute(f"SELECT {attr} FROM sessions").fetchone()[0]

    # async def _get(self, attr: str):
    #     return await self.loop.run_in_executor(self.executor, self._get_impl, attr)

    async def _get(self):
        attr = inspect.stack()[2].function
        return await self.loop.run_in_executor(self.executor, self._get_impl, attr)

    def _set_impl(self, attr: str, value: any):
        with self.conn:
            return self.conn.execute(f"UPDATE sessions SET {attr} = ?", (value,))

    # async def _set(self, attr: str, value: Any):
    #     return await self.loop.run_in_executor(self.executor, self._set_impl, attr, value)

    async def _set(self, value: Any):
        attr = inspect.stack()[2].function

        return await self.loop.run_in_executor(self.executor, self._set_impl, attr, value)

    async def _accessor(self, value: Any = object):
        # return await self._get(attr) if value == object else await self._set(attr, value)
        return await self._get() if value == object else await self._set(value)
    
    def _get_version_impl(self):
        with self.conn:
            return self.conn.execute("SELECT number FROM version").fetchone()[0]

    def _set_version_impl(self, value):
        with self.conn:
            return self.conn.execute("UPDATE version SET number = ?", (value,))

    async def dc_id(self, value: int = object):
        return await self._accessor(value)

    async def api_id(self, value: int = object):
        return await self._accessor(value)

    async def test_mode(self, value: bool = object):
        return await self._accessor(value)

    async def auth_key(self, value: bytes = object):
        return await self._accessor(value)

    async def date(self, value: int = object):
        return await self._accessor(value)

    async def user_id(self, value: int = object):
        return await self._accessor(value)

    async def is_bot(self, value: bool = object):
        return await self._accessor(value)

    async def version(self, value: int = object):
        if value == object:
            return await self.loop.run_in_executor(self.executor, self._get_version_impl)
        else:
            return await self.loop.run_in_executor(self.executor, self._set_version_impl, value)
