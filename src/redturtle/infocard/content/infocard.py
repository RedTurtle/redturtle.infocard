# -*- coding: utf-8 -*-
from plone import api
from plone.app.textfield.interfaces import ITransformer
from plone.dexterity.content import Container
from redturtle.infocard.interfaces import IInfocard
from zope.interface import implementer


@implementer(IInfocard)
class Infocard(Container):
    """
    """

    _order = []

    def updateCards(self):
        ul = filter(lambda x: self.is_present(x), self.getCards())
        self.order = ul

    def getCards(self):
        infocard = api.content.get(UID=self.UID())

        cards_list = []
        cards_list.extend(
            api.content.find(context=infocard, portal_type="Card")
        )
        cards_list.extend(
            api.content.find(context=infocard.default, portal_type="Card")
        )
        cards_list = [x.getObject() for x in cards_list]
        return [{"publish": True, "uid_card": x.UID()} for x in cards_list]

    def is_present(self, x):
        for el in self._order:
            if el["uid_card"] == x["uid_card"]:
                return False
        return True

    @property
    def order(self):
        ul = []
        ul = self._order + filter(
            lambda x: self.is_present(x), self.getCards()
        )
        for card in ul:
            if not card.get("title_card", None):
                obj = api.content.get(UID=card["uid_card"])
                if obj:
                    card["title_card"] = obj.title
        return ul

    @order.setter
    def order(self, val):
        self._order = val

    def searched_text(self):
        """ The text searched
        """
        parts = [self.title, self.description]
        transformer = ITransformer(self)

        infocard_view = api.content.get_view(
            "infocard_view", self, self.REQUEST
        )
        for x in infocard_view.allowed_infos:
            card = None
            if x.get("uid_card"):
                card = api.content.get(UID=x["uid_card"])
            if card and card.text:
                if isinstance(card.text, unicode):
                    parts.append(card.text)
                else:
                    parts.append(transformer(card.text, "text/plain"))

        return u" ".join(set(u" ".join(parts).lower().split()))
