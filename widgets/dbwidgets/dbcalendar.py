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
# dbcalendar
# Database gtk.Calendar widget module
###############################################################################

# Python imports
from datetime import datetime

# GTK Imports
import gobject, gtk

# DBWidget base class
from dbwidgetbase import DBWidgetBase

class DBCalendar(gtk.Calendar,DBWidgetBase):
    """
    Database gtk.Calendar widget
    """
    __gtype_name__ = 'DBCalendar'
    __gproperties__=DBWidgetBase._DBWidgetBase__properties
    
    def __init__(self,*args,**kwargs):
        """
        Class initialization
        """
        # Initialize DBWidget base class
        DBWidgetBase.__init__(self,*args,**kwargs)
        # Initialize calendar widget
        gtk.Calendar.__init__(self)
        # Widget properties
        if self.inmediate_validation:
            self.connect('day-selected',self.validate)
            self.connect('day-selected-double-click',self.validate)
            self.connect('month-changed',self.validate)
        self.__default_bg_color=self.get_style().bg[0]
        self.__error_bg_color=gtk.gdk.color_parse('red')

    def set_invalidated(self):
        """
        Set this widget as invalidated
        """
        self.modify_bg(gtk.STATE_NORMAL,self.__error_bg_color)        

    def set_validated(self):
        """
        Set this widget as validated
        """
        self.modify_bg(gtk.STATE_NORMAL,self.__default_bg_color)

    def get_widget_data(self):
        """
        Returns widget data
        """
        date=self.get_date()
        return datetime(date[0],date[1]+1,date[2])
        
gobject.type_register(DBCalendar)