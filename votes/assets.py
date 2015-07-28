from webassets.filter import Filter
from csscompressor import compress


class CSSCompressorFilter(Filter):
    name = 'compressor'

    def output(self, inp, out, **kw):
        out.write(compress(inp.read()))
