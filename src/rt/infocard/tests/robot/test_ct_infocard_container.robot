# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s rt.infocard -t test_infocard_container.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src rt.infocard.testing.RT_INFOCARD_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/rt/infocard/tests/robot/test_infocard_container.robot
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

Scenario: As a site administrator I can add a InfocardContainer
  Given a logged-in site administrator
    and an add InfocardContainer form
   When I type 'My InfocardContainer' into the title field
    and I submit the form
   Then a InfocardContainer with the title 'My InfocardContainer' has been created

Scenario: As a site administrator I can view a InfocardContainer
  Given a logged-in site administrator
    and a InfocardContainer 'My InfocardContainer'
   When I go to the InfocardContainer view
   Then I can see the InfocardContainer title 'My InfocardContainer'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add InfocardContainer form
  Go To  ${PLONE_URL}/++add++InfocardContainer

a InfocardContainer 'My InfocardContainer'
  Create content  type=InfocardContainer  id=my-infocard_container  title=My InfocardContainer

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the InfocardContainer view
  Go To  ${PLONE_URL}/my-infocard_container
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a InfocardContainer with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the InfocardContainer title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
