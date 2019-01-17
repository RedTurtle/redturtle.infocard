# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s redturtle.infocard -t test_card.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src redturtle.infocard.testing.RT_INFOCARD_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/rt/infocard/tests/robot/test_card.robot
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

Scenario: As a site administrator I can add a Card
  Given a logged-in site administrator
    and an add Infocard form
   When I type 'My Card' into the title field
    and I submit the form
   Then a Card with the title 'My Card' has been created

Scenario: As a site administrator I can view a Card
  Given a logged-in site administrator
    and a Card 'My Card'
   When I go to the Card view
   Then I can see the Card title 'My Card'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Infocard form
  Go To  ${PLONE_URL}/++add++Infocard

a Card 'My Card'
  Create content  type=Infocard  id=my-card  title=My Card

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Card view
  Go To  ${PLONE_URL}/my-card
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Card with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Card title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
