# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from rt.infocard.interfaces import IInfocard
from zope.interface import implementer


@implementer(IInfocard)
class Infocard(Container):
    """
    """
