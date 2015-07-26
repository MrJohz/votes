import collections
import yaml


class QuickEnum(object):
    """Quickly create a fairly simple enumeration object

    This collects multiple constants into one namespace, which is cleaner, but doesn't
    faff around creating a new enum, which isn't quite as self-documenting, but means
    I can just write it.  Quickly.
    """

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


def ordered_load(fn, Loader=yaml.Loader, mapper=collections.OrderedDict):
    with open(fn) as stream:
        class OrderedLoader(Loader):
            pass
        def construct_mapping(loader, node):
            loader.flatten_mapping(node)
            return mapper(loader.construct_pairs(node))
        OrderedLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            construct_mapping)
        return yaml.load(stream, OrderedLoader)


def dewidow(string, force=False):
    if len(string.split(' ')) > 3 or force:
        return "&nbsp;".join(string.rsplit(' ', 1))
    else:
        return string


def double_paragraphs(string):
    return string.replace('\n', '\n\n')
