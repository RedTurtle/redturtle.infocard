# -*- coding: utf-8 -*-
from redturtle.infocard.content.default_card_container import IDefaultCardContainer  # NOQA E501
from redturtle.infocard.testing import REDTURTLE_INFOCARD_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class DefaultCardContainerIntegrationTest(unittest.TestCase):

    layer = REDTURTLE_INFOCARD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'InfocardContainer',
            self.portal,
            'default_card_container',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_default_card_container_schema(self):
        fti = queryUtility(IDexterityFTI, name='DefaultCardContainer')
        schema = fti.lookupSchema()
        self.assertEqual(IDefaultCardContainer, schema)

    def test_ct_default_card_container_fti(self):
        fti = queryUtility(IDexterityFTI, name='DefaultCardContainer')
        self.assertTrue(fti)

    def test_ct_default_card_container_factory(self):
        fti = queryUtility(IDexterityFTI, name='DefaultCardContainer')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IDefaultCardContainer.providedBy(obj),
            u'IDefaultCardContainer not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_default_card_container_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='DefaultCardContainer',
            id='default_card_container',
        )

        self.assertTrue(
            IDefaultCardContainer.providedBy(obj),
            u'IDefaultCardContainer not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_default_card_container_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='DefaultCardContainer')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )

    def test_ct_default_card_container_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='DefaultCardContainer')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'default_card_container_id',
            title='DefaultCardContainer container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
