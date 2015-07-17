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
# dbcheckbutton
# Database gtk.CheckButton widget module
###############################################################################

# GTK Imports
import gobject, gtk

# DBWidget base class
from dbwidgetbase import DBWidgetBase

class DBCheckButton(gtk.CheckButton,DBWidgetBase):
    """
    Database gtk.CheckButton widget
    """
    __gtype_name__ = 'DBCheckButton'
    __gproperties__=DBWidgetBase._DBWidgetBase__properties
    
    def __init__(self,*args,**kwargs):
        """
        Class initialization
        """
        # Initialize DBWidget base class
        DBWidgetBase.__init__(self,*args,**kwargs)
        # Initialize parent widget
        gtk.CheckButton.__init__(self)
        # Error image
        self.__errorimg=gtk.Image()
        self.__errorimg. set_from_stock(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_MENU)
        self.__errorimg.show()
        # Widget properties
        self.set_property('image-position',gtk.POS_RIGHT)
        if self.inmediate_validation:
            self.connect('toggled',self.validate)

    def get_widget_data(self):
        """
        Returns widget data
        """
        return self.get_active()

    def set_invalidated(self):
        """
        Set this widget as invalidated
        """
        # GTK Settings for evogtk
        self.set_property('image',self.__errorimg)

    def set_validated(self):
        """
        Set this widget as validated
        """
        self.__validationerrors=[]
        self.set_property('image',None)

gobject.type_register(DBCheckButton)