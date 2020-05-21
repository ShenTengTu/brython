import pathlib
from . import path_project, copy_tree


src_path = path_project.joinpath("www/src")
dest_path = path_project.joinpath("L10n/www/src")


def ignore_function(root, dirs, files):
    ignore_list = []
    path_root = pathlib.Path(root)

    if path_root.match("www/src/Lib"):
        for d in dirs:
            if d in ["browser"]:
                continue
            ignore_list.append(path_root.joinpath(d))
        ignore_list.extend([path_root.joinpath(f) for f in files])

    if path_root.match("www/src/Lib/browser"):
        for d in dirs:
            if d in ["widgets"]:
                continue
            ignore_list.append(path_root.joinpath(d))
        for f in files:
            if f in ["highlight.py"]:
                continue
            ignore_list.append(path_root.joinpath(f))

    if path_root.match("www/src/libs"):
        for d in dirs:
            ignore_list.append(path_root.joinpath(d))
        for f in files:
            if f in ["_jsre.js"]:
                continue
            ignore_list.append(path_root.joinpath(f))

    return ignore_list


copy_tree(src_path, dest_path, ignore_function)
