# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone.app.dexterity.behaviors import constrains
from plone import api


CAN_CONTAINS = {"default": ("Card",)}


def add_new_infocardcontainer(self, event):
    """ Add folder default for general card """

    default = api.content.create(
        container=event.object, type="DefaultCardContainer", title="Default"
    )
