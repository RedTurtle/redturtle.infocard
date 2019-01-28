# -*- coding: utf-8 -*-
from plone import api
from plone.tiles import Tile
from redturtle.infocard.vocabularies import (
    InfocardContainerServiceTypesFactory,
    InfocardContainerRecipientsFactory,
)
from redturtle.infocard import logger


class SearchTile(Tile):
    def available(self):
        """
        The portlet will be available if the target is visible
        """
        return bool(
            self.target and "View" in api.user.get_permissions(obj=self.target)
        )

    @property
    def target(self):
        """ Get's the object related to the target
        """
        try:
            return api.content.get(UID=self.data["target"])
        except Exception:
            msg = "Unable to find target: %s" % self.data["target"]
            logger.exception(msg)

    @property
    def display_title(self):
        """ Check out the configuration to see if we can display title
        """
        return self.data["display_title"]

    @property
    def get_url(self):
        return api.content.get(UID=self.data["target"]).absolute_url()

    @property
    def text_before(self):
        """ Display text before search fields
        """
        return (
            self.data["text_before"].raw if self.data["text_before"] else u""
        )

    @property
    def text_after(self):
        """ Display text after search fields
        """
        return self.data["text_after"].raw if self.data["text_after"] else u""

    @property
    def display_filters(self):
        """ Check out the configuration to see if we can display additional
        checkboxes for filtering on recipents and service types
        """
        return self.data["display_filters"]

    @property
    def recipients(self):
        """ Get the recipient vocabulary for target
        """
        return InfocardContainerRecipientsFactory(self.target)

    @property
    def servicetypes(self):
        """ Get the recipient vocabulary for target
        """
        return InfocardContainerServiceTypesFactory(self.target)
