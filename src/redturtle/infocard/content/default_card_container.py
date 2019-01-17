# -*- coding: utf-8 -*-
from plone.app.contenttypes.content import Folder
from plone.dexterity.content import Container
from redturtle.infocard.interfaces import IDefaultCardContainer
from zope.interface import implementer


@implementer(IDefaultCardContainer)
class DefaultCardContainer(Folder):
    """
    """
