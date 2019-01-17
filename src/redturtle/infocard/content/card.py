# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from redturtle.infocard.interfaces import ICard
from zope.interface import implementer


@implementer(ICard)
class Card(Item):
    """
    """
