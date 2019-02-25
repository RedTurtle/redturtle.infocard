# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from Acquisition import aq_parent
from collective.z3cform.datagridfield.registry import DictRow
from plone import api
from plone.app.contenttypes.interfaces import IFolder
from plone.app.textfield import RichText
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives
from plone.supermodel import model
from redturtle.infocard import _
from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import provider
from zope.interface import Interface
from zope.schema.interfaces import IContextAwareDefaultFactory
from plone.directives import form
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory

from collective.z3cform.datagridfield.interfaces import AttributeNotFoundError
from collective.z3cform.datagridfield.interfaces import IRow
from z3c.form.interfaces import NO_VALUE
from zope.interface import implementer
from zope.schema import Field
from zope.schema import getFields
from zope.schema import Object
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import WrongContainedType


class IRedturtleInfocardLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICard(model.Schema):
    """ Marker interface for Card
    """


class ICardOrder(Interface):
    publish = schema.Bool(title=_(u"Publish"), required=True)
    title_card = schema.TextLine(title=_(u"Title card"), required=False)
    uid_card = schema.ASCIILine(title=_("Uid card"), required=False)


# @provider(IContextAwareDefaultFactory)
# def getInfoCardList(context):
#     # viene chiamata durante l'inserimento di una infocard
#
#     cards = api.content.find(context=context.default, portal_type="Card")
#     cards = [x.getObject() for x in cards]
#     return [
#         {"publish": True, "title_card": x.title, "uid_card": x.UID()}
#         for x in cards
#     ]


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


class IInfocard(Interface):
    """ Marker interface and Dexterity Python Schema for Infocard
    """

    servicetypes = schema.Tuple(
        title=_("label_servicetypes", u"Service types"),
        value_type=schema.TextLine(),
        required=True,
        missing_value=None,
    )
    directives.widget(
        "servicetypes",
        AjaxSelectFieldWidget,
        vocabulary="redturtle.infocard.infocardcontainer.servicetypes",
        pattern_options={"allowNewItems": False},
    )

    recipients = schema.Tuple(
        title=_("label_recipients", u"Recipients"),
        value_type=schema.TextLine(),
        required=True,
        missing_value=None,
    )
    directives.widget(
        "recipients",
        AjaxSelectFieldWidget,
        vocabulary="redturtle.infocard.infocardcontainer.recipients",
        pattern_options={"allowNewItems": False},
    )

    order = schema.List(
        title=_(u"Cards"),
        required=False,
        value_type=DictRow(title=u"Card", schema=ICardOrder),
        # defaultFactory=getInfoCardList,
        missing_value=[],
    )
    form.widget(order=DataGridFieldFactory)


class IDefaultCardContainer(IFolder):
    """ Marker interface and Dexterity Python Schema for DefaultCardContainer
    """
