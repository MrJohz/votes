from webassets.filter import Filter, register_filter

from csscompressor import compress

class CSSCompressorFilter(Filter):
    name = 'compressor'

    def output(self, inp, out, **kw):
        out.write(compress(inp.read()))

register_filter(CSSCompressorFilter)
