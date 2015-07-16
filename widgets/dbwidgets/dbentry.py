# -*- coding: utf-8 -*-
###############################################################################
# Copyright (C) 2008 EVO Sistemas Libres <central@evosistemas.com>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
###############################################################################
# dbentry
# Database gtk.Entry widget module
###############################################################################

# GTK Imports
import gobject, gtk

# DBWidget base class
from dbwidgetbase import DBWidgetBase

class DBEntry(gtk.Entry,DBWidgetBase):
    """
    Database gtk.Entry widget
    """
    __gtype_name__ = 'DBEntry'
    __gproperties__=DBWidgetBase._DBWidgetBase__properties

    def __init__(self):
        """
        Class initialization
        """
        # Initialize DBWidget base class
        DBWidgetBase.__init__(self)
        # Initialize Entry widget
        gtk.Entry.__init__(self)
        # Widget properties
        self.set_property('secondary-icon-sensitive',True)
        if self.inmediate_validation:
            self.connect('changed',self.validate)
        self.connect('activate',self.validate)

    def get_widget_data(self):
        """
        Returns widget data
        """
        return self.get_text()

    def set_invalidated(self):
        """
        Set this widget as invalidated
        """
        self.set_property('secondary-icon-stock',gtk.STOCK_DIALOG_ERROR)
        
    def set_validated(self):
        """
        Set this widget as validated
        """
        self.__validationerrors=[]
        self.set_property('secondary-icon-stock',None)

gobject.type_register(DBEntry)