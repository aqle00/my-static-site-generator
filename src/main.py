from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive
import shutil
import os
import sys

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main() -> None:
    base_path = "/"
    if sys.argv[1]:
        base_path = sys.argv[1]

    print(f"deleting everything in {dir_path_docs}")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    copy_files_recursive(dir_path_static, dir_path_docs)
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_docs,
        base_path
    )


main()