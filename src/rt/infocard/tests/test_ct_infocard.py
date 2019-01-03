# -*- coding: utf-8 -*-
from rt.infocard.content.infocard import IInfocard  # NOQA E501
from rt.infocard.testing import RT_INFOCARD_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class InfocardIntegrationTest(unittest.TestCase):

    layer = RT_INFOCARD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'InfocardContainer',
            self.portal,
            'infocard',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_infocard_schema(self):
        fti = queryUtility(IDexterityFTI, name='Infocard')
        schema = fti.lookupSchema()
        self.assertEqual(IInfocard, schema)

    def test_ct_infocard_fti(self):
        fti = queryUtility(IDexterityFTI, name='Infocard')
        self.assertTrue(fti)

    def test_ct_infocard_factory(self):
        fti = queryUtility(IDexterityFTI, name='Infocard')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IInfocard.providedBy(obj),
            u'IInfocard not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_infocard_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Infocard',
            id='infocard',
        )

        self.assertTrue(
            IInfocard.providedBy(obj),
            u'IInfocard not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_infocard_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Infocard')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )

    def test_ct_infocard_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Infocard')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'infocard_id',
            title='Infocard container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
