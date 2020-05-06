# -*- coding: utf-8 -*-
# Generate list of modules in the standard distribution

"""
Similar as `scripts/make_stdlib_list.py`
"""
import sys
import os
import pathlib
from . import path_project, insert_sys_path
from .conf import languages, dict_stdlib_list

# hack sys.path to be able to import git
insert_sys_path(str(path_project.joinpath("scripts")))
import git

if sys.version_info[0] != 3:
    raise ValueError("This script must be run with Python 3")

version = "%s.%s" % sys.version_info[:2]

brython_stdlib_folder = path_project.joinpath("www/src")
python_stdlib_folder = pathlib.Path(sys.executable).parent
print(python_stdlib_folder)
doc_folder = path_project.joinpath("L10n/www/doc")
static_doc_folder = path_project.joinpath("L10n/www/static_doc")

if not static_doc_folder.exists():
    import mk_doc

for lang in languages:

    index = (
        doc_folder.joinpath(lang, "index_static.html").open("r", encoding="utf-8").read()
    )

    with static_doc_folder.joinpath(lang, "stdlib.html").open("w", encoding="utf-8") as out:

        html = "<h1>%s %s" '</h1>\n<div style="padding-left:30px;">' % (
            dict_stdlib_list["title"][lang],
            version,
        )
        html += "\n<div>%s</div>" % dict_stdlib_list["diff"][lang]
        html += "<table border=1>\n"
        html += (
            "<tr>\n<th>%s</th>\n"
            "<th>%s</th>\n"
            "<th>%s</th>\n"
            "<th>%s</th></tr>\n"
            % (
                dict_stdlib_list["dir"][lang],
                dict_stdlib_list["both"][lang],
                dict_stdlib_list["specific"][lang],
                dict_stdlib_list["not_yet"][lang],
            )
        )
        for dirpath, dirnames, filenames in os.walk(brython_stdlib_folder):

            if "dist" in dirnames:
                dirnames.remove("dist")
            if ".hg" in dirnames:
                dirnames.remove(".hg")
            if ".git" in dirnames:
                dirnames.remove(".git")
            for dirname in dirnames:
                if dirname == "dist":
                    continue
                if dirname == "__pycache__":
                    continue

            if "site-packages" in dirpath:
                continue

            path = dirpath[len(str(brython_stdlib_folder)) + 1 :]
            python_path = python_stdlib_folder.joinpath(path)

            if path.startswith("Lib\\test"):
                continue

            if not git.in_index(path.replace("\\", "/")):
                continue

            if path:
                valid = [f for f in filenames if os.path.splitext(f)[1] not in [".pyc"]]
                valid = [
                    v
                    for v in valid
                    if git.in_index(os.path.join(path, v).replace("\\", "/"))
                ]
                valid = [v for v in valid if v.startswith("_")] + [
                    v for v in valid if not v.startswith("_")
                ]

                if valid:
                    common = [v for v in valid if python_path.joinpath(v).exists()]
                    for i, f in enumerate(common):
                        if (
                            os.stat(os.path.join(dirpath, f)).st_size
                            != python_path.joinpath(f).stat().st_size
                        ):
                            common[i] = "*" + common[i]
                    brython_specific = [v for v in valid if not v in common]
                    if python_path.exists():
                        missing = [
                            f
                            for f in os.listdir(python_path)
                            if f != "__pycache__"
                            and python_path.joinpath(f).is_file()
                            and not f in valid
                        ]
                    else:
                        missing = []
                    html += '<tr><td valign="top">%s</td>\n' % path
                    for files in common, brython_specific, missing:
                        html += (
                            '<td style="vertical-align:top;">'
                            + "\n<br>".join(files)
                            + "</td>\n"
                        )
                    html += "</tr>\n"

        html += "</table>\n"

        # Directories in CPython dist missing from Brython dist
        html += "<h2>%s</h2>" % dict_stdlib_list["missing"][lang]
        for dirpath, dirnames, filenames in os.walk(python_stdlib_folder):
            path = dirpath[len(str(python_stdlib_folder)) + 1 :]
            if path.startswith(r"Lib\site-packages"):
                continue
            if path.endswith(r"\__pycache__"):
                continue
            brython_path = brython_stdlib_folder.joinpath(path)
            if not brython_path.exists():
                html += "<li>%s\n" % path
                dirnames.clear()  # no recursion

        html += "</div>\n</body>\n</html>"

        html = index.replace("<content>", html)
        html = html.replace("<prefix>", "..")

        out.write(html)
