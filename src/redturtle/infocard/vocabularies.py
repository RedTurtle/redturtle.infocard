# -*- coding: utf-8 -*-
from Acquisition import aq_chain
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from redturtle.infocard.content.infocard_container import InfocardContainer
from zope.component import getUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


@implementer(IVocabularyFactory)
class InfocardContainerServiceTypesVocabulary(object):
    def __call__(self, context=None):
        normalizer = getUtility(IIDNormalizer)
        for value in aq_chain(context):
            if isinstance(value, InfocardContainer):
                terms = [
                    SimpleTerm(
                        value=normalizer.normalize(x.strip()),
                        token=normalizer.normalize(x.strip()),
                        title=x.strip(),
                    )
                    for x in value.servicetypes
                    if x.strip()
                ]
                return SimpleVocabulary(terms)
        return SimpleVocabulary([])


InfocardContainerServiceTypesFactory = (
    InfocardContainerServiceTypesVocabulary()
)


@implementer(IVocabularyFactory)
class InfocardContainerRecipientsVocabulary(object):
    def __call__(self, context=None):
        normalizer = getUtility(IIDNormalizer)
        for value in aq_chain(context):
            if isinstance(value, InfocardContainer):
                terms = [
                    SimpleTerm(
                        value=normalizer.normalize(x.strip()),
                        token=normalizer.normalize(x.strip()),
                        title=x.strip(),
                    )
                    for x in value.recipients
                    if x.strip()
                ]
                return SimpleVocabulary(terms)
        return SimpleVocabulary([])


InfocardContainerRecipientsFactory = InfocardContainerRecipientsVocabulary()


@implementer(IVocabularyFactory)
class InfoCardContainerVocabulary(object):
    def __call__(self, context=None):
        infocardcontainer_list = api.content.find(
            portal_type="InfocardContainer"
        )

        infocardcontainer_list = [
            x.getObject() for x in infocardcontainer_list
        ]

        terms = [
            SimpleTerm(value=x.UID(), token=x.UID(), title=x.title)
            for x in infocardcontainer_list
        ]

        return SimpleVocabulary(terms)


InfoCardContainerVocabularyFactory = InfoCardContainerVocabulary()
