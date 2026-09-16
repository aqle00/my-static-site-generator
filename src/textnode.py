from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node: object) -> bool:
        if not isinstance(node, TextNode):
            return False
        return self.text == node.text and self.text_type == node.text_type and self.url == node.url 

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    