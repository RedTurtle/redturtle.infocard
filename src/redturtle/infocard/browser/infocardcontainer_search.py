# -*- coding: utf-8 -*-
from plone import api
from plone.directives import form
from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from redturtle.infocard import _
from z3c.form import button
from zope import schema
from zope.interface import Invalid
from zope.interface import invariant
from redturtle.infocard.vocabularies import (
    InfocardContainerServiceTypesFactory,
    InfocardContainerRecipientsFactory,
)


class IInfocardContainerSearchForm(form.Schema):
    """ Define form fields """

    text = schema.TextLine(
        title=_("label_search_text", u"Search text"), required=False
    )
    servicetype = schema.Choice(
        title=_("label_servicetype", u"Service type"),
        vocabulary="redturtle.infocard.infocardcontainer.servicetypes",
        required=False,
    )
    recipient = schema.Choice(
        title=_("label_for_who_is_it", u"For who is it?"),
        vocabulary="redturtle.infocard.infocardcontainer.recipients",
        required=False,
    )

    @invariant
    def at_least_one(data):
        if data.servicetype or data.recipient or data.text:
            return
        raise Invalid(
            _(
                "label_at_least_one_search_parameter",
                u"You should specify at least one search parameter",
            )
        )


class InfocardContainerSearchForm(form.SchemaForm):

    ignoreContext = True
    schema = IInfocardContainerSearchForm
    searching = False

    table_fields = [
        {"id": "title", "label": _("title")},
        {"id": "description", "label": _("description")},
        {
            "id": "servicetypes",
            "label": _("label_servicetypes", u"Service types"),
        },
        {
            "id": "recipients",
            "label": _("label_for_who_is_it", u"For who is it?"),
        },
    ]

    def _init_(self, context, request):
        self.context = context
        self.request = request

    def accept_infocard(self, infocard, data):
        """ Given the data in the parameters filter the infocard
        """
        if data.get("servicetype"):
            voc = InfocardContainerServiceTypesFactory(self.context)
            if not voc.getTermByToken(data.get("servicetype")).title in infocard.servicetypes:
                return False
        if data.get("recipient"):
            voc = InfocardContainerRecipientsFactory(self.context)
            if not voc.getTermByToken(data.get("recipient")).title in infocard.recipients:
                return False
        if data.get("text"):
            if not data.get("text").lower() in infocard.searched_text():
                return False
        return True

    def search_results(self, data):
        """
        """
        infocards = self.context.listFolderContents(
            {"portal_type": "InformationCard"}
        )
        results = []
        for infocard in infocards:
            if self.accept_infocard(infocard, data):
                results.append(
                    {
                        "review_state": api.content.get_state(infocard),
                        "url": infocard.absolute_url,
                        "title": infocard.title,
                        "description": infocard.description,
                        "servicetypes": ", ".join(
                            sorted(infocard.servicetypes)
                        ),
                        "recipients": ", ".join(sorted(infocard.recipients)),
                    }
                )
        sorted(results, key=lambda x: x["title"])
        return results

    @button.buttonAndHandler(_("label_search", u"Search"))
    def handleSearch(self, action):
        self.searching = True
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            self.results = []
            return
        self.results = self.search_results(data)


infocardcontainersearchform_view = wrap_form(
    InfocardContainerSearchForm,
    index=ViewPageTemplateFile("templates/infocardcontainer_search.pt"),
)
