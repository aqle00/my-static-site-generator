from __future__ import annotations


class HTMLNode:
    def __init__(
            self, 
            tag: str | None = None,
            value: str | None = None,
            children: list[HTMLNode] | None = None,
            props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props 

    def to_html(self) -> str:
        raise NotImplementedError("Not implementd")

    def props_to_html(self) -> str:
        if not self.props or len(self.props) == 0:
            return ""
        html = ""
        for k in self.props:
            html += f' {k}="{self.props[k]}"'
        return html

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None = None, value: str | None = None, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("Invalid LeadNode: value cannot be None")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str | None = None, children: list[HTMLNode] | None = None, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Invalid ParentNode: tag cannot be None")
        if not self.children:
            raise ValueError("Invalid ParentNode: children cannot be None")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}>{children_html}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"