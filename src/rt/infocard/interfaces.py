# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.app.textfield import RichText
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives
from plone.supermodel import model
from rt.infocard import _
from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IRtInfocardLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICard(model.Schema):
    """ Marker interface for Card
    """


class IInfocardContainer(model.Schema):
    """ Marker interface and Dexterity Python Schema for InfocardContainer
    """

    introduction = RichText(title=_(u"Introduction"), required=True)

    servicetypes = schema.List(
        title=_("label_available_servicetypes", u"Available service types"),
        description=_(
            "help_available_servicetypes",
            (
                u"Insert one service type per line. "
                u"They will be proposed "
                u"in the service type field of the infocards"
            ),
        ),
        value_type=schema.TextLine(title=_(u"service_type", "Service type")),
        default=[],
        required=True,
    )

    recipients = schema.List(
        title=_("label_available_recipients", u"Available recipients"),
        description=_(
            "help_available_recipients",
            (
                u"Insert one recipient per line. "
                u"They will be proposed "
                u"in the recipient field of the infocards"
            ),
        ),
        value_type=schema.TextLine(title=_(u"recipient", "Recipient")),
        default=[],
        required=True,
    )


class IInfocard(model.Schema):
    """ Marker interface and Dexterity Python Schema for Infocard
    """

    servicetypes = schema.Tuple(
        title=_(
            'label_servicetypes',
            u"Service types"
        ),
        value_type=schema.TextLine(),
        required=True,
        missing_value=None,
    )
    directives.widget(
        'servicetypes',
        AjaxSelectFieldWidget,
        vocabulary='rt.infocard.infocardcontainer.servicetypes'
    )

    recipients = schema.Tuple(
        title=_(
            'label_recipients',
            u"Recipients"
        ),
        value_type=schema.TextLine(),
        required=True,
        missing_value=None,
    )
    directives.widget(
        'recipients',
        AjaxSelectFieldWidget,
        vocabulary='rt.infocard.infocardcontainer.recipients'
    )
