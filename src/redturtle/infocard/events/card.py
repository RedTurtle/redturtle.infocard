# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from plone import api
from redturtle.infocard.content.default_card_container import DefaultCardContainer
from redturtle.infocard.content.infocard import Infocard


def remove_card(self, event):

    if isinstance(event.oldParent, DefaultCardContainer):
        # aggiorno tutte le infocard del container
        infocards = api.content.find(
            context=aq_parent(event.oldParent),
            portal_type="Infocard"
        )

        infocards = [x.getObject().updateCards() for x in infocards]

    elif isinstance(event.oldParent, Infocard):
        # aggiorno solo l'infocard interessata
        event.oldParent.updateCards()