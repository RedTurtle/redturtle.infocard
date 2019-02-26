# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from plone import api
from redturtle.infocard.content.default_card_container import DefaultCardContainer
from redturtle.infocard.content.infocard import Infocard


def remove_card(self, event):
    """
    Al momento della creazione di una card viene aggiornata la posizione delle
    Card
    """
    if isinstance(event.oldParent, Infocard):
        event.oldParent.updateCards()


def add_card(self, event):
    """
    Quando viene aggiunta una card, se si trova all'interno di una cartella di
    default, allora viene copiata in tutte le infocard
    """
    parent = aq_parent(self)
    if isinstance(parent, DefaultCardContainer):

        # aggiungo la card a tutte le infocard di quel container
        infocards = api.content.find(
            context=aq_parent(parent),
            portal_type="InformationCard"
        )

        for infocard in infocards:
            infocard = infocard.getObject()
            api.content.copy(source=self, target=infocard)
