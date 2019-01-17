# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s redturtle.infocard -t test_default_card_container.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src redturtle.infocard.testing.REDTURTLE_INFOCARD_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/redturtle/infocard/tests/robot/test_default_card_container.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a DefaultCardContainer
  Given a logged-in site administrator
    and an add InfocardContainer form
   When I type 'My DefaultCardContainer' into the title field
    and I submit the form
   Then a DefaultCardContainer with the title 'My DefaultCardContainer' has been created

Scenario: As a site administrator I can view a DefaultCardContainer
  Given a logged-in site administrator
    and a DefaultCardContainer 'My DefaultCardContainer'
   When I go to the DefaultCardContainer view
   Then I can see the DefaultCardContainer title 'My DefaultCardContainer'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add InfocardContainer form
  Go To  ${PLONE_URL}/++add++InfocardContainer

a DefaultCardContainer 'My DefaultCardContainer'
  Create content  type=InfocardContainer  id=my-default_card_container  title=My DefaultCardContainer

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the DefaultCardContainer view
  Go To  ${PLONE_URL}/my-default_card_container
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a DefaultCardContainer with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the DefaultCardContainer title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
