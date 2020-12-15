import sys
import os
import pathlib
import shutil


path_project = pathlib.Path(__file__).parent.parent.parent


def insert_sys_path(path):
    """
    Dynamic load module path
    """
    sys.path.insert(0, path)


def copy_file(src: pathlib.Path, dest: pathlib.Path):
    if not dest.parent.exists():
        dest.parent.mkdir(parents=True)
    shutil.copyfile(src, dest)
    print(src, "\n  >>", dest)


def copy_tree(src_dir: pathlib.Path, dest_dir: pathlib.Path, ignore_function=None):
    ignore_dirs = []
    ignore_files = []
    for root, dirs, files in os.walk(src_dir):
        if callable(ignore_function):
            for ignore in ignore_function(root, dirs, files):
                p = pathlib.Path(ignore)
                if p.is_dir():
                    ignore_dirs.append(str(p))
                if p.is_file():
                    ignore_files.append(str(p))

        if True in [root.startswith(d) for d in ignore_dirs]:
            continue

        path_root = pathlib.Path(root)
        for f in files:
            p = path_root.joinpath(f)
            if str(p) in ignore_files:
                continue

            copy_file(p, dest_dir.joinpath(p.relative_to(src_dir)))
