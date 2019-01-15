# -*- coding: utf-8 -*-
from Acquisition import aq_chain
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

InfocardContainerServiceTypesFactory = InfocardContainerServiceTypesVocabulary() # noqa


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

InfocardContainerRecipientsFactory = InfocardContainerRecipientsVocabulary() # noqa
