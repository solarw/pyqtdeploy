# Copyright (c) 2014, Riverbank Computing Limited
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


class BaseMetadata:
    """ Encapsulate the meta-data common to all types of module. """

    def __init__(self, min_version=None, version=None, max_version=None, internal=False, ssl=None, windows=None, deps=(), core=False, defines='', libs=''):
        """ Initialise the object. """

        # A meta-datum is uniquely identified by a range of version numbers.  A
        # version number is a 2-tuple of major and minor version number.  It is
        # an error if version numbers for a particular module overlaps.
        if version is not None:
            if isinstance(version, tuple):
                self.min_version = self.max_version = version
            else:
                # A single digit is interpreted as a range.
                self.min_version = (version, 0)
                self.max_version = (version, 99)
        else:
            if min_version is not None:
                self.min_version = min_version
            else:
                self.min_version = (2, 0)

            if max_version is not None:
                self.max_version = max_version
            else:
                self.max_version = (3, 99)

        # Set if the module is internal.
        self.internal = internal

        # True if the module is required if SSL is enabled, False if it is
        # required if SSL is disabled and None if SSL is not relevant.
        self.ssl = ssl

        # True if the module is Windows-specific, False if non-Windows and None
        # if present on all platforms.
        self.windows = windows

        # The sequence of modules that this one is dependent on.
        self.deps = (deps, ) if isinstance(deps, str) else deps

        # Set if the module is always compiled in to the interpreter library
        # (if it is an extension module) or if it is required (if it is a
        # Python module).
        self.core = core

        # The DEFINES to add to the .pro file.
        self.defines = defines

        # The LIBS to add to the .pro file.
        self.libs = libs


class ExtensionModule(BaseMetadata):
    """ Encapsulate the meta-data for a single extension module. """

    def __init__(self, source, subdir='', min_version=None, version=None, max_version=None, internal=None, ssl=None, windows=None, deps=(), core=False, defines='', libs=''):
        """ Initialise the object. """

        super().__init__(min_version=min_version, version=version,
                max_version=max_version, internal=internal, ssl=ssl,
                windows=windows, deps=deps, core=core, defines=defines,
                libs=libs)

        # The sequence of source files relative to the Modules directory.
        self.source = (source, ) if isinstance(source, str) else source

        # A sub-directory of the Modules directory to add to INCLUDEPATH.
        self.subdir = subdir


class CoreExtensionModule(ExtensionModule):
    """ Encapsulate the meta-data for an extension module that is always
    compiled in to the interpreter library.
    """

    def __init__(self, min_version=None, version=None, max_version=None, internal=None, ssl=None, windows=None, deps=()):
        """ Initialise the object. """

        super().__init__(source=(), min_version=min_version, version=version,
                max_version=max_version, internal=internal, ssl=ssl,
                windows=windows, deps=deps, core=True)


class PythonModule(BaseMetadata):
    """ Encapsulate the meta-data for a single Python module. """

    def __init__(self, min_version=None, version=None, max_version=None, internal=None, ssl=None, windows=None, deps=(), core=False, modules=None):
        """ Initialise the object. """

        super().__init__(min_version=min_version, version=version,
                max_version=max_version, internal=internal, ssl=ssl,
                windows=windows, deps=deps, core=core)

        # The sequence of modules or sub-packages if this is a package,
        # otherwise None.
        self.modules = (modules, ) if isinstance(modules, str) else modules


class CorePythonModule(PythonModule):
    """ Encapsulate the meta-data for a Python module that is always required
    an application.
    """

    def __init__(self, min_version=None, version=None, max_version=None, internal=None, ssl=None, windows=None, deps=(), modules=None):
        """ Initialise the object. """

        super().__init__(min_version=min_version, version=version,
                max_version=max_version, internal=internal, ssl=ssl,
                windows=windows, deps=deps, core=True, modules=modules)


# The meta-data for each module.
_metadata = {
    # These are the public modules.
    '__future__':       PythonModule(),
    '_thread':          CoreExtensionModule(version=3),

    'abc': (            PythonModule(version=(2, 6)),
                        PythonModule(version=(2, 7),
                                deps=('types', '_weakrefset')),
                        PythonModule(version=3,
                                deps='_weakrefset')),
    'aifc': (           PythonModule(version=2,
                                deps=('audioop', 'chunk', 'cl', 'math',
                                        'struct')),
                        PythonModule(version=(3, 3),
                                deps=('audioop', 'chunk', 'math', 'struct',
                                        'warnings')),
                        PythonModule(min_version=(3, 4),
                                deps=('audioop', 'chunk', 'collections',
                                        'math', 'struct', 'warnings'))),
    'argparse': (       PythonModule(version=(2, 7),
                                deps=('collections', 'copy', 'gettext', 'os',
                                        're', 'textwrap', 'warnings')),
                        PythonModule(min_version=(3, 3),
                                deps=('collections', 'copy', 'gettext', 'os',
                                        're', 'textwrap'))),
    'array':            ExtensionModule(source='arraymodule.c'),
    'atexit': (         CorePythonModule(version=2,
                                deps='traceback'),
                        ExtensionModule(version=(3, 3),
                                source='atexitmodule.c'),
                        CoreExtensionModule(min_version=(3, 4))),
    'audioop':          ExtensionModule(source='audioop.c'),

    'base64': (         PythonModule(version=2,
                                deps=('binascii', 're', 'struct')),
                        PythonModule(version=3,
                                deps=('binascii', 're', 'struct',
                                        'warnings'))),
    'binascii':         ExtensionModule(source='binascii.c',
                                defines='USE_ZLIB_CRC32', libs='-lz'),
    'bisect':           PythonModule(deps='_bisect'),
    'bz2': (            ExtensionModule(version=2,
                                source='bz2module.c', libs='-lbz2'),
                        PythonModule(version=3,
                                deps=('_thread', '_bz2', 'io', 'warnings'))),

    'calendar':         PythonModule(deps=('datetime', 'locale')),
    'chunk':            PythonModule(deps='struct'),
    'cmath': (          ExtensionModule(version=(2, 6),
                                source='cmathmodule.c', libs='-lm'),
                        ExtensionModule(version=(2, 7),
                                source=['cmathmodule.c', '_math.c'],
                                libs='-lm'),
                        ExtensionModule(version=3,
                                source=['cmathmodule.c', '_math.c'],
                                libs='-lm')),
    'codecs':           PythonModule(deps='_codecs'),
    'collections': (    PythonModule(version=(2, 6),
                                deps=('_abcoll', '_collections', 'keyword',
                                        'operator')),
                        PythonModule(version=(2, 7),
                                deps=('_abcoll', '_collections', 'heapq',
                                        'itertools', 'keyword', 'operator',
                                        'thread')),
                        PythonModule(version=(3, 3),
                                deps=('collections.abc', '_collections',
                                        'copy', 'heapq', 'itertools',
                                        'keyword', 'operator', 'reprlib',
                                        'weakref'),
                                modules='collections.abc'),
                        PythonModule(min_version=(3, 4),
                                deps=('_collections', '_collections_abc',
                                        'copy', 'heapq', 'itertools',
                                        'keyword', 'operator', 'reprlib',
                                        '_weakref'),
                                modules='collections.abc')),
    'collections.abc': (PythonModule(version=(3, 3),
                                deps='abc'),
                        PythonModule(min_version=(3, 4),
                                deps='_collections_abc')),
    'contextlib': (     PythonModule(version=(2, 6),
                                deps='functools'),
                        PythonModule(version=(2, 7),
                                deps=('functools', 'warnings')),
                        PythonModule(version=3,
                                deps=('collections', 'functools'))),
    'copy': (           PythonModule(version=(2, 6),
                                deps=('copy_reg', 'types')),
                        PythonModule(version=(2, 7),
                                deps=('copy_reg', 'types', 'weakref')),
                        PythonModule(version=3,
                                deps=('copyreg', 'types', 'weakref'))),
    'copy_reg':         PythonModule(version=2, deps='types'),
    'copyreg':          PythonModule(version=3),
    'cPickle':          ExtensionModule(version=2, source='cPickle.c'),
    'crypt': (          ExtensionModule(version=2,
                                source='cryptmodule.c', libs='-lcrypt'),
                        PythonModule(version=3,
                                deps=('collections', '_crypt', 'random',
                                        'string'))),
    'cStringIO':        ExtensionModule(version=2, source='cStringIO.c'),

    'datetime': (       ExtensionModule(version=2,
                                source=('datetimemodule.c', 'timemodule.c'),
                                deps='_strptime'),
                        PythonModule(version=3,
                                deps=('_datetime', 'math', '_strptime',
                                        'time'))),
    'dbm': (            ExtensionModule(version=2,
                                source='dbmmodule.c',
                                defines='HAVE_NDBM_H', libs='-lndbm'),
                        PythonModule(version=3,
                                deps=('io', 'os', 'struct'),
                                modules=('dbm.dumb', 'dbm.gnu', 'dbm.ndbm'))),
    'dbm.dumb':         PythonModule(version=3,
                                deps=('collections', 'io', 'os')),
    'dbm.gnu':          PythonModule(version=3, deps='_gdbm'),
    'dbm.ndbm':         PythonModule(version=3, deps='_dbm'),

    'email': (          PythonModule(version=2,
                                deps=('email.mime', 'email.parser'),
                                modules=('email.charset', 'email.encoders',
                                        'email.errors', 'email.generator',
                                        'email.header', 'email.iterators',
                                        'email.message', 'email.mime',
                                        'email.parser', 'email.utils')),
                        PythonModule(version=(3, 3),
                                deps='email.parser',
                                modules=('email.charset', 'email.encoders',
                                        'email.errors', 'email.generator',
                                        'email.header', 'email.headerregistry',
                                        'email.iterators', 'email.message',
                                        'email.mime', 'email.parser',
                                        'email.policy', 'email.utils')),
                        PythonModule(min_version=(3, 4),
                                deps='email.parser',
                                modules=('email.charset',
                                        'email.contentmanager',
                                        'email.encoders', 'email.errors',
                                        'email.generator', 'email.header',
                                        'email.headerregistry',
                                        'email.iterators', 'email.message',
                                        'email.mime', 'email.parser',
                                        'email.policy', 'email.utils'))),
    'email.charset': (  PythonModule(version=(2, 6),
                                deps=('email.base64mime', 'email.encoders',
                                        'email.errors', 'email.quoprimime')),
                        PythonModule(version=(2, 7),
                                deps=('codecs', 'email.base64mime',
                                        'email.encoders', 'email.errors',
                                        'email.quoprimime')),
                        PythonModule(version=3,
                                deps=('email.base64mime', 'email.encoders',
                                        'email.errors', 'email.quoprimime',
                                        'functools'))),
    'email.contentmanager': PythonModule(min_version=(3, 4),
                                    deps=('binascii', 'email.charset',
                                            'email.errors', 'email.message',
                                            'email.quoprimime')),
    'email.encoders':   PythonModule(deps=('base64', 'quopri')),
    'email.errors':     PythonModule(),
    'email.generator': (PythonModule(version=2,
                                deps=('cStringIO', 'email.header', 'random',
                                        're', 'time', 'warnings')),
                        PythonModule(version=(3, 3),
                                deps=('copy', 'email.charset', 'email.header',
                                        'email._policybase', 'email.utils',
                                        'io', 'random', 're', 'time',
                                        'warnings')),
                        PythonModule(min_version=(3, 4),
                                deps=('copy', 'email.utils', 'io', 'random',
                                        're', 'time'))),
    'email.header':     PythonModule(
                                deps=('binascii', 'email.base64mime',
                                        'email.charset', 'email.errors',
                                        'email.quoprimime', 're')),
    'email.headerregistry': PythonModule(version=3,
                                    deps=('email.errors',
                                            'email._header_value_parser',
                                            'email.utils')),
    'email.iterators': (PythonModule(version=2,
                                deps='cStringIO'),
                        PythonModule(version=3,
                                deps='io')),
    'email.message': (  PythonModule(version=2,
                                deps=('binascii', 'cStringIO', 'email.charset',
                                        'email.errors', 'email.generator',
                                        'email.iterators', 'email.utils', 're',
                                        'uu', 'warnings')),
                        PythonModule(version=(3, 3),
                                deps=('base64', 'binascii', 'email.charset',
                                        'email._encoded_words', 'email.errors',
                                        'email.generator', 'email.iterators',
                                        'email._policybase', 'email.utils',
                                        'io', 're', 'uu')),
                        PythonModule(min_version=(3, 4),
                                deps=('email.charset', 'email._encoded_words',
                                        'email.errors', 'email.generator',
                                        'email.iterators', 'email.policy',
                                        'email._policybase', 'email.utils',
                                        'io', 'quopri', 're', 'uu'))),
    'email.mime':       PythonModule(
                                modules=('email.mime.application',
                                        'email.mime.audio', 'email.mime.base',
                                        'email.mime.image',
                                        'email.mime.message',
                                        'email.mime.multipart',
                                        'email.mime.nonmultipart',
                                        'email.mime.text')),
    'email.mime.application':   PythonModule(
                                        deps=('email.encoders',
                                                'email.mime.nonmultipart')),
    'email.mime.audio': (   PythonModule(version=2,
                                    deps=('cStringIO', 'email.encoders',
                                            'email.mime.nonmultipart',
                                            'sndhdr')),
                            PythonModule(version=3,
                                    deps=('email.encoders',
                                            'email.mime.nonmultipart', 'io',
                                            'sndhdr'))),
    'email.mime.base':  PythonModule(deps='email.message'),
    'email.mime.image': PythonModule(
                                deps=('email.encoders',
                                        'email.mime.nonmultipart', 'imghdr')),
    'email.mime.message':   PythonModule(
                                    deps=('email.message',
                                            'email.mime.nonmultipart')),
    'email.mime.multipart': PythonModule(deps='email.mime.base'),
    'email.mime.nonmultipart':  PythonModule(
                                        deps=('email.errors',
                                                'email.mime.base')),
    'email.mime.text': (PythonModule(max_version=(3, 3),
                                deps=('email.encoders',
                                        'email.mime.nonmultipart')),
                        PythonModule(min_version=(3, 4),
                                deps='email.mime.nonmultipart')),
    'email.parser': (   PythonModule(version=2,
                                deps=('cStringIO', 'email.feedparser',
                                        'email.message', 'warnings')),
                        PythonModule(version=(3, 3),
                                deps=('email.feedparser', 'email.message',
                                        'email._policybase', 'io',
                                        'warnings')),
                        PythonModule(min_version=(3, 4),
                                deps=('email.feedparser', 'email._policybase',
                                        'io'))),
    'email.policy': (   PythonModule(version=(3, 3),
                                deps=('email.headerregistry',
                                        'email._policybase', 'email.utils')),
                        PythonModule(min_version=(3, 4),
                                deps=('email.contentmanager',
                                        'email.headerregistry',
                                        'email._policybase', 'email.utils'))),
    'email.utils': (    PythonModule(version=2,
                                deps=('base64', 'email.encoders',
                                        'email._parseaddr', 'os', 'quopri',
                                        'random', 're', 'socket', 'time',
                                        'urllib', 'warnings')),
                        PythonModule(version=(3, 3),
                                deps=('base64', 'datetime', 'email.charset',
                                        'email.encoders', 'email._parseaddr',
                                        'io', 'os', 'quopri', 'random', 're',
                                        'socket', 'time', 'urllib.parse',
                                        'warnings')),
                        PythonModule(min_version=(3, 4),
                                deps=('datetime', 'email.charset',
                                        'email._parseaddr', 'os', 'random',
                                        're', 'socket', 'time',
                                        'urllib.parse'))),
    # TODO - the non-core encodings.
    'encodings': (      PythonModule(version=2,
                                deps=('codecs', 'encodings.aliases'),
                                modules=('encodings.aliases',
                                        'encodings.ascii', 'encodings.cp437',
                                        'encodings.latin_1', 'encodings.mbcs',
                                        'encodings.utf_8')),
                        CorePythonModule(version=3,
                                deps=('codecs', 'encodings.aliases'),
                                modules=('encodings.aliases',
                                        'encodings.ascii', 'encodings.cp437',
                                        'encodings.latin_1', 'encodings.mbcs',
                                        'encodings.utf_8'))),
    'encodings.aliases': (  PythonModule(version=2),
                            CorePythonModule(version=3)),
    'encodings.ascii': (    PythonModule(version=2),
                            CorePythonModule(version=3)),
    'encodings.cp437': (    PythonModule(version=2),
                            CorePythonModule(version=3)),
    'encodings.latin_1': (  PythonModule(version=2),
                            CorePythonModule(version=3)),
    'encodings.mbcs': (     PythonModule(version=2),
                            CorePythonModule(version=3)),
    'encodings.utf_8': (    PythonModule(version=2),
                            CorePythonModule(version=3)),
    'enum':             PythonModule(version=3, deps=('collections', 'types')),
    'errno':            CoreExtensionModule(),
    'exceptions':       CoreExtensionModule(version=2),

    'faulthandler':     CoreExtensionModule(version=3),
    'fcntl':            ExtensionModule(source='fcntlmodule.c'),
    'fnmatch': (        PythonModule(version=2,
                                deps=('os', 'posixpath', 're')),
                        PythonModule(version=3,
                                deps=('functools', 'os', 'posixpath', 're'))),
    'functools': (      PythonModule(version=2,
                                deps='_functools'),
                        PythonModule(version=(3, 3),
                                deps=('collections', '_functools', '_thread')),
                        PythonModule(min_version=(3, 4),
                                deps=('abc', 'collections', '_functools',
                                        '_thread', 'types', 'weakref'))),
    'future_builtins':  ExtensionModule(version=2, source='future_builtins.c'),

    'gc':               CoreExtensionModule(),
    'gdbm':             ExtensionModule(version=2, source='gdbmmodule.c',
                                libs='-lgdbm'),
    'getpass': (        PythonModule(version=2,
                                deps=('msvcrt', 'os', 'pwd', 'termios',
                                        'warnings')),
                        PythonModule(version=3,
                                deps=('contextlib', 'io', 'msvcrt', 'os',
                                        'pwd', 'termios', 'warnings'))),
    'gettext': (        PythonModule(version=2,
                                deps=('copy', 'cStringIO', 'errno', 'locale',
                                        'os', 're', 'struct', 'token',
                                        'tokenize')),
                        PythonModule(version=3,
                                deps=('copy', 'errno', 'io', 'locale', 'os',
                                        're', 'struct', 'token', 'tokenize'))),
    'grp':              ExtensionModule(source='grpmodule.c'),

    'ftplib': (         PythonModule(version=(2, 6),
                                deps=('os', 're', 'socket')),
                        PythonModule(min_version=(2, 7), max_version=(3, 3),
                                deps=('os', 're', 'socket', 'ssl')),
                        PythonModule(min_version=(3, 4),
                                deps=('os', 're', 'socket', 'ssl',
                                        'warnings'))),

    'hashlib': (        PythonModule(version=(2, 6),
                                deps=('_hashlib', '_md5', '_sha', '_sha256',
                                        '_sha512')),
                        PythonModule(version=(2, 7),
                                deps=('binascii', '_hashlib', '_md5', '_sha',
                                        '_sha256', '_sha512', 'struct')),
                        PythonModule(version=3,
                                deps=('_hashlib', '_md5', '_sha1', '_sha256',
                                        '_sha512'))),
    'heapq': (          PythonModule(version=(2, 6),
                                deps=('bisect', '_heapq', 'itertools',
                                        'operator')),
                        PythonModule(version=(2, 7),
                                deps=('_heapq', 'itertools', 'operator')),
                        PythonModule(version=3,
                                deps=('_heapq', 'itertools'))),
    'html': (           PythonModule(version=(3, 3),
                                modules=('html.entities', 'html.parser')),
                        PythonModule(min_version=(3, 4),
                                deps=('html.entities', 're'),
                                modules=('html.entities', 'html.parser'))),
    'html.entities':    PythonModule(version=3),
    'html.parser': (    PythonModule(version=(3, 3),
                                deps=('html.entities', '_markupbase', 're',
                                        'warnings')),
                        PythonModule(min_version=(3, 4),
                                deps=('html', '_markupbase', 're',
                                        'warnings'))),
    'http':             PythonModule(version=3,
                                modules=('http.client', 'http.cookiejar',
                                        'http.cookies', 'http.server')),
    'http.client': (    PythonModule(version=(3, 3),
                                deps=('collections', 'email.message',
                                        'email.parser', 'io', 'os', 'socket',
                                        'ssl', 'urllib.parse', 'warnings')),
                        PythonModule(min_version=(3, 4),
                                deps=('collections', 'email.message',
                                        'email.parser', 'io', 'os', 'socket',
                                        'ssl', 'urllib.parse'))),
    'http.cookiejar':   PythonModule(version=3,
                                deps=('calendar', 'copy', 'datetime',
                                        'http.client', 're', 'threading',
                                        'time', 'urllib.parse',
                                        'urllib.request')),
    'http.cookies':     PythonModule(version=3, deps=('re', 'string', 'time')),
    'http.server': (    PythonModule(version=(3, 3),
                                deps=('argparse', 'base64', 'binascii', 'copy',
                                        'email.message', 'email.parser',
                                        'html', 'http.client', 'io',
                                        'mimetypes', 'os', 'posixpath', 'pwd',
                                        'select', 'shutil', 'socket',
                                        'socketserver', 'subprocess', 'time',
                                        'urllib.parse')),
                        PythonModule(min_version=(3, 4),
                                deps=('argparse', 'base64', 'binascii', 'copy',
                                        'html', 'http.client', 'io',
                                        'mimetypes', 'os', 'posixpath', 'pwd',
                                        'select', 'shutil', 'socket',
                                        'socketserver', 'subprocess', 'time',
                                        'urllib.parse'))),

    'imageop':          ExtensionModule(version=2, source='imageop.c'),
    'imghdr':           PythonModule(),
    'imp': (            CoreExtensionModule(version=2),
                        PythonModule(version=(3, 3),
                                deps=('_imp', 'importlib', 'os', 'tokenize',
                                        'warnings')),
                        PythonModule(min_version=(3, 4),
                                deps=('_imp', 'importlib', 'os', 'tokenize',
                                        'types', 'warnings'))),
    'importlib': (      PythonModule(version=(2, 7),
                                modules=()),
                        CorePythonModule(version=(3, 3),
                                deps=('importlib._bootstrap', '_imp'),
                                modules=('importlib.abc',
                                        'importlib.machinery',
                                        'importlib.util')),
                        CorePythonModule(min_version=(3, 4),
                                deps=('importlib._bootstrap', '_imp', 'types',
                                        'warnings'),
                                modules=('importlib.abc',
                                        'importlib.machinery',
                                        'importlib.util'))),
    'importlib.abc': (  PythonModule(version=(3, 3),
                                deps=('abc', 'imp', 'importlib._bootstrap',
                                        'importlib.machinery', 'marshal',
                                        'tokenize', 'warnings')),
                        PythonModule(min_version=(3, 4),
                                deps=('abc', 'importlib._bootstrap',
                                        'importlib.machinery'))),
    'importlib.machinery':  PythonModule(version=3,
                                    deps=('_imp', 'importlib._bootstrap')),
    'importlib.util': ( PythonModule(version=(3, 3),
                                    deps='importlib._bootstrap'),
                        PythonModule(min_version=(3, 4),
                                    deps=('contextlib', 'functools',
                                            'importlib._bootstrap',
                                            'warnings'))),
    'io': (             PythonModule(version=(2, 6),
                                deps=('__future__', 'abc', 'array', '_bytesio',
                                        'codecs', '_fileio', 'locale',
                                        'threading', 'os')),
                        PythonModule(version=(2, 7),
                                deps=('abc', '_io')),
                        CorePythonModule(version=3,
                                deps=('abc', '_io'))),
    'itertools': (      ExtensionModule(version=2, source='itertoolsmodule.c'),
                        CoreExtensionModule(version=3)),

    'keyword':          PythonModule(),

    'linecache': (      PythonModule(version=2,
                                deps='os'),
                        PythonModule(version=3,
                                deps=('os', 'tokenize'))),
    'linuxaudiodev':    ExtensionModule(version=2, source='linuxaudiodev.c'),
    'locale': (         PythonModule(version=2,
                                deps=('encodings', 'encodings.aliases',
                                        'functools', '_locale', 'os',
                                        'operator', 're')),
                        PythonModule(version=3,
                                deps=('collections', 'encodings',
                                        'encodings.aliases', 'functools',
                                        '_locale', 'os', 're'))),

    'marshal':          CoreExtensionModule(),
    'math': (           ExtensionModule(version=(2, 6),
                                source='mathmodule.c', libs='-lm'),
                        ExtensionModule(version=(2, 7),
                                source=('mathmodule.c', '_math.c'),
                                libs='-lm'),
                        ExtensionModule(version=3,
                                source=('mathmodule.c', '_math.c'),
                                libs='-lm')),
    'mimetypes': (      PythonModule(version=(2, 6),
                                deps=('os', 'posixpath', 'urllib')),
                        PythonModule(version=(2, 7),
                                deps=('os', 'posixpath', 'urllib', '_winreg')),
                        PythonModule(version=3,
                                deps=('os', 'posixpath', 'urllib.parse',
                                        'winreg'))),
    'mmap':             ExtensionModule(source='mmapmodule.c'),
    # TODO - msvcrt on Windows
    'msvcrt':           ExtensionModule(source='TODO', windows=True),

    'nis':              ExtensionModule(source='nismodule.c', libs='-lnsl'),

    'operator': (       ExtensionModule(version=2,
                                source='operator.c'),
                        CoreExtensionModule(version=(3, 3)),
                        PythonModule(min_version=(3, 4),
                                deps='_operator')),
    'os': (             PythonModule(version=2,
                                deps=('copy_reg', 'errno', 'nt', 'ntpath',
                                        'posix', 'posixpath', 'subprocess',
                                        'warnings')),
                        PythonModule(version=3,
                                deps=('collections', 'copyreg', 'errno', 'io',
                                        'nt', 'ntpath', 'posix', 'posixpath',
                                        'stat', 'subprocess', 'warnings'))),
    'ossaudiodev':      ExtensionModule(source='ossaudiodev.c'),

    'parser':           ExtensionModule(source='parsermodule.c'),
    'pickle': (         PythonModule(version=2,
                                deps=('binascii', 'copy_reg', 'cStringIO',
                                        'marshal', 're', 'struct', 'types')),
                        PythonModule(version=(3, 3),
                                deps=('codecs', '_compat_pickle', 'copyreg',
                                        'io', 'marshal', '_pickle', 're',
                                        'struct', 'types')),
                        PythonModule(min_version=(3, 4),
                                deps=('codecs', '_compat_pickle', 'copyreg',
                                        'io', 'itertools', 'marshal',
                                        '_pickle', 're', 'struct', 'types'))),
    'pwd':              CoreExtensionModule(),

    'quopri': (         PythonModule(version=2,
                                deps=('binascii', 'cStringIO')),
                        PythonModule(version=3,
                                deps=('binascii', 'io'))),

    'random': (         PythonModule(version=(2, 6),
                                deps=('__future__', 'binascii', 'math', 'os',
                                        '_random', 'time', 'types',
                                        'warnings')),
                        PythonModule(version=(2, 7),
                                deps=('__future__', 'binascii', 'hashlib',
                                        'math', 'os', '_random', 'time',
                                        'types', 'warnings')),
                        PythonModule(version=(3, 3),
                                deps=('collections', 'hashlib', 'math', 'os',
                                        '_random', 'time', 'types',
                                        'warnings')),
                        PythonModule(version=(3, 4),
                                deps=('_collections_abc', 'hashlib', 'math',
                                        'os', '_random', 'time', 'types',
                                        'warnings'))),
    're': (             PythonModule(version=2,
                                deps=('copy_reg', 'sre_compile',
                                        'sre_constants', 'sre_parse')),
                        PythonModule(version=(3, 3),
                                deps=('copyreg', 'functools', 'sre_compile',
                                        'sre_constants', 'sre_parse')),
                        PythonModule(min_version=(3, 4),
                                deps=('copyreg', 'sre_compile',
                                        'sre_constants', 'sre_parse'))),
    'readline':         ExtensionModule(source='readline.c',
                                libs='-lreadline -ltermcap'),
    'repr':             PythonModule(version=2, deps='itertools'),
    'reprlib':          PythonModule(version=3, deps=('itertools', '_thread')),
    'resource':         ExtensionModule(source='resource.c'),

    'select':           ExtensionModule(source='selectmodule.c'),
    'selectors':        PythonModule(min_version=(3, 4),
                                deps=('abc', 'collections', 'math', 'select')),
    'shutil': (         PythonModule(version=(2, 6),
                                deps=('errno', 'fnmatch', 'os', 'stat')),
                        PythonModule(version=(2, 7),
                                deps=('collections', 'errno', 'fnmatch', 'grp',
                                        'os', 'pwd', 'stat', 'tarfile',
                                        'zipfile')),
                        PythonModule(version=3,
                                deps=('collections', 'errno', 'fnmatch', 'grp',
                                        'nt', 'os', 'pwd', 'stat', 'tarfile',
                                        'zipfile'))),
    'signal':           CoreExtensionModule(),
    'sndhdr': (         PythonModule(max_version=(3, 3),
                                deps='aifc'),
                        PythonModule(min_version=(3, 4),
                                deps=('aifc', 'wave'))),
    'spwd':             ExtensionModule(source='spwdmodule.c'),
    'socket': (         PythonModule(version=(2, 6),
                                deps=('cStringIO', 'errno', 'os', 'ssl',
                                        '_ssl', '_socket', 'warnings')),
                        PythonModule(version=(2, 7),
                                deps=('cStringIO', 'errno', 'functools', 'os',
                                        'ssl', '_ssl', '_socket', 'types',
                                        'warnings')),
                        PythonModule(version=(3, 3),
                                deps=('errno', 'io', 'os', '_socket')),
                        PythonModule(min_version=(3, 4),
                                deps=('errno', 'enum', 'io', 'os',
                                        '_socket'))),
    'socketserver':     PythonModule(version=3,
                                deps=('errno', 'io', 'os', 'select', 'socket',
                                        'traceback', 'threading')),
    'ssl': (            PythonModule(version=2,
                                ssl=True,
                                deps=('base64', 'errno', 'socket', '_ssl',
                                        'textwrap', 'time')),
                        PythonModule(version=(3, 3),
                                ssl=True,
                                deps=('base64', 'errno', 're', 'socket', '_ssl',
                                        'textwrap', 'time', 'traceback')),
                        PythonModule(min_version=(3, 4),
                                ssl=True,
                                deps=('base64', 'collections', 'enum', 'errno',
                                        'os', 're', 'socket', '_ssl',
                                        'textwrap', 'time'))),
    'stat': (           PythonModule(version=2),
                        PythonModule(version=(3, 3)),
                        PythonModule(min_version=(3, 4),
                                deps='_stat')),
    'string': (         PythonModule(version=2,
                                deps=('re', 'strop')),
                        PythonModule(version=3,
                                deps=('collections', 're', '_string'))),
    'struct':           PythonModule(deps='_struct'),
    'subprocess': (     PythonModule(version=2,
                                deps=('errno', 'fcntl', 'gc', 'msvcrt', 'os',
                                        'pickle', 'select', 'signal',
                                        '_subprocess', 'threading',
                                        'traceback', 'types')),
                        PythonModule(version=(3, 3),
                                deps=('errno', 'gc', 'io', 'msvcrt', 'os',
                                        '_posixsubprocess', 'select', 'signal',
                                        'threading', 'time', 'traceback',
                                        'warnings', '_winapi')),
                        PythonModule(min_version=(3, 4),
                                deps=('errno', 'gc', 'io', 'msvcrt', 'os',
                                        '_posixsubprocess', 'select',
                                        'selectors', 'signal', 'threading',
                                        'time', 'traceback', 'warnings',
                                        '_winapi'))),
    'syslog':           ExtensionModule(source='syslogmodule.c'),

    'tarfile': (        PythonModule(version=2,
                                deps=('calendar', 'copy', 'cStringIO', 'errno',
                                        'grp', 'operator', 'pwd', 'os', 're',
                                        'shutil', 'stat', 'struct', 'time',
                                        'warnings')),
                        PythonModule(version=3,
                                deps=('calendar', 'copy', 'errno', 'grp', 'io',
                                        'pwd', 'os', 're', 'shutil', 'stat',
                                        'struct', 'time', 'warnings'))),
    'tempfile': (       PythonModule(version=(2, 6),
                                deps=('cStringIO', 'errno', 'fcntl', 'os',
                                        'random', 'thread')),
                        PythonModule(version=(2, 7),
                                deps=('cStringIO', 'errno', 'fcntl', 'io',
                                        'os', 'random', 'thread')),
                        PythonModule(version=(3, 3),
                                deps=('atexit', 'errno', 'fcntl', 'functools',
                                        'io', 'os', 'random', 'shutil',
                                        '_thread', 'warnings')),
                        PythonModule(min_version=(3, 4),
                                deps=('errno', 'functools', 'io', 'os',
                                        'random', 'shutil', '_thread',
                                        'warnings', 'weakref'))),
    'termios':          ExtensionModule(source='termios.c'),
    'textwrap': (       PythonModule(version=2,
                                deps=('re', 'string')),
                        PythonModule(version=3,
                                deps='re')),
    'thread':           CoreExtensionModule(version=2),
    'time':             ExtensionModule(source='timemodule.c', libs='-lm'),
    'threading': (      PythonModule(version=(2, 6),
                                deps=('collections', 'functools', 'random',
                                        'thread', 'time', 'traceback',
                                        'warnings')),
                        PythonModule(version=(2, 7),
                                deps=('collections', 'random', 'thread',
                                        'time', 'traceback', 'warnings')),
                        PythonModule(version=(3, 3),
                                deps=('_thread', 'time', 'traceback',
                                        '_weakrefset')),
                        PythonModule(min_version=(3, 4),
                                deps=('_collections', 'itertools', '_thread',
                                        'time', 'traceback', '_weakrefset'))),
    'token':            PythonModule(),
    'tokenize': (       PythonModule(version=(2, 6),
                                deps=('re', 'string', 'token')),
                        PythonModule(version=(2, 7),
                                deps=('itertools', 're', 'string', 'token')),
                        PythonModule(version=3,
                                deps=('codecs', 'collections', 'io',
                                        'itertools', 're', 'token'))),
    'traceback': (      PythonModule(version=2,
                                deps=('linecache', 'types')),
                        PythonModule(version=(3, 3),
                                deps='linecache'),
                        PythonModule(min_version=(3, 4),
                                deps=('linecache', 'operator'))),
    'types':            PythonModule(),

    'unicodedata':      ExtensionModule(source='unicodedata.c'),
    'urllib': (         PythonModule(version=2,
                                deps=('base64', 'cStringIO', 'email.utils',
                                        'ftplib', 'getpass', 'httplib',
                                        'mimetools', 'mimetypes', 'nturl2path',
                                        'os', 're', 'socket', 'ssl', 'string',
                                        'tempfile', 'time', 'urlparse',
                                        'warnings', '_winreg')),
                        PythonModule(version=3,
                                modules=('urllib.error', 'urllib.parse',
                                        'urllib.request', 'urllib.response',
                                        'urllib.robotparser'))),
    'urllib.error':     PythonModule(version=3, deps='urllib.response'),
    'urllib.parse':     PythonModule(version=3, deps=('collections', 're')),
    'urllib.request':   PythonModule(version=3,
                                deps=('base64', 'bisect', 'collections',
                                        'contextlib', 'email', 'email.utils',
                                        'fnmatch', 'ftplib', 'getpass',
                                        'hashlib', 'http.client',
                                        'http.cookiejar', 'io', 'mimetypes',
                                        'nturl2path', 'os', 'posixpath', 're',
                                        'socket', 'ssl', 'tempfile', 'time',
                                        'urllib.error', 'urllib.parse',
                                        'urllib.response', 'warnings',
                                        'winreg')),
    'urllib.response': (PythonModule(version=(3, 3)),
                        PythonModule(min_version=(3, 4),
                                deps='tempfile')),
    'urllib.robotparser':   PythonModule(version=3,
                                    deps=('time', 'urllib.parse',
                                            'urllib.request')),
    'urllib2': (        PythonModule(version=(2, 6),
                                deps=('base64', 'bisect', 'cStringIO',
                                        'cookielib', 'email.utils', 'ftplib',
                                        'hashlib', 'httplib', 'mimetools',
                                        'mimetypes', 'os', 'posixpath',
                                        'random', 're', 'socket', 'time',
                                        'types', 'urllib', 'urlparse')),
                        PythonModule(version=(2, 7),
                                deps=('base64', 'bisect', 'cStringIO',
                                        'cookielib', 'email.utils', 'ftplib',
                                        'hashlib', 'httplib', 'mimetools',
                                        'mimetypes', 'os', 'posixpath',
                                        'random', 're', 'socket', 'time',
                                        'types', 'urllib', 'urlparse',
                                        'warnings'))),
    'urlparse': (       PythonModule(version=(2, 6),
                                deps='collections'),
                        PythonModule(version=(2, 7),
                                deps=('collections', 're'))),
    'uu':               PythonModule(deps=('binascii', 'os')),

    'warnings': (       PythonModule(version=2,
                                deps=('linecache', 'types', 're',
                                        '_warnings')),
                        PythonModule(version=3,
                                deps=('linecache', 're', '_warnings'))),
    'wave': (           PythonModule(max_version=(3, 3),
                                deps=('array', 'chunk', 'struct')),
                        PythonModule(min_version=(3, 4),
                                deps=('audioop', 'chunk', 'collections',
                                        'struct'))),
    'weakref': (        PythonModule(version=(2, 6),
                                deps=('exceptions', 'UserDict', '_weakref')),
                        PythonModule(version=(2, 7),
                                deps=('exceptions', 'UserDict', '_weakref',
                                        '_weakrefset')),
                        PythonModule(version=(3, 3),
                                deps=('collections', 'copy', '_weakref',
                                        '_weakrefset')),
                        PythonModule(min_version=(3, 4),
                                deps=('atexit', 'collections', 'copy', 'gc',
                                        'itertools', '_weakref',
                                        '_weakrefset'))),
    # TODO - _winreg/winreg on Windows
    '_winreg':          ExtensionModule(version=2, source='TODO',
                                windows=True),
    'winreg':           ExtensionModule(version=3, source='TODO',
                                windows=True),

    'xml':              PythonModule(
                                modules=('xml.dom', 'xml.etree', 'xml.parsers',
                                        'xml.sax')),
    'xml.dom':          PythonModule(deps='xml.dom.domreg',
                                modules=('xml.dom.minidom',
                                        'xml.dom.pulldom')),
    'xml.dom.minidom': (PythonModule(version=2,
                                deps=('codecs', 'StringIO',
                                        'xml.dom.minicompat',
                                        'xml.dom.xmlbuilder')),
                        PythonModule(version=3,
                                deps=('codecs', 'io', 'xml.dom.minicompat',
                                        'xml.dom.xmlbuilder'))),
    'xml.dom.pulldom': (PythonModule(version=2,
                                deps=('cStringIO', 'types', 'xml.dom.minidom',
                                        'xml.sax.handler')),
                        PythonModule(version=3,
                                deps=('io', 'xml.dom.minidom',
                                        'xml.sax.handler'))),
    'xml.etree':        PythonModule(modules='xml.etree.ElementTree'),
    'xml.etree.ElementTree': (  PythonModule(version=(2, 6),
                                        deps=('re', 'string',
                                                'xml.etree.ElementPath',
                                                'xml.parsers.expat')),
                                PythonModule(version=(2, 7),
                                        deps=('re', 'warnings',
                                                'xml.etree.ElementPath',
                                                'xml.parsers.expat')),
                                PythonModule(version=3,
                                        deps=('contextlib', '_elementtree',
                                                'io', 'locale', 're',
                                                'warnings',
                                                'xml.etree.ElementPath',
                                                'xml.parsers.expat'))),
    'xml.parsers':      PythonModule(modules='xml.parsers.expat'),
    'xml.parsers.expat':    PythonModule(deps='pyexpat'),
    'xml.sax': (        PythonModule(version=2,
                                deps=('cStringIO', 'os', 'xml.sax._exceptions',
                                        'xml.sax.handler',
                                        'xml.sax.xmlreader'),
                                modules=('xml.sax.handler', 'xml.sax.saxutils',
                                        'xml.sax.xmlreader')),
                        PythonModule(version=3,
                                deps=('io', 'os', 'xml.sax._exceptions',
                                        'xml.sax.handler',
                                        'xml.sax.xmlreader'),
                                modules=('xml.sax.handler', 'xml.sax.saxutils',
                                        'xml.sax.xmlreader'))),
    'xml.sax.handler':  PythonModule(),
    'xml.sax.saxutils': (   PythonModule(version=(2, 6),
                                    deps=('codecs', 'os', 'types', 'urlparse',
                                            'urllib', 'xml.sax.handler',
                                            'xml.sax.xmlreader')),
                            PythonModule(version=(2, 7),
                                    deps=('io', 'os', 'types', 'urlparse',
                                            'urllib', 'xml.sax.handler',
                                            'xml.sax.xmlreader')),
                            PythonModule(version=3,
                                    deps=('codecs', 'io', 'os', 'urllib.parse',
                                            'urllib.request',
                                            'xml.sax.handler',
                                            'xml.sax.xmlreader'))),
    'xml.sax.xmlreader':    PythonModule(
                                    deps=('xml.sax._exceptions',
                                            'xml.sax.handler',
                                            'xml.sax.saxutils')),

    'zipfile': (        PythonModule(version=(2, 6),
                                deps=('binascii', 'cStringIO', 'os', 'shutil',
                                        'stat', 'struct', 'time', 'zlib')),
                        PythonModule(version=(2, 7),
                                deps=('binascii', 'cStringIO', 'io', 'os',
                                        're', 'shutil', 'stat', 'string',
                                        'struct', 'time', 'zlib')),
                        PythonModule(version=(3, 3),
                                deps=('binascii', 'imp', 'io', 'os', 're',
                                        'shutil', 'stat', 'struct', 'time',
                                        'warnings', 'zlib')),
                        PythonModule(min_version=(3, 4),
                                deps=('binascii', 'importlib.util', 'io', 'os',
                                        're', 'shutil', 'stat', 'struct',
                                        'time', 'warnings', 'zlib'))),
    'zipimport':        CoreExtensionModule(),
    'zlib':             ExtensionModule(source='zlibmodule.c', libs='-lz'),

    # These are internal modules.
    '_ast':             CoreExtensionModule(internal=True),

    '_bisect':          ExtensionModule(internal=True,
                                source='_bisectmodule.c'),
    '_bsdb':            ExtensionModule(version=2,
                                internal=True, source='_bsddb.c', libs='-ldb'),
    '_bytesio':         ExtensionModule(version=(2, 6),
                                internal=True, source='_bytesio.c'),
    '_bz2':             ExtensionModule(version=3, internal=True,
                                source='_bz2mocule.c', libs='-lbz2'),

    '_codecs':          CoreExtensionModule(internal=True),
    '_codecs_cn':       ExtensionModule(internal=True,
                                source='cjkcodecs/_codecs_cn.c'),
    '_codecs_hk':       ExtensionModule(internal=True,
                                source='cjkcodecs/_codecs_hk.c'),
    '_codecs_iso2022':  ExtensionModule(internal=True,
                                source='cjkcodecs/_codecs_iso2022.c'),
    '_codecs_jp':       ExtensionModule(internal=True,
                                source='cjkcodecs/_codecs_jp.c'),
    '_codecs_kr':       ExtensionModule(internal=True,
                                source='cjkcodecs/_codecs_kr.c'),
    '_codecs_tw':       ExtensionModule(internal=True,
                                source='cjkcodecs/_codecs_tw.c'),
    '_collections': (   ExtensionModule(version=2,
                                internal=True, source='_collectionsmodule.c'),
                        CoreExtensionModule(version=3,
                                internal=True)),
    '_collections_abc': PythonModule(min_version=(3, 4),
                                internal=True, deps='abc'),
    '_compat_pickle':   PythonModule(version=3, internal=True),
    '_crypt':           ExtensionModule(version=3, internal=True,
                                source='_cryptmodule.c', libs='-lcrypt'),
    '_csv':             ExtensionModule(internal=True, source='_csv.c'),
    '_curses':          ExtensionModule(internal=True,
                                source='_cursesmodule.c',
                                libs='-lcurses -ltermcap'),
    '_curses_panel':    ExtensionModule(internal=True,
                                source='_curses_panel.c',
                                libs='-lpanel -lcurses'),

    '_datetime':        ExtensionModule(version=3,
                                internal=True, source='_datetimemodule.c'),
    '_dbm':             ExtensionModule(version=3, source='_dbmmodule.c',
                                defines='HAVE_NDBM_H', libs='-lndbm'),

    '_elementtree': (   ExtensionModule(version=2,
                                internal=True, source='_elementtree.c',
                                defines='HAVE_EXPAT_CONFIG_H USE_PYEXPAT_CAPI',
                                deps='pyexpat'),
                        ExtensionModule(version=3,
                                internal=True, source='_elementtree.c',
                                defines='HAVE_EXPAT_CONFIG_H USE_PYEXPAT_CAPI',
                                deps=('copy', 'pyexpat',
                                        'xml.etree.ElementPath'))),
    'email.base64mime': (   PythonModule(version=2,
                                    internal=True,
                                    deps=('binascii', 'email.utils')),
                            PythonModule(version=3,
                                    internal=True,
                                    deps=('base64', 'binascii'))),
    'email._encoded_words': PythonModule(version=3,
                                    internal=True,
                                    deps=('base64', 'binascii', 'email.errors',
                                            'functools', 're', 'string')),
    'email.feedparser': (   PythonModule(version=2,
                                    internal=True,
                                    deps=('email.errors', 'email.message',
                                            're')),
                            PythonModule(version=3,
                                    internal=True,
                                    deps=('email.errors', 'email.message',
                                            'email._policybase', 're'))),
    'email._header_value_parser':   PythonModule(version=3,
                                            internal=True,
                                            deps=('collections',
                                                    'email._encoded_words',
                                                    'email.errors',
                                                    'email.utils', 're',
                                                    'string', 'urllib')),
    'email._parseaddr': (   PythonModule(version=(2, 6),
                                    internal=True, deps='time'),
                            PythonModule(min_version=(2, 7),
                                    internal=True, deps=('calendar', 'time'))),
    'email._policybase':    PythonModule(version=3,
                                    internal=True,
                                    deps=('abc', 'email.charset',
                                            'email.header', 'email.utils')),
    'email.quoprimime': (   PythonModule(version=2,
                                    internal=True,
                                    deps=('email.utils', 're', 'string')),
                            PythonModule(version=(3, 3),
                                    internal=True,
                                    deps=('io', 're', 'string')),
                            PythonModule(min_version=(3, 4),
                                    internal=True, deps=('re', 'string'))),

    '_fileio':          ExtensionModule(version=(2, 6),
                                internal=True, source='_fileio.c'),
    '_functools': (     ExtensionModule(version=2,
                                internal=True, source='_functoolsmodule.c'),
                        CoreExtensionModule(version=3,
                                internal=True)),

    'genericpath':      PythonModule(internal=True, deps=('os', 'stat')),
    '_gdbm':            ExtensionModule(version=3, internal=True,
                                source='_gdbmmodule.c', libs='-lgdbm'),

    '_hashlib':         ExtensionModule(internal=True, ssl=True,
                                source='_hashopenssl.c',
                                libs='-lssl -lcrypto'),
    '_heapq':           ExtensionModule(internal=True,
                                source='_heapqmodule.c'),
    '_hotshot':         ExtensionModule(version=2, internal=True,
                                source='_hotshotmodule.c'),

    '_imp':             CoreExtensionModule(version=3, internal=True),
    'importlib._bootstrap': PythonModule(version=3, internal=True),
    '_io': (            ExtensionModule(version=(2, 7),
                                internal=True,
                                source=('_io/bufferedio.c', '_io/bytesio.c',
                                        '_io/fileio.c', '_io/iobase.c',
                                        '_io/_iomodule.c', '_io/stringio.c',
                                        '_io/textio.c'),
                                subdir='_io'),
                        CoreExtensionModule(version=3,
                                internal=True)),

    '_json':            ExtensionModule(internal=True, source='_jsonmodule.c'),

    '_locale': (        ExtensionModule(version=2,
                                internal=True, source='_localemodule.c',
                                libs='-lintl'),
                        CoreExtensionModule(version=3,
                                internal=True)),
    '_lsprof':          ExtensionModule(internal=True,
                                source=('_lsprof.c', 'rotatingtree.c')),
    '_lzma':            ExtensionModule(version=3, internal=True,
                                source='_lzmamodule.c', libs='-llzma'),

    '_markupbase':      PythonModule(version=3, internal=True, deps='re'),
    '_md5': (           ExtensionModule(version=2,
                                internal=True, ssl=False,
                                source=('md5module.c', 'md5.c')),
                        ExtensionModule(version=3,
                                internal=True, source='md5module.c')),
    '_multibytecodec':  ExtensionModule(internal=True,
                                source='cjkcodecs/_multibytecodec.c'),

    # TODO - nt on Windows
    'nt':               ExtensionModule(internal=True, source='TODO',
                                windows=True),
    'ntpath':           PythonModule(internal=True, windows=True,
                                deps=('genericpath', 'nt', 'os', 'stat',
                                        'string', 'warnings')),
    # TODO - nturl2path on Windows
    'nturl2path':       ExtensionModule(internal=True, source='TODO',
                                windows=True),

    '_opcode':          ExtensionModule(min_version=(3, 4),
                                internal=True, source='_opcode.c'),
    '_operator':        CoreExtensionModule(min_version=(3, 4)),

    '_pickle':          ExtensionModule(version=3, source='_pickle.c'),
    'posix':            CoreExtensionModule(internal=True, windows=False),
    'posixpath':        PythonModule(internal=True, windows=False,
                                deps=('genericpath', 'os', 'pwd', 're', 'stat',
                                        'warnings')),
    '_posixsubprocess': ExtensionModule(version=3, internal=True,
                                windows=False, source='_posixsubprocess.c'),
    'pyexpat':          ExtensionModule(internal=True,
                                source=('expat/xmlparse.c', 'expat/xmlrole.c',
                                        'expat/xmltok.c', 'pyexpat.c'),
                                defines='HAVE_EXPAT_CONFIG_H', subdir='expat'),

    '_random':          ExtensionModule(source='_randommodule.c'),

    '_sha':             ExtensionModule(version=2, internal=True, ssl=False,
                                source='shamodule.c'),
    '_sha1':            ExtensionModule(version=3, internal=True, ssl=False,
                                source='sha1module.c'),
    '_sha256':          ExtensionModule(internal=True, ssl=False,
                                source='sha256module.c'),
    '_sha512':          ExtensionModule(internal=True, ssl=False,
                                source='sha512module.c'),

    '_socket': (        ExtensionModule(version=(2, 6),
                                internal=True, source='socketmodule.c'),
                        ExtensionModule(version=(2, 7),
                                internal=True,
                                source=('socketmodule.c', 'timemodule.c')),
                        ExtensionModule(version=3,
                                internal=True, source='socketmodule.c')),
    '_sqlite3':         ExtensionModule(internal=True,
                                source=('_sqlite/cache.c',
                                        '_sqlite/connection.c',
                                        '_sqlite/cursor.c',
                                        '_sqlite/microprotocols.c',
                                        '_sqlite/module.c',
                                        '_sqlite/prepare_protocol.c',
                                        '_sqlite/row.c', '_sqlite/statement.c',
                                        '_sqlite/util.c'),
                                defines='SQLITE_OMIT_LOAD_EXTENSION',
                                subdir='_sqlite'),
    '_sre':             CoreExtensionModule(),
    'sre_compile':      PythonModule(internal=True,
                                deps=('array', '_sre', 'sre_constants',
                                        'sre_parse')),
    'sre_constants': (  PythonModule(version=(2, 6),
                                internal=True),
                        PythonModule(version=(2, 7),
                                internal=True, deps='_sre'),
                        PythonModule(version=3,
                                internal=True, deps='_sre')),
    'sre_parse': (      PythonModule(version=2,
                                internal=True, deps='sre_constants'),
                        PythonModule(version=3,
                                internal=True,
                                deps=('sre_constants', 'warnings'))),
    '_ssl':             ExtensionModule(internal=True, ssl=True,
                                source='_ssl.c', libs='-lssl -lcrypto'),
    '_stat':            CoreExtensionModule(min_version=(3, 4), internal=True),
    '_string':          CoreExtensionModule(version=3, internal=True),
    '_strptime': (      PythonModule(version=2,
                                internal=True,
                                deps=('calendar', 'datetime', 'locale', 're',
                                        'thread', 'time')),
                        PythonModule(version=3,
                                internal=True,
                                deps=('calendar', 'datetime', 'locale', 're',
                                        '_thread', 'time'))),
    '_struct':          ExtensionModule(internal=True, source='_struct.c'),
    # TODO - _subprocess on Windows
    '_subprocess':      ExtensionModule(version=2, internal=True,
                                source='TODO', windows=True),
    '_symtable':        CoreExtensionModule(internal=True),

    '_testcapi':        ExtensionModule(internal=True,
                                source='_testcapimodule.c'),
    '_tracemalloc':     CoreExtensionModule(min_version=(3, 4), internal=True),

    '_warnings':        CoreExtensionModule(internal=True),
    '_weakref': (       ExtensionModule(version=(2, 6),
                                internal=True, source='_weakref.c'),
                        CoreExtensionModule(version=(2, 7),
                                internal=True),
                        CoreExtensionModule(version=3)),
    '_weakrefset': (    PythonModule(version=(2, 7),
                                internal=True, deps='_weakref'),
                        PythonModule(version=3,
                                internal=True, deps='_weakref')),
    # TODO - _winapi on Windows
    '_winapi':          ExtensionModule(version=3, internal=True,
                                source='TODO', windows=True),

    'xml.dom.domreg': ( PythonModule(version=2,
                                internal=True,
                                deps=('os', 'xml.dom.minicompat')),
                        PythonModule(version=3,
                                internal=True, deps='os')),
    'xml.dom.expatbuilder': PythonModule(internal=True,
                                    deps=('xml.dom.minicompat',
                                            'xml.dom.minidom',
                                            'xml.parsers.expat')),
    'xml.dom.minicompat':   PythonModule(internal=True),
    'xml.dom.xmlbuilder': ( PythonModule(version=2,
                                    internal=True,
                                    deps=('copy', 'posixpath', 'urllib2',
                                            'urlparse',
                                            'xml.dom.expatbuilder')),
                            PythonModule(version=3,
                                    internal=True,
                                    deps=('copy', 'posixpath', 'urllib.parse',
                                            'urllib.request',
                                            'xml.dom.expatbuilder'))),
    'xml.etree.ElementPath':    PythonModule(internal=True, deps='re'),
    'xml.sax._exceptions':  PythonModule(internal=True),
}


def _get_module_for_version(name, major, minor):
    """ Return the module meta-data for a particular version.  None is returned
    if there is none but this should not happen with correct meta-data.
    """

    versions = _metadata.get(name)

    if versions is None:
        return None

    if not isinstance(versions, tuple):
        versions = (versions, )

    for module in versions:
        min_major, min_minor = module.min_version
        max_major, max_minor = module.max_version

        if major >= min_major and major <= max_major:
            if minor >= min_minor and minor <= max_minor:
                break
    else:
        module = None

    return module


def get_python_metadata(major, minor, ssl):
    """ Return the dict of PythonMetadata instances for a particular version of
    Python.  It is assumed that the version is valid.
    """

    # Find the most recent version that is not later than the desired version.
    version = (major, minor)
    best = None
    best_version = (0, 0)

    for key, value in _python_metadata.items():
        if version >= key and key > best_version:
            best = value
            best_version = key

    return best


if __name__ == '__main__':

    def check_modules_for_version(names, major, minor, seen=None):
        """ Sanity check a list of module names. """

        if seen is None:
            top_level = True
            seen = {}
        else:
            top_level = False

        for name in names:
            # Detect recursive dependences.
            if name in seen:
                continue

            versions = _metadata.get(name)
            if versions is None:
                print("Unknown module '{0}'".format(name))
                continue

            if not isinstance(versions, tuple):
                versions = (versions, )

            # Check the version numbers.
            matches = []
            for module in versions:
                min_major, min_minor = module.min_version
                max_major, max_minor = module.max_version

                if min_major > max_major:
                    print("Module '{0}' major version numbers are swapped".format(name))
                elif min_major == max_major and min_minor > max_minor:
                    print("Module '{0}' minor version numbers are swapped".format(name))

                if major >= min_major and major <= max_major:
                    if minor >= min_minor and minor <= max_minor:
                        matches.append(module)

            nr_matches = len(matches)

            if nr_matches != 1:
                if nr_matches > 1:
                    print("Module '{0}' has overlapping versions".format(name))

                continue

            module = matches[0]

            if module.internal and not module.core:
                if top_level:
                    if name not in seen:
                        # This internal, non-core module is not used so far.
                        seen[name] = True
                else:
                    # This internal, non-core module is used.
                    seen[name] = False
            else:
                seen[name] = None

            # Check the dependencies.
            check_modules_for_version(module.deps, major, minor, seen)

            # Check the package contents.
            if isinstance(module, PythonModule) and module.modules is not None:
                check_modules_for_version(module.modules, major, minor, seen)

        if top_level:
            # See if there are any internal, non-core modules that are unused.
            for name, unused in seen.items():
                if unused is True:
                    print("Unused module '{0}'".format(name))

    def check_version(major, minor):
        """ Carry out sanity checks for a particular version of Python. """

        print("Checking Python v{0}.{1}...".format(major, minor))

        check_modules_for_version(_metadata.keys(), major, minor)

    # Check each supported version.
    check_version(2, 6)
    check_version(2, 7)
    check_version(3, 3)
    check_version(3, 4)
