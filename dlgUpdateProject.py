# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from dlgUpdateProjectBase import Ui_UpdateProjectDialogBase


class UpdateProjectDialog(QDialog, Ui_UpdateProjectDialogBase):
    def __init__(self, parent, projects):
        QDialog.__init__(self)
        self.setupUi(self)
        self.projects = projects
        self.buttonBox.accepted.connect(self.updateProject)
        self.fillCombo()

    def fillCombo(self):
        self.existingProjectsCombo.clear()
        for project in self.projects:
            print project
            self.existingProjectsCombo.addItem(project['name'], project)

    def updateProject(self):
        currentIndex = self.existingProjectsCombo.currentIndex()
        self.project = self.existingProjectsCombo.itemData(currentIndex)