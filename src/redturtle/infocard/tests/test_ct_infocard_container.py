# -*- coding: utf-8 -*-
from redturtle.infocard.content.infocard_container import IInfocardContainer  # NOQA E501
from redturtle.infocard.testing import RT_INFOCARD_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class InfocardContainerIntegrationTest(unittest.TestCase):

    layer = RT_INFOCARD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_ct_infocard_container_schema(self):
        fti = queryUtility(IDexterityFTI, name='InfocardContainer')
        schema = fti.lookupSchema()
        self.assertEqual(IInfocardContainer, schema)

    def test_ct_infocard_container_fti(self):
        fti = queryUtility(IDexterityFTI, name='InfocardContainer')
        self.assertTrue(fti)

    def test_ct_infocard_container_factory(self):
        fti = queryUtility(IDexterityFTI, name='InfocardContainer')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IInfocardContainer.providedBy(obj),
            u'IInfocardContainer not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_infocard_container_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='InfocardContainer',
            id='infocard_container',
        )

        self.assertTrue(
            IInfocardContainer.providedBy(obj),
            u'IInfocardContainer not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_infocard_container_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='InfocardContainer')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_infocard_container_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='InfocardContainer')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'infocard_container_id',
            title='InfocardContainer container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
