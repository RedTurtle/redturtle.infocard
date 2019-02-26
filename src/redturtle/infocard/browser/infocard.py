# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from z3c.form.interfaces import HIDDEN_MODE
from z3c.form.interfaces import DISPLAY_MODE


class AddForm(add.DefaultAddForm):
    def updateWidgets(self):
        super(AddForm, self).updateWidgets()

        del self.widgets["order"]

    def datagridUpdateWidgets(self, subform, widgets, widget):
        subform.widgets["title_card"].mode = DISPLAY_MODE
        subform.widgets["uid_card"].mode = HIDDEN_MODE


class AddView(add.DefaultAddView):
    form = AddForm


class EditForm(edit.DefaultEditForm):
    def updateWidgets(self):
        super(EditForm, self).updateWidgets()

        if not api.content.find(context=self.context, portal_type="Card"):
            del self.widgets["order"]
        else:
            self.widgets["order"].allow_reorder = True
            self.widgets["order"].allow_insert = False
            self.widgets["order"].allow_delete = False
            self.widgets["order"].auto_append = False

            # hide a column
            self.widgets["order"].columns = [
                c
                for c in self.widgets["order"].columns
                if c["name"] != "uid_card"
            ]

    def datagridUpdateWidgets(self, subform, widgets, widget):
        subform.widgets["title_card"].mode = DISPLAY_MODE
        subform.widgets["uid_card"].mode = HIDDEN_MODE


class EditView(edit.DefaultEditView):
    form = EditForm
