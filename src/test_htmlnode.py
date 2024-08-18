import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode
)
class TestHTMLNode(unittest.TestCase):

    def test_with_props(self) -> None:
        node = HTMLNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"})
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_output)
    
    def test_empty_props(self) -> None:
        node = HTMLNode(tag="p", props={})
        expected_output = ''
        self.assertEqual(node.props_to_html(), expected_output)
    
    def test_values(self) -> None:
        node = HTMLNode(tag="div", value="Hello world")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello world")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})
    
    def test_none_props(self) -> None:
        node = HTMLNode(tag="p", props=None)
        expected_output = ''
        self.assertEqual(node.props_to_html(), expected_output)
    
    def test_to_html_no_children(self) -> None:
        node = LeafNode("p", "Hello world")
        self.assertEqual(node.to_html(), "<p>Hello world</p>")
    
    def test_to_html_no_tag(self) -> None:
        node = LeafNode(None, "Hello world")
        self.assertEqual(node.to_html(), "Hello world")

    def test_repr(self) -> None:
        node = HTMLNode(tag="div", value="content", children=[], props={"id": "main"})
        expected_output = 'HTMLNode(div, content, 0, {\'id\': \'main\'})'
        self.assertEqual(repr(node), expected_output)
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")
    
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

if __name__ == "__main__":
    unittest.main()