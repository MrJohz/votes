import mistune
from .utils import dewidow


class DewidowRenderer(mistune.Renderer):

    def block_quote(self, text):
        print(text)
        return super().block_quote(dewidow(text))

    def header(self, text, level, raw=None):
        return super().header(dewidow(text), level, raw)

    def list_item(self, text):
        return super().list_item(dewidow(text))

    def paragraph(self, text):
        return super().paragraph(dewidow(text))

    def table_cell(self, content, **flags):
        return super().table_cell(dewidow(content), **flags)
