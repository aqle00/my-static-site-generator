from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive
import shutil
import os

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main() -> None:
    print(f"deleting everything in {dir_path_public}")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_files_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
    )


main()