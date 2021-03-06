Introduction
============

:program:`pyqtdeploy` is a tool that, in conjunction with other tools provided
with Qt, enables the deployment of PyQt applications written with Python v2.7
or Python v3.3 or later.  It supports deployment to desktop platforms (Linux,
Windows and macOS) and to mobile platforms (iOS and Android).

Normally you would create statically compiled versions of the Python
interpreter library, any third party extension modules, PyQt and Qt.  This way
your application has no external dependencies.  However there is nothing to
stop you using shared versions of any of these components in order to reduce
the size of the application, but at the cost of increasing the complexity of
the deployment.

:program:`pyqtdeploy` itself requires PyQt5 and Python v3.5 or later.

:program:`pyqtdeploy` works by taking the individual modules of a PyQt
application, freezing them, and then placing them in a Qt resource file that is
converted to C++ code by Qt's :program:`rcc` tool.  Python's standard library
is handled in the same way.

:program:`pyqtdeploy` generates a simple C++ wrapper around the Python
interpreter library that uses the Python import mechanism to enable access to
the embedded frozen modules in a similar way that Python supports the packaging
of modules in zip files.

Finally :program:`pyqtdeploy` generates a target-specific Qt ``.pro`` file that
describes all the generated C++ code.  From this Qt's :program:`qmake` tool is
used to generate a ``Makefile`` which will then generate a single executable.
Further Qt and/or platform specific tools can then be used to convert the
executable to a target-specific deployable package.

When run :program:`pyqtdeploy` presents a GUI that allows all the separate
components to be specified.  This information is stored in a
:program:`pyqtdeploy` project file.

:program:`pyqtdeploy` does not (yet) perform auto-discovery of Python standard
library modules or third party modules to be included with the application.
You must specify these yourself.  However it does understand the
inter-dependencies within the standard library, so you only need to specify
those packages that your application explicitly imports.

A companion program :program:`pyqtdeploy-build` can be run from the command
line (or a shell script or batch file) to generate the C++ code from a project
file.

Another companion program :program:`pyqtdeploy-sysroot` provides support for
creating a system root directory containing target-specific installations of
certain components (e.g. Python itself and PyQt).

.. note::

    Creating a single executable (particularly one with no external
    dependencies) from a complex Python application (particularly one that uses
    external C extension modules) is not a simple task.  It requires experience
    of C code, compilers, build systems and the ability to debug associated
    problems.  You have been warned!


Differences from Version 1
--------------------------

There have been a number of changes to :program:`pyqtdeploy` since v1.  Most of
these changes are related to the supporting tools rather than the GUI.  Project
files created for v1 are automatically updated by later versions.

Python v3.6 or later is required for Android, support for earlier versions has
been removed.

v1 recommended a directory structure to adopt when assembling the various parts
of a deployable application.  This was refered to as the *sysroot* directory.
An unsupported script, :program:`build-sysroot.py`, was provided that created
the sysroot directory and was able to build and install a limited number of
components - mainly PyQt and related packages.  It used configuration files
generated by the :program:`pyqtdeploycli` program to specify how those
components were built, e.g. which individual modules and features were enabled.
:program:`build-sysroot.py` has been replaced with the fully supported 
:program:`pyqtdeploy-sysroot` program.  Individual component support is
implemented by a configurable component plugin.  An API is provided for you to
write (and contribute) your own plugins for additional components.  As with v1,
using the sysroot directory structure is entirely optional.

The :program:`pyqtdeploycli` program has been removed.  The build functionality
has been replaced by the new :program:`pyqtdeploy-build` program.

The ``Build`` tab of the :program:`pyqtdeploy` GUI has been removed.  The sole
purpose of the GUI is now to create and modify a project file.

The C++ code and :program:`qmake` ``.pro`` file generated by v1 attempted to be
portable across all target architectures.  :program:`pyqtdeploy-build` will
generate code specific for a single target architecture which is determined by
the :option:`--target <pyqtdeploy-build --target>` option and default to the
host architecture.


Author
------

:program:`pyqtdeploy` is copyright (c) Riverbank Computing Limited.  Its
homepage is https://www.riverbankcomputing.com/software/pyqtdeploy/.

Support may be obtained from the PyQt mailing list at
https://www.riverbankcomputing.com/mailman/listinfo/pyqt/.


License
-------

:program:`pyqtdeploy` is released under the BSD license.


Installation
------------

:program:`pyqtdeploy` can be downloaded and installed from
`PyPi <https://pypi.python.org/pypi/pyqtdeploy/>`_::

    pip3 install pyqtdeploy

:program:`pyqtdeploy` requires
`PyQt5 <https://www.riverbankcomputing.com/software/pyqt/download5>`_ to be
installed.  This is not installed automatically.
