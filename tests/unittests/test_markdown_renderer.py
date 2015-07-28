from votes import markdown_renderer

import mistune
import pytest


class TestDewidowRenderer:

    @pytest.fixture
    def markdown(self):
        return mistune.Markdown()

    @pytest.fixture
    def dewidow_markdown(self):
        return mistune.Markdown(renderer=markdown_renderer.DewidowRenderer())

    def test_block_quote(self, markdown, dewidow_markdown):
        inp = "> Hello! Short!"
        out = "> Hello! Short!"
        assert dewidow_markdown(inp) == markdown(out)

        inp = "> Hello goodbye longer text here"
        out = "> Hello goodbye longer text&nbsp;here"
        assert dewidow_markdown(inp) == markdown(out)

    def test_header(self, markdown, dewidow_markdown):
        inp = "# Header text"
        out = "# Header text"
        assert dewidow_markdown(inp) == markdown(out)

        inp = "# Long header text needs dewidowing"
        out = "# Long header text needs&nbsp;dewidowing"
        assert dewidow_markdown(inp) == markdown(out)

    def test_list_item(self, markdown, dewidow_markdown):
        inp = "- li one\n- li two"
        out = "- li one\n- li two"
        assert dewidow_markdown(inp) == markdown(out)

        inp = "- li one long line\n- li two more long lines"
        out = "- li one long&nbsp;line\n- li two more long&nbsp;lines"
        assert dewidow_markdown(inp) == markdown(out)

    def test_paragraph(self, markdown, dewidow_markdown):
        inp = "short body"
        out = "short body"
        assert dewidow_markdown(inp) == markdown(out)

        inp = "much longer body goes here"
        out = "much longer body goes&nbsp;here"
        assert dewidow_markdown(inp) == markdown(out)
