# -*- coding: utf-8 -*-
from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from z3c.form.interfaces import HIDDEN_MODE


class AddForm(add.DefaultAddForm):
    def updateWidgets(self):
        super(AddForm, self).updateWidgets()

        self.widgets["IBasic.description"].mode = HIDDEN_MODE


class AddView(add.DefaultAddView):
    form = AddForm


class EditForm(edit.DefaultEditForm):
    def updateWidgets(self):
        super(EditForm, self).updateWidgets()

        self.widgets["IBasic.description"].mode = HIDDEN_MODE


class EditView(edit.DefaultEditView):
    form = EditForm
