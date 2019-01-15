# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from redturtle.infocard.interfaces import IInfocardContainer
from zope.interface import implementer


@implementer(IInfocardContainer)
class InfocardContainer(Container):
    """
    """
