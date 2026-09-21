import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
	# 0
	def test_all_params_have_value(self):
		child = HTMLNode(tag="span", value="child")
		node = HTMLNode(
			tag="div",
			value="content",
			children=[child],
			props={"class": "container"},
		)

		self.assertEqual(node.tag, "div")
		self.assertEqual(node.value, "content")
		self.assertEqual(node.children, [child])
		self.assertEqual(node.props, {"class": "container"})

	# 1
	def test_missing_tag(self):
		node = HTMLNode(value="content")

		self.assertIsNone(node.tag)

	# 2
	def test_missing_value(self):
		node = HTMLNode(tag="div", children=[])

		self.assertIsNone(node.value)

	# 3
	def test_missing_children(self):
		node = HTMLNode(tag="div", value="content")

		self.assertIsNone(node.children)

	# 4
	def test_missing_props(self):
		node = HTMLNode(tag="div", value="content")

		self.assertIsNone(node.props)

	# def test_value_and_children_are_mutually_exclusive(self):
	# 	value_node = HTMLNode(tag="div", value="content")
	# 	children_node = HTMLNode(
	# 		tag="div",
	# 		children=[HTMLNode(tag="span", value="child")],
	# 	)

	# 	self.assertIsNotNone(value_node.value)
	# 	self.assertEqual(value_node.children, [])
	# 	self.assertIsNone(children_node.value)
	# 	self.assertEqual(len(children_node.children), 1)

	# 5
	def test_props_to_html_with_none_props(self):
		node = HTMLNode(tag="div", value="content", props=None)

		self.assertEqual(node.props_to_html(), "")

	# 6
	def test_props_to_html_with_empty_props(self):
		node = HTMLNode(tag="div", value="content", props={})

		self.assertEqual(node.props_to_html(), "")

	# 7
	def test_props_to_html_with_props(self):
		node = HTMLNode(
			tag="div",
			value="content",
			props={"class": "container", "id": "main"},
		)

		self.assertEqual(
			node.props_to_html(),
			' class="container" id="main"',
		)

	# 8
	def test_repr(self):
		child = HTMLNode(tag="span", value="child")
		node = HTMLNode(
			tag="div",
			value="content",
			children=[child],
			props={"class": "container"},
		)

		self.assertEqual(
			repr(node),
			"HTMLNode(div, content, [HTMLNode(span, child, None, None)], "
			"{'class': 'container'})",
		)

	# 9
	def test_leaf_node_renders_with_tag(self):
		node = LeafNode("p", "Hello, world!")

		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
		self.assertIsNone(node.children)

	# 10
	def test_leaf_node_renders_props(self):
		node = LeafNode("a", "Boot.dev", {"href": "https://www.boot.dev"})

		self.assertEqual(
			node.to_html(),
			'<a href="https://www.boot.dev">Boot.dev</a>',
		)

	# 11
	def test_leaf_node_without_tag_returns_value(self):
		node = LeafNode(value="plain text")

		self.assertEqual(node.to_html(), "plain text")

	# 12
	def test_leaf_node_without_value_raises_error(self):
		node = LeafNode("p")

		with self.assertRaisesRegex(ValueError, "Invalid LeadNode: value cannot be None"):
			node.to_html()

	# 13
	def test_parent_node_renders_children(self):
		node = ParentNode(
			"div",
			[
				LeafNode("p", "Hello"),
				LeafNode("p", "World"),
			],
		)

		self.assertEqual(
			node.to_html(),
			"<div><p>Hello</p><p>World</p></div>",
		)

	# 14
	def test_parent_node_renders_nested_children(self):
		node = ParentNode(
			"div",
			[ParentNode("section", [LeafNode("p", "Nested")])],
		)

		self.assertEqual(
			node.to_html(),
			"<div><section><p>Nested</p></section></div>",
		)

	# 15
	def test_parent_node_renders_props(self):
		node = ParentNode(
			"div",
			[LeafNode(value="Content")],
			{"class": "container"},
		)

		self.assertEqual(
			node.to_html(),
			"<div>Content</div>",
		)

	# 16
	def test_parent_node_without_tag_raises_error(self):
		node = ParentNode(children=[LeafNode(value="Content")])

		with self.assertRaisesRegex(ValueError, "tag cannot be None"):
			node.to_html()

	# 17
	def test_parent_node_without_children_raises_error(self):
		node = ParentNode("div")

		with self.assertRaisesRegex(ValueError, "children cannot be None"):
			node.to_html()

	# 18
	def test_parent_node_with_empty_children_raises_error(self):
		node = ParentNode("div", [])

		with self.assertRaisesRegex(ValueError, "children cannot be None"):
			node.to_html()

	# 19
	def test_parent_node_repr(self):
		child = LeafNode("p", "Content")
		node = ParentNode("div", [child], {"class": "container"})

		self.assertEqual(
			repr(node),
			"ParentNode(div, children: [HTMLNode(p, Content, None, None)], "
			"{'class': 'container'})",
		)


if __name__ == "__main__":
	unittest.main()
