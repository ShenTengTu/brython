"""
Similar as `scripts/make_doc.py`
"""

import sys
import shutil
from . import path_project, insert_sys_path
from .conf import languages

# hack sys.path to be able to import version
insert_sys_path(str(path_project.joinpath("scripts")))
from version import implementation

impl_name = ".".join(str(x) for x in implementation[:3])

# restore original sys.path
del sys.path[0]

# hack sys.path to be able to import markdown
insert_sys_path(str(path_project.joinpath("www/src/Lib/browser")))
import markdown

# restore original sys.path
del sys.path[0]

# path of markdown files
md_doc_path = path_project.joinpath("L10n/www/doc")

static_doc_path = path_project.joinpath("L10n/www/static_doc")

md_tutorial_path = path_project.joinpath("L10n/www/tutorial")

static_tutorial_path = path_project.joinpath("L10n/www/static_tutorial")

src_paths = [static_doc_path, static_doc_path.joinpath("cookbook"), static_tutorial_path]

for path in src_paths:
    if not path.exists():
        path.mkdir()

# copy css
shutil.copy(
    md_doc_path.joinpath("doc_brython.css"), static_doc_path.joinpath("doc_brython.css")
)

# copy images
images_dir_src = md_doc_path.joinpath("images")
images_dir_dest = static_doc_path.joinpath("images")
if not images_dir_dest.exists():
    images_dir_dest.mkdir()

for img in images_dir_src.iterdir():

    shutil.copy(img, images_dir_dest)

with md_tutorial_path.joinpath("index.html").open(encoding="utf-8") as f:
    index_tutorial = f.read()

# documentation
for lang in languages:
    dest_path = static_doc_path.joinpath(lang)
    dest_paths = [dest_path, dest_path.joinpath("cookbook")]

    index = md_doc_path.joinpath(lang, "index_static.html").open("rb").read()
    index = index.decode("utf-8")

    for path in dest_paths:
        if not path.exists():
            path.mkdir()

    print("static doc %s" % lang)
    for i, (src_path, dest_path) in enumerate(
        zip(
            [md_doc_path.joinpath(lang), md_doc_path.joinpath(lang, "cookbook")], dest_paths
        )
    ):
        for file_path in src_path.iterdir():

            ext = file_path.suffix
            if ext == ".md":

                src = src_path.joinpath(file_path).open("rb").read()
                src = src.decode("utf-8")
                html, scripts = markdown.mark(src)
                out = dest_path.joinpath(file_path.stem + ".html").open("wb")
                html = index.replace("<content>", html)
                html = html.replace("<prefix>", "/".join([".."] * (i + 1)))
                if i == 1:
                    html = html.replace('class="navig" href="', 'class="navig" href="../')
                if scripts:
                    script_content = "\n".join(scripts)
                    html = html.replace("<scripts>", script_content)
                out.write(html.encode("utf-8"))
                out.close()
            elif ext == ".txt":
                shutil.copy(src_path.joinpath(file_path), dest_path.joinpath(file_path))
            elif src_path.joinpath(file_path).is_dir() and file_path.name != "cookbook":
                dest_dir = dest_path.joinpath(file_path)
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)
                shutil.copytree(src_path.joinpath(file_path), dest_dir)

# tutorial
for lang in languages:
    print(f"tutorial {lang}")
    md_path = md_tutorial_path.joinpath(lang)
    static_path = static_tutorial_path.joinpath(lang)
    if md_path.exists():
        if not static_path.exists():
            static_path.mkdir()
        for file_path in md_path.iterdir():
            print(md_path, file_path)
            basename = file_path.stem
            ext = file_path.suffix
            if ext == ".md":
                src_path = md_path.joinpath(file_path)
                with src_path.open(encoding="utf-8") as f:
                    src = f.read()
                    src = src.replace("{implementation}", impl_name)
                    html, scripts = markdown.mark(src)
                    dest_path = static_path.joinpath(basename + ".html")
                    print("save in", dest_path)
                    content = index_tutorial.replace("{{content}}", html)
                    with dest_path.open("w", encoding="utf-8") as out:
                        out.write(content)
