# -*- coding: utf-8 -*-
from redturtle.infocard import logger
from redturtle.infocard import _
from redturtle.infocard.vocabularies import (
    InfocardContainerServiceTypesFactory,
)
from redturtle.infocard.vocabularies import InfocardContainerRecipientsFactory
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from z3c.form import field
from zope.interface import implementer
from zope import schema
from plone.app.z3cform.widget import RichTextFieldWidget
from redturtle.infocard.portlets.interfaces import IInfocardSearchPortlet
from redturtle.infocard.vocabularies import (
    InfocardContainerServiceTypesFactory,
    InfocardContainerRecipientsFactory,
)


@implementer(IInfocardSearchPortlet)
class Assignment(base.Assignment):

    """Portlet assignment."""

    def __init__(
        self,
        name=u"",
        display_title=True,
        target=None,
        display_filters=False,
        text_before=u"",
        text_after=u"",
    ):
        self.name = name
        self.display_title = display_title
        self.target = target
        self.display_filters = display_filters
        self.text_before = text_before
        self.text_after = text_after

    @property
    def title(self):
        title = u"Infocard search"
        if self.data.name:
            title = u"%s: %s" % (title, self.data.name)
        return title


class AddForm(base.AddForm):
    label = _(u"Add Infocard search portlet")
    description = _(u"This portlet displays a search form.")
    schema = IInfocardSearchPortlet
    form_fields = field.Fields(schema)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    label = _(u"Edit Recent Portlet")
    description = _(u"This portlet displays a search form.")
    schema = IInfocardSearchPortlet
    form_fields = field.Fields(schema)


class Renderer(base.Renderer):

    """ Render he search form
    """

    render = ViewPageTemplateFile("search.pt")

    def available(self):
        """
        The portlet will be available if the target is visible
        """
        return bool(
            self.target and "View" in api.user.get_permissions(obj=self.target)
        )

    @property
    def target(self):
        """ Get's the object related to the target
        """
        try:
            return api.content.get(UID=self.data.target)
        except Exception:
            msg = "Unable to find target: %s" % self.data.target
            logger.exception(msg)

    @property
    def display_title(self):
        """ Check out the configuration to see if we can display title
        """
        return self.data.display_title

    @property
    def get_url(self):
        return api.content.get(UID=self.data.target).absolute_url()

    @property
    def text_before(self):
        """ Display text before search fields
        """
        return self.data.text_before

    @property
    def text_after(self):
        """ Display text after search fields
        """
        return self.data.text_after

    @property
    def display_filters(self):
        """ Check out the configuration to see if we can display additional
        checkboxes for filtering on recipents and service types
        """
        return self.data.display_filters

    @property
    def recipients(self):
        """ Get the recipient vocabulary for target
        """
        return InfocardContainerRecipientsFactory(self.target)

    @property
    def servicetypes(self):
        """ Get the recipient vocabulary for target
        """
        return InfocardContainerServiceTypesFactory(self.target)
