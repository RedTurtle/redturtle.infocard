# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from plone import api
from redturtle.infocard.content.default_card_container import (
    DefaultCardContainer,
)
from redturtle.infocard.content.infocard import Infocard


def copy_default_card(self, event):
    """
    Quando viene creata una nuova infocard vengono copiate le card di default
    all'interno dell'infocard
    """
    infocard_container = aq_parent(event.object)

    if getattr(infocard_container, "default", None):
        cards = api.content.find(
            context=infocard_container.default, portal_type="Card"
        )

        for card in cards:
            api.content.copy(source=card.getObject(), target=event.object)
