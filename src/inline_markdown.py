from textnode import (
    TextNode,
    text_type_bold,
    text_type_text,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)

import re

def text_to_textnodes(text) -> TextNode:
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, new_text_type) -> list:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        parts = old_node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], text_type_text))
            else:
                new_nodes.append(TextNode(parts[i], new_text_type))

    return new_nodes

def extract_markdown_images(text) -> list:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)        
    return [(alt_text, url) for alt_text, url in matches]

def extract_markdown_links(text) -> list:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)        
    return [(anchor_text, url) for anchor_text, url in matches]

def split_nodes_image(old_nodes) -> list:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        text_content = old_node.text
        images = extract_markdown_images(text_content)

        for image in images:        
            alt_text, url = image
        
            parts = text_content.split(f'![{alt_text}]({url})', 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], text_type_text))        
            new_nodes.append(TextNode(alt_text, text_type_image, url))
            text_content = parts[1] if len(parts) > 1 else ""
        
        if text_content:
            new_nodes.append(TextNode(text_content, text_type_text))
    

    return new_nodes

def split_nodes_link(old_nodes) -> list:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        text_content = old_node.text
        images = extract_markdown_links(text_content)

        for image in images:        
            anchor_text, url = image
        
            parts = text_content.split(f'[{anchor_text}]({url})', 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], text_type_text))        
            new_nodes.append(TextNode(anchor_text, text_type_link, url))
            
            text_content = parts[1] if len(parts) > 1 else ""
        
        if text_content:
            new_nodes.append(TextNode(text_content, text_type_text))
    

    return new_nodes


if __name__ == "__main__":
    main()