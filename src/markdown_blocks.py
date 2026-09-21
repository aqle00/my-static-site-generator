from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")
    blocks: list[str] = []
    for block in raw_blocks:
        # have to strip first because whitespaces and \n still count for len and will mess up the check
        cleaned = block.strip()
        if len(cleaned) == 0:
            continue
        blocks.append(cleaned)
    return blocks

def block_to_block_type(block: str) -> BlockType:
    lines: list[str] = block.split('\n')
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i+1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes: list[HTMLNode] = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes

def paragraph_to_html_node(block: str) -> ParentNode:
    block = block.replace("\n", " ")
    children = text_to_children(block)
    return ParentNode("p", children)

def heading_to_html_node(block: str) -> ParentNode:
    parts = block.split(" ", 1)
    level = len(parts[0])
    if level > 6:
        raise ValueError(f"Invalid markdown: heading level {level} ")
    children = text_to_children(parts[1])
    return ParentNode(f"h{level}", children)
            
def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid markdown: code block must be correctly wrapped with ```")
    code_block = block[4:-3]
    text_node = TextNode(code_block, TextType.TEXT)
    children: list[HTMLNode] = [ParentNode("code", [text_node_to_html_node(text_node)])]
    return ParentNode("pre", children)

def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    cleaned_lines: list[str] = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid markdown: quote block must start with >")
        cleaned_lines.append(line.lstrip(">").strip())
    children = text_to_children((" ".join(cleaned_lines)))
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    big_list_children: list[HTMLNode] = []
    for line in lines:
        if not line.startswith("- "):
            raise ValueError("Invalid markdown: unordered list must start with - ")
        children = text_to_children(line[2:])
        big_list_children.append(ParentNode("li", children))
    return ParentNode("ul", big_list_children)

def ordered_list_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    big_list_children: list[HTMLNode] = []
    for line in lines:
        parts = line.split(". ", 1)
        children = text_to_children(parts[1])
        big_list_children.append(ParentNode("li", children))
    return ParentNode("ol", big_list_children)

def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    raise ValueError("Invalid block type")

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)
