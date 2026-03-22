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

import os
import subprocess
import sys
import inspect

sys.path.insert(0, os.path.abspath("../.."))

from pyrogram import __version__
from pyrogram.raw.all import layer

commit_id = subprocess.check_output([
    "git",
    "rev-parse",
    "--short",
    "HEAD",
]).decode("UTF-8").strip()

project_url = "https://github.com/TelegramPlayGround/Pyrogram"
project = "pyrotgfork"
copyright = "2017-present, Dan"
author = "Dan"
version = f"{__version__} Layer {layer}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    # "sphinx.ext.viewcode",
    "sphinx_copybutton",
    # "sphinx.ext.coverage",
    "sphinx.ext.linkcode",
    "sphinx_llms_txt",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None)
}

master_doc = "index"
source_suffix = ".rst"
autodoc_member_order = "bysource"

templates_path = ["../resources/templates"]
html_copy_source = False

napoleon_use_rtype = False
napoleon_use_param = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# Decides the language used for syntax highlighting of code blocks.
highlight_language = "python3"

copybutton_prompt_text = "$ "

suppress_warnings = ["image.not_readable"]

html_title = f"PyroTGFork {version}"
html_theme = "furo"
html_static_path = [os.path.abspath("static")]
print("ABSOLUTE PATH", os.path.abspath("static"))
html_css_files = [
    "css/all.min.css",
    "css/custom.css",
]
html_show_sourcelink = True
html_show_copyright = False
html_logo = html_static_path[0] + "/img/pyrogram.png"
html_favicon = html_static_path[0] + "/img/favicon.ico"
html_theme_options = {
    "navigation_with_keys": True,
    "footer_icons": [
        {  # Github logo
            "name": "GitHub",
            "url": f"https://github.com/TelegramPlayGround/pyrogram/tree/{commit_id}",
            "class": "fa-brands fa-solid fa-github fa-2x",
        },
        {
            # Telegram channel logo
            "name": "Telegram Channel",
            "url": "https://PyroTGFork.t.me/2",
            "class": "fa-brands fa-solid fa-telegram fa-2x",
        },
        {
            "name": "",
            "url": "https://pypi.org/project/pyrotgfork/",
            "class": "fa-brands fa-solid fa-python fa-2x",
        },
    ]
}
html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        # "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
    ]
}
latex_engine = "xelatex"
latex_logo = os.path.abspath("static/img/pyrogram.png")
print("latex_logo", latex_logo)

latex_elements = {
    "pointsize": "12pt",
    "fontpkg": r"""
        \setmainfont{Open Sans}
        \setsansfont{Bitter}
        \setmonofont{Ubuntu Mono}
        """
}

# Set canonical URL from the Read the Docs Domain
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")
if not html_baseurl:
    html_baseurl = "/pyrogram/"

# Tell Jinja2 templates the build is running on Read the Docs
if os.environ.get("READTHEDOCS", "") == "True":
    if "html_context" not in globals():
        html_context = {}
    html_context["READTHEDOCS"] = True

llms_txt_filename = "llms.txt"

# Disable full documentation file
llms_txt_full_file = False

# Provide a specific, agent-friendly summary of Pyrogram
llms_txt_summary = """Pyrogram is an elegant, modern, and asynchronous MTProto API framework for Telegram in Python for users and bots.
This documentation covers the Pyrogram Client High-Level API, the Smart Plugin system, and the raw Low-Level Telegram Functions Types.
We merge changes made to few of pyrogram forks plus changes made by us to this repository. All the features are just customized feature mostly for personal use; there is no guarantee in them being stable, USE AT YOUR OWN RISK.
"""

llms_txt_title = "PyroTGFork"

# Exclude pages that just consume tokens without providing value (like indexes or search pages)
llms_txt_exclude = [
    "search",
    "genindex",
    "modindex",
]

def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """
    if domain != "py":
        return None
    if not info["module"]:
        return None

    filename = info["module"].replace(".", "/")
    
    # Attempt to find the exact line numbers using the inspect module
    module = sys.modules.get(info["module"])
    if module is not None:
        obj = module
        for part in info["fullname"].split("."):
            obj = getattr(obj, part, None)
            
        if obj is not None:
            try:
                source, lineno = inspect.getsourcelines(obj)
                # Returns a link like: https://github.com/user/repo/blob/main/module.py#L10-L25
                return f"{project_url}/blob/{commit_id}/{filename}.py#L{lineno}-L{lineno + len(source) - 1}"
            except (TypeError, OSError):
                pass
    
    # Fallback to just linking to the file if line numbers can't be resolved
    return f"{project_url}/blob/{commit_id}/{filename}.py"
