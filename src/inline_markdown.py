from textnode import TextNode, TextType
# from htmlnode import HTMLNode
import re

def split_nodes_delimiter(
        old_nodes: list[TextNode],
        delimiter: str,
        text_type: TextType
        ) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    # loop through old nodes
    for node in old_nodes:
        # if not TextType.TEXT -> add to list as is, continue to next
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # if is TextType.TEXT -> check for delimiter pair, if missing then exception
        # if markdown is valid, there should be 1 opening delimiter and 1 closing like so:
        # ** something ** or __ something __
        # so valid markdown will always split into odd number( 1 3 5 7)
        # if after split the list has even length the markdown is invalid
        splitted_text = node.text.split(delimiter)
        if len(splitted_text) % 2 == 0:
            raise Exception(f"Invalid markdown: missing delimiter {delimiter}, need 2 delimiter, only got 1")

        # reaches here markdown is valid
        #loop through the splitted_text_list
        # convert each string into a node
        # after splitting, the texts that are inside delimiters will always be in odd positions( 1 3 5 7)
        # while normal text will be even (0 2 4 6)
        splitted_nodes: list[TextNode] = []
        for i in range(len(splitted_text)):
            if splitted_text[i] == "":
                continue
            if i % 2 == 0:
                splitted_nodes.append(TextNode(splitted_text[i], TextType.TEXT))
            else:
                splitted_nodes.append(TextNode(splitted_text[i], text_type))
        new_nodes.extend(splitted_nodes)
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    # image version of split_nodes_delimiter
    
    # steps:
    # 1. make new_nodes to hold all the nodes we get after everything
    # 2. loop through each node in old_nodes
        # check 1: text_type != TextType.TEXT -> dont need to handle, just append
        # extract images from node to use for splitting later
        # check 2: if after extract len == 0 means its textnode -> append

        #3. start inner loop, loop through all images
            
                        # example: "raw1 ![alt1](img1) raw2 ![alt2](img2) raw3" 
                        # need to handle 5 parts, [raw1, img1, raw2, img2, raw3]

            # split original text based on the extracted image, maxsplit=1 to only handle [0], [1] will be handled later
            # after split: [raw1, ...raw2+ the rest] -> img1 gone cuz its the thing we use to split

            # check 1: len [] != 2 means its wrong markdown -> error
            # check 2: if [0] != "" -> not empty, raw1 text detected, append
            # after checks, append img1( not in the list cuz we used as deliminator)
        
        # 4. this step outside of inner loop:
        # after inner loop finishes, handle the last part of the raw text, check if empty and append if needed 
    
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # for use later without mutating node.text
        original_node_text = node.text
        # after extracting, extracted_images is a list of textnode
        extracted_images = extract_markdown_images(original_node_text)
        # if no image -> append whole thing cuz its just normal textnode
        if len(extracted_images) == 0:
            new_nodes.append(node)
            continue

        #inner loop start
        for image in extracted_images:
            # this should always split the original node's text into 2 part, [0] and [1], length = 2 always
            splitted_text = original_node_text.split(f"![{image[0]}]({image[1]})", 1)
            # length!=2 means markdown error 
            if len(splitted_text) != 2:
                raise ValueError("Invalid markdown: image markdown invalid, check if markdown is correct")
            # raw1 not empty -> append raw1
            if splitted_text[0] != "":
                new_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            # append img1
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            # assign ...raw2+everything else to handle next since raw1 and img1 is done
            original_node_text = splitted_text[1]
        # after all inner loop runs, we have 1 last part of the text left, check and append if needed
        if original_node_text != "":
            new_nodes.append(TextNode(original_node_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    # mostly the same as split_nodes_images, but with a few changes due to markdown syntax difference and variable names diff
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_node_text = node.text
        extracted_links = extract_markdown_links(original_node_text)
        if len(extracted_links) == 0:
            new_nodes.append(node)
            continue
        for link in extracted_links:
            splitted_text = original_node_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(splitted_text) != 2:
                raise ValueError("Invalid markdown: link markdown invalid, check if markdown is correct")
            if splitted_text[0] != "":
                new_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_node_text = splitted_text[1]
        if original_node_text != "":
            new_nodes.append(TextNode(original_node_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes