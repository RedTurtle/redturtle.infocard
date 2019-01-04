# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone.app.dexterity.behaviors import constrains
from plone import api


CAN_CONTAINS = {"card": ("Card",)}


def add_new_infocardcontainer(self, event):
    """ Add folder default for general card """

    default = api.content.create(
        container=event.object, type="Folder", title="Default"
    )
    api.content.transition(obj=default, transition="publish")

    behavior = ISelectableConstrainTypes(default)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    if CAN_CONTAINS.get(default.getId(), None):
        behavior.setImmediatelyAddableTypes(CAN_CONTAINS["card"])
