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
# calendar
# EVOGTK Access class for gtk.Calendar like widgets
###############################################################################

# Python imports
from datetime import date

# GTK Imports
import gtk

# EVOGTK Widgets imports
from evogtk.widgets import DatePicker

# DBWidgets imports
from evogtk.widgets import DBCalendar
from evogtk.widgets import DBDatePicker

class AccessClass:
    """
    Class for gtk.Calendar like widgets access
    """
    def supported_widgets(self):
        """
        Supported widgets for this access class
        """
        return [gtk.Calendar,DatePicker,DBCalendar,DBDatePicker]

    def supported_types(self):
        """
        Supported types for this access class
        """
        return []

    def set_content(self,widget,content):
        """
        Method for setting the widget content
        """
        widget.select_month(content.month-1,content.year)
        widget.select_day(content.day)
    
    def get_content(self,widget):
        """
        Method for setting the widget content
        """
        seldate=widget.get_date()
        return date(seldate[0],seldate[1]+1,seldate[2])
        
