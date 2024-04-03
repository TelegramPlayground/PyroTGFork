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
from pathlib import Path
import re
import requests  # requests==2.28.1
import sys

if len(sys.argv) != 2:
    sys.exit(1)

if sys.argv[1] == "sort": 
    for p in Path("source").glob("*.tsv"):
        with open(p) as f:
            reader = csv.reader(f, delimiter="\t")
            dct = {k: v for k, v in reader if k != "id"}
            keys = sorted(dct)

        with open(p, "w") as f:
            f.write("id\tmessage\n")

            for i, item in enumerate(keys, start=1):
                f.write(f"{item}\t{dct[item]}")

                if i != len(keys):
                    f.write("\n")

elif sys.argv[1] == "scrape":
    b = "https://core.telegram.org"
    c = "/api/errors"
    a = requests.get(b + c)
    d = a.text
    e = r"\<a\ href\=\"(.*)\"\>here.*\<\/a\>"
    f = re.search(e, d)
    if f:
        a = requests.get(
            b + f.group(1)
        )
        d = a.json()
        e = d.get("errors", [])
        for h in e:
            dct = {}

            for p in Path("source/").glob(f"{h}*.tsv"):
                with open(p) as f:
                    reader = csv.reader(f, delimiter="\t")
                    dct = {k: v for k, v in reader if k != "id"}

            j = d.get("errors").get(h)
            for k in j:
                if k.endswith("_*"):
                    continue
                g = d.get("descriptions")
                l = g.get(k)
                m = k.replace("_%d", "_X")
                l = l.replace("%d", "{value}")
                dct[m] = l

            keys = sorted(dct)
            
            for p in Path("source/").glob(f"{h}*.tsv"):
                with open(p, "w") as f:
                    f.write("id\tmessage\n")
                    for i, item in enumerate(keys, start=1):
                        f.write(f"{item}\t{dct[item]}\n")
