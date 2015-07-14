from collections import OrderedDict
import yaml


class QuickEnum(object):
    """Quickly create a fairly simple enumeration object

    This collects multiple constants into one namespace, which is cleaner, but doesn't
    faff around creating a new enum, which isn't quite as self-documenting, but means
    I can just write it.  Quickly.
    """

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, val)


def ordered_load(filename, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    with open(filename) as stream:
        class OrderedLoader(Loader):
            pass
        def construct_mapping(loader, node):
            loader.flatten_mapping(node)
            return object_pairs_hook(loader.construct_pairs(node))
        OrderedLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            construct_mapping)
        return yaml.load(stream, OrderedLoader)
