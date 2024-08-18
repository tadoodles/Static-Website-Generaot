import unittest

from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
    text_node_to_html_node,
)

class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_eq_url(self) -> None:
        node = TextNode("This is a text node", text_type_bold, None)
        node2 = TextNode("This is a text node", text_type_bold, None)
        self.assertEqual(node, node2)
    
    def test_not_eq_different_text_type(self) -> None:
        node = TextNode("This is a text node", text_type_italic)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_different_text(self) -> None:
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This are text nodes", text_type_bold)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_different_url(self) -> None:
        node = TextNode("This is a text node", text_type_bold, None)
        node2 = TextNode("This is a text node", text_type_bold, "github.com")
        self.assertNotEqual(node, node2)
    
    def test__repr(self) -> str:
        node = TextNode("This is a text node", text_type_bold, "https://github.com")
        self.assertEqual("TextNode(This is a text node, bold, https://github.com)", repr(node))
    
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self) -> None:
        node = TextNode("Hello world", text_type_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello world")
    
    def test_image(self) -> None:
        node = TextNode("Image", text_type_image, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {"src": "https://google.com", "alt": "Image"})
    
    def test_link(self) -> None:
        node = TextNode("Link", text_type_link, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, 'Link')
        self.assertEqual(html_node.props, {"href": "https://google.com"})

if __name__ == "__main__":
    unittest.main()
