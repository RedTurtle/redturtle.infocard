# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.portlets.interfaces import IPortletDataProvider
from redturtle.infocard import _
from zope import schema


class IInfocardSearchPortlet(IPortletDataProvider):

    """A portlet that allows searching in an infocard container
    """
    name = schema.TextLine(
        title=_(u"name", default=u"Portlet name"),
        default=u'Infocard search portlet',
        required=False,
    )

    display_title = schema.Bool(
        title=_(u"label_display_title", default=u"Display title"),
        description=_(
            u"help_display_title",
            u"If checked the portlet will display a title based on name"
        ),
        default=True,
        required=True,
    )

    target = schema.Choice(
        title=_(u"Target infocard container"),
        description=_(
            "help_target",
            u"Choose the infocard container in which you can search"
        ),
        vocabulary='redturtle.infocard.infocartcontainer.vocabulary',
        required=True
    )

    display_filters = schema.Bool(
        title=_('label_display_filters', u"Display filters"),
        description=_(
            "help_display_filters",
            u'By default the portlet displays one input '
            u'to search on infocard text. '
            u'If you select this checkbox two additional selects will appear. '
            u'They will allow to search in the fields '
            u'"Service type" and "Recipient".'
        ),
        default=False,
    )

    text_before = RichText(
        title=_(u"Text before search fields"),
        description=_(u"This text will appear before the search fields"),
        required=False
    )

    text_after = RichText(
        title=_(u"Text after search fields"),
        description=_(u"This text will appear after the search fields"),
        required=False
    )
