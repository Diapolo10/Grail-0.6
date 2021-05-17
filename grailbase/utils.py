"""Several useful routines that isolate some of the weirdness of Grail-based
applications.
"""
__version__ = '$Revision: 1.3 $'

import os
import string
import sys
from pathlib import Path

# TBD: hack!  grail.py calculates grail_root, which would be
# convenient to export to extensions, but you can't `import grail' or
# `import __main__'.  grail.py isn't designed for that.  You could
# `from grail import grail_root' but that's kind of gross.  This
# global holds the value of grail_root which can be had with
# grailutil.get_grailroot()
_grail_root = None
_grail_app = None


# XXX Unix specific stuff
# XXX (Actually it limps along just fine for Macintosh, too)

def getgraildir():
    return os.environ.get("GRAILDIR") or str(Path.home() / ".grail")


def get_grailroot():
    return _grail_root


def get_grailapp():
    return _grail_app

def getenv(key): # TODO: Remove when all instances removed as deprecated
    return os.environ.get(key)

def gethome(): # TODO: Remove when all instances removed as deprecated
    return str(Path.home())


def which(filename, searchlist=None):
    if searchlist is None:
        searchlist = sys.path

    for dir in searchlist:
        found = Path(dir) / filename
        if found.exists():
            return str(found)
    return None


def establish_dir(dir):
    """Ensure existence of DIR, creating it if necessary.

    Returns 1 if successful, 0 otherwise."""
    if os.path.isdir(dir):
        return 1
    head, tail = os.path.split(dir)
    if not establish_dir(head):
        return 0
    try:
        os.mkdir(dir, 0o777)
        return 1
    except os.error:
        return 0


def conv_mimetype(type):
    """Convert MIME media type specifications to tuples of
    ('type/subtype', {'option': 'value'}).
    """
    if not type:
        return None, {}
    if ';' in type:
        i = string.index(type, ';')
        opts = _parse_mimetypeoptions(type[i + 1:])
        type = type[:i]
    else:
        opts = {}
    fields = string.split(string.lower(type), '/')
    if len(fields) != 2:
        raise ValueError, "Illegal media type specification."
    type = string.join(fields, '/')
    return type, opts


def _parse_mimetypeoptions(options):
    opts = {}
    options = string.strip(options)
    while options:
        if '=' in options:
            pos = string.find(options, '=')
            name = string.lower(string.strip(options[:pos]))
            value = string.strip(options[pos + 1:])
            options = ''
            if ';' in value:
                pos = string.find(value, ';')
                options = string.strip(value[pos + 1:])
                value = string.strip(value[:pos])
            if name:
                opts[name] = value
        else:
            options = None
    return opts
