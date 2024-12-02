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


import logging
import os
import sqlite3
from pathlib import Path

from .sqlite_storage import SQLiteStorage

log = logging.getLogger(__name__)

USERNAMES_SCHEMA = """
CREATE TABLE usernames
(
    id       INTEGER,
    username TEXT,
    FOREIGN KEY (id) REFERENCES peers(id)
);

CREATE INDEX idx_usernames_username ON usernames (username);
"""

UPDATE_STATE_SCHEMA = """
CREATE TABLE update_state
(
    id   INTEGER PRIMARY KEY,
    pts  INTEGER,
    qts  INTEGER,
    date INTEGER,
    seq  INTEGER
);
"""


class FileStorage(SQLiteStorage):
    FILE_EXTENSION = ".session"

    def __init__(self, name: str, workdir: Path):
        super().__init__(name)

        self.database = workdir / (self.name + self.FILE_EXTENSION)

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
            self.conn.executescript(USERNAMES_SCHEMA)

    def _update_from_four_impl(self):
        with self.conn:
            self.conn.executescript(UPDATE_STATE_SCHEMA)

    def _update_from_five_impl(self):
        with self.conn:
            self.conn.executescript("CREATE INDEX idx_usernames_id ON usernames (id);")

    def _connect_impl(self, path):
        self.conn = sqlite3.connect(str(path), timeout=1, check_same_thread=False)

        with self.conn:
            self.conn.execute("PRAGMA journal_mode=WAL").close()
            self.conn.execute("PRAGMA synchronous=NORMAL").close()
            self.conn.execute("PRAGMA temp_store=1").close()

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

    async def open(self):
        path = self.database
        file_exists = path.is_file()

        self.executor.submit(self._connect_impl, path).result()

        if not file_exists:
            await self.create()
        else:
            await self.update()

        await self.loop.run_in_executor(self.executor, self._vacuum)

    async def delete(self):
        os.remove(self.database)
