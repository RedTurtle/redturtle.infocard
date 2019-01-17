# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from redturtle.infocard.testing import RT_INFOCARD_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that redturtle.infocard is properly installed."""

    layer = RT_INFOCARD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if redturtle.infocard is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'redturtle.infocard'))

    def test_browserlayer(self):
        """Test that IRedturtleInfocardLayer is registered."""
        from redturtle.infocard.interfaces import (
            IRedturtleInfocardLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IRedturtleInfocardLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = RT_INFOCARD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['redturtle.infocard'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if redturtle.infocard is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'redturtle.infocard'))

    def test_browserlayer_removed(self):
        """Test that IRedturtleInfocardLayer is removed."""
        from redturtle.infocard.interfaces import \
            IRedturtleInfocardLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IRedturtleInfocardLayer,
            utils.registered_layers())
