# -*- coding: utf-8 -*-
from rt.infocard.content.card import ICard  # NOQA E501
from rt.infocard.testing import RT_INFOCARD_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class CardIntegrationTest(unittest.TestCase):

    layer = RT_INFOCARD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Infocard',
            self.portal,
            'card',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_card_schema(self):
        fti = queryUtility(IDexterityFTI, name='Card')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('Card')
        self.assertEqual(schema_name, schema.getName())

    def test_ct_card_fti(self):
        fti = queryUtility(IDexterityFTI, name='Card')
        self.assertTrue(fti)

    def test_ct_card_factory(self):
        fti = queryUtility(IDexterityFTI, name='Card')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ICard.providedBy(obj),
            u'ICard not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_card_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Card',
            id='card',
        )

        self.assertTrue(
            ICard.providedBy(obj),
            u'ICard not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_card_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Card')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )
