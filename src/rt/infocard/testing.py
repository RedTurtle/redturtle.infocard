# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import rt.infocard


class RtInfocardLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=rt.infocard)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'rt.infocard:default')


RT_INFOCARD_FIXTURE = RtInfocardLayer()


RT_INFOCARD_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RT_INFOCARD_FIXTURE,),
    name='RtInfocardLayer:IntegrationTesting',
)


RT_INFOCARD_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(RT_INFOCARD_FIXTURE,),
    name='RtInfocardLayer:FunctionalTesting',
)


RT_INFOCARD_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        RT_INFOCARD_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='RtInfocardLayer:AcceptanceTesting',
)
