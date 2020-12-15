import pathlib
from . import path_project, copy_tree


src_path = path_project.joinpath("www")
dest_path = path_project.joinpath("L10n/www")


def ignore_function(root, dirs, files):
    ignore_list = []
    path_root = pathlib.Path(root)
    match_dirs = [
        "www'assets",
        "www/benchmarks",
        "www/code_coverage",
        "www/doc",  # need manual copy
        "www/font",
        "www/gallery",
        "www/slideshow",
        "www/speed",
        "www/src",
        "www/tests",
    ]
    for d in dirs:
        path_d = path_root.joinpath(d)
        for m in match_dirs:
            if path_d.match(m):
                ignore_list.append(path_d)
    for f in files:
        path_f = path_root.joinpath(f)
        if path_f.suffix != ".html":
            ignore_list.append(path_f)
    return ignore_list


copy_tree(src_path, dest_path, ignore_function)
