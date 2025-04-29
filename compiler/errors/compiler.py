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

import csv
import os
import re
import shutil

HOME = "compiler/errors"
DEST = "pyrogram/errors/exceptions"
NOTICE_PATH = "NOTICE"


def snek(s):
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def caml(s):
    s = snek(s).split("_")
    return "".join([str(i.title()) for i in s])


def start():
    shutil.rmtree(DEST, ignore_errors=True)
    os.makedirs(DEST)

    files = [i for i in os.listdir(f"{HOME}/source")]

    with open(NOTICE_PATH, encoding="utf-8") as f:
        notice = []

        for line in f.readlines():
            notice.append(f"# {line}".strip())

        notice = "\n".join(notice)

    with open(f"{DEST}/all.py", "w", encoding="utf-8") as f_all:
        f_all.write(notice + "\n\n")
        f_all.write("count = {count}\n\n")
        f_all.write("exceptions = {\n")

        count = 0

        for i in files:
            code, name = re.search(r"(\d+)_([A-Z_]+)", i).groups()

            f_all.write(f"    {code}: {{\n")

            init = f"{DEST}/__init__.py"

            if not os.path.exists(init):
                with open(init, "w", encoding="utf-8") as f_init:
                    f_init.write(notice + "\n\n")

            with open(init, "a", encoding="utf-8") as f_init:
                f_init.write(f"from .{name.lower()}_{code} import *\n")

            with open(f"{HOME}/source/{i}", encoding="utf-8") as f_csv, \
                open(f"{DEST}/{name.lower()}_{code}.py", "w", encoding="utf-8") as f_class:
                reader = csv.reader(f_csv, delimiter="\t")

                super_class = caml(name)
                name = " ".join([str(i.capitalize()) for i in name.replace(r"_", " ").lower().split(" ")])

                sub_classes = []

                f_all.write(f"        \"_\": \"{super_class}\",\n")

                for j, row in enumerate(reader):
                    if j == 0:
                        continue

                    count += 1

                    if not row:  # Row is empty (blank line)
                        continue

                    error_id, error_message = row

                    sub_class = caml(error_id.replace(r"_X", "_"))
                    sub_class = re.sub(r"^2", "Two", sub_class)
                    sub_class = sub_class.replace(r" ", "")

                    f_all.write(f"        \"{error_id}\": \"{sub_class}\",\n")

                    sub_classes.append((sub_class, error_id, error_message))

                with open(f"{HOME}/template/class.txt", encoding="utf-8") as f_class_template:
                    class_template = f_class_template.read()

                    with open(f"{HOME}/template/sub_class.txt", encoding="utf-8") as f_sub_class_template:
                        sub_class_template = f_sub_class_template.read()

                    class_template = class_template.format(
                        notice=notice,
                        super_class=super_class,
                        code=code,
                        docstring=f'"""{name}"""',
                        sub_classes="".join([sub_class_template.format(
                            sub_class=k[0],
                            super_class=super_class,
                            id=f"\"{k[1]}\"",
                            docstring=f'"""{k[2]}"""'
                        ) for k in sub_classes])
                    )

                f_class.write(class_template)

            f_all.write("    },\n")

        f_all.write("}\n")

    with open(f"{DEST}/all.py", encoding="utf-8") as f:
        content = f.read()

    with open(f"{DEST}/all.py", "w", encoding="utf-8") as f:
        f.write(re.sub(r"{count}", str(count), content))


if __name__ == "__main__":
    HOME = "."
    DEST = "../../pyrogram/errors/exceptions"
    NOTICE_PATH = "../../NOTICE"

    start()
