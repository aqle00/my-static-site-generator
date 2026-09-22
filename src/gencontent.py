from markdown_blocks import markdown_to_html_node
# from htmlnode import HTMLNode
import os
import pathlib


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("Header h1 not found")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

# open files
    source_file = open(from_path, "r")
    source_file_markdown = source_file.read()
    source_file.close()

    template = open(template_path, "r")
    template_raw_text = template.read()
    template.close()

# get title and content
    html_node = markdown_to_html_node(source_file_markdown)
    content = html_node.to_html()
    title = extract_title(source_file_markdown)

# replace template text with source file text
    template_raw_text = template_raw_text.replace("{{ Title }}", title)
    template_raw_text = template_raw_text.replace("{{ Content }}", content)

# write
    directories = os.path.dirname(dest_path)
    if directories != "":
        os.makedirs(directories, exist_ok=True)
    dest_file = open(dest_path, "w")
    dest_file.write(template_raw_text)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    names = os.listdir(dir_path_content)

    for name in names:
        name_path = os.path.join(dir_path_content, name)
        new_dest_path = os.path.join(dest_dir_path, name)
        absolute_path = pathlib.Path(name_path)
        if not os.path.isfile(absolute_path):
            generate_pages_recursive(name_path, template_path, new_dest_path)
        else:
            generate_page(name_path, template_path, new_dest_path.replace(".md", ".html"))

    

