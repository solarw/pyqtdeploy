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


from PyQt5.QtWidgets import QFormLayout, QVBoxLayout, QWidget

from .filename_editor import FilenameEditor
from .mfs_package_editor import MfsPackageEditor


class ApplicationPage(QWidget):
    """ The GUI for the application page of a project. """

    # The page's label.
    label = "Application Source"

    @property
    def project(self):
        """ The project property getter. """

        return self._project

    @project.setter
    def project(self, value):
        """ The project property setter. """

        if self._project != value:
            self._project = value
            self._script_edit.setProject(value)
            self._update_page()

    def __init__(self):
        """ Initialise the page. """

        super().__init__()

        self._project = None

        # Create the page's GUI.
        layout = QVBoxLayout()

        form = QFormLayout()

        self._script_edit = FilenameEditor("Application Script",
                placeholderText="Application script",
                whatsThis="The name of the application's main script file.",
                textEdited=self._script_changed)
        form.addRow("Main script file", self._script_edit)

        layout.addLayout(form)

        self._package_edit = MfsPackageEditor("Application Package",
                scanning="application package...")
        self._package_edit.package_changed.connect(self._package_changed)
        layout.addWidget(self._package_edit)

        self.setLayout(layout)

    def _update_page(self):
        """ Update the page using the current project. """

        project = self.project

        self._script_edit.setText(project.application_script)
        self._package_edit.configure(project.application_package, project)

    def _script_changed(self, value):
        """ Invoked when the user edits the application script name. """

        self.project.application_script = self.project.relative_path(value)
        self.project.modified = True

    def _package_changed(self):
        """ Invoked when the user edits the application package. """

        self.project.modified = True
