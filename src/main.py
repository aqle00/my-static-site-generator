from textnode import TextNode, TextType

def main() -> None:
    new = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(new.__repr__())

main()