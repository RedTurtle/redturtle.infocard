# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


class ICard(model.Schema):
    """ Marker interface for Card
    """


@implementer(ICard)
class Card(Item):
    """
    """
