import pathlib
from . import path_project, copy_tree


src_path = path_project.joinpath("www/src")
dest_path = path_project.joinpath("L10n/www/src")


def ignore_function(root, dirs, files):
    ignore_list = []
    path_root = pathlib.Path(root)
    for d in dirs:
        path_d = path_root.joinpath(d)
        if path_d.match("www/src/Lib"):
            ignore_list.append(path_d)
        if path_d.match("www/src/libs"):
            ignore_list.append(path_d)
    return ignore_list


copy_tree(src_path, dest_path, ignore_function)
