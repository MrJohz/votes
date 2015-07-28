import collections


class QuickEnum(object):
    """Quickly create a fairly simple enumeration object

    This collects multiple constants into one namespace, which is cleaner, but doesn't
    faff around creating a new enum, which isn't quite as self-documenting, but means
    I can just write it.  Quickly.
    """

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


def dewidow(string, force=False):
    string = string.replace("&nbsp;", " ")
    if len(string.split(' ')) > 3 or force:
        return "&nbsp;".join(string.rsplit(' ', 1))
    else:
        return string


def destr(strist):
    """Convert a thing that may be a string or a list into a list of strings"""
    if strist is None:
        return []
    elif isinstance(strist, str):
        return [strist]
    return [s for s in strist if s.strip()]
