import shutil
import os

def copy_files_recursive(source_dir_path: str, destination_dir_path: str) -> None:
    # this function can be replaced with a shutil.copytree like this:
        # shutil.copytree(source_dir_path, destination_dir_path)
    
    # but for training purposes, so this is a recursive  function

    # check destination_dir_path exists, if not make one with mkdir
    if not os.path.exists(destination_dir_path):
        os.mkdir(destination_dir_path)
    
    for name in os.listdir(source_dir_path):
        # if name is file, copy
        src_path = f"{source_dir_path}/{name}"
        dest_path = f"{destination_dir_path}/{name}"
        if os.path.isfile(src_path):
            print(f"copying from {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            # name not file-> is directory
            # recursively call this function, so that it makes new directory and copy its file recursively      
            copy_files_recursive(f"{source_dir_path}/{name}", f"{destination_dir_path}/{name}")
