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
# datepicker
# EVOGTK date picker widget
###############################################################################

# Python Imports
import sys
from datetime import datetime

# GTK Imports
import gobject,gtk

# Import default date format
if sys.platform!='win32':
    import locale
    LOCALE_DATE_FORMAT=locale.nl_langinfo(locale.D_FMT)
else:
    LOCALE_DATE_FORMAT='%Y-%m-%d'

class DatePicker(gtk.Entry):
    """
    Sourceview enhanced widget class
    """
    __gtype_name__ = 'DatePicker'
    __properties = {
        'date-format' : (gobject.TYPE_STRING,'Date Format','Date format for this DatePicker',LOCALE_DATE_FORMAT,gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
    }
    __gproperties__ = __properties

    def __init__(self,date_format=LOCALE_DATE_FORMAT):
        """
        Initialization
        """        
        # Initialize parent class
        gtk.Entry.__init__(self)
        # Initialize date format
        self.date_format=date_format
        # Initialize Calendar popup window for date picker
        self.__calendar_window=gtk.Window(type=gtk.WINDOW_POPUP)
        self.__calendar_window.set_decorated(False)
        self.__calendar_window.set_resizable(False)
        self.__calendar_window.set_keep_above(True)
        # self.__calendar_window.set_size_request(250,200)
        # Initialize calendar widget
        self.__calendar=gtk.Calendar()
        self.__calendar_window.add(self.__calendar)
        self.set_property('primary-icon-activatable',True)     
        self.set_property('primary-icon-sensitive',True)
        self.set_property('primary-icon-stock',gtk.STOCK_INDEX)        
        # Connect signals to show/hide calendar and date entry
        self.connect('activate',self.__validate_date_format)
        self.connect('icon-press',self.__popup_calendar)
        self.connect('focus-out-event',self.__validate_date_format)
        self.__calendar.connect('day-selected-double-click',self.__popdown_calendar)
        # Connect signals for setting date in gtk.Entry
        self.__calendar.connect('day-selected',self.__sync_calendar_date)
        self.__calendar.connect('month-changed',self.__sync_calendar_date)

    def __sync_calendar_date(self,widget=None,event=None):
        """
        Detect changes in gtk.Calendar and sets date in gtk.Entry
        """
        self.set_text(self.get_date_string())

    def __validate_date_format(self,widget=None,event=None):
        """
        Parses date in gtk.Entry to set it on gtk.Calendar and hides calendar popup if widget loses focus
        """
        self.__calendar_window.hide()
        try:
            date=datetime.strptime(self.get_text(),self.date_format)
            self.set_datetime(date)
        except:
            gobject.timeout_add(0,self.__invalid_date_dialog,priority=gobject.PRIORITY_HIGH)

    def __invalid_date_dialog(self):
        """
        Shows a dialog to state that we introduced an invalid date format
        """
        dialog=gtk.MessageDialog(self.get_toplevel(),gtk.DIALOG_MODAL and gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE)
        dialog.set_markup('<b>Date format error</b>')
        dialog.format_secondary_markup('Specified date is not valid')
        self.__sync_calendar_date()
        dialog.run()
        dialog.destroy()

    def __popup_calendar(self,widget=None,icon=None,event=None):
        """
        Shows calendar
        """
        if icon==gtk.ENTRY_ICON_PRIMARY:
            posx,posy=self.get_toplevel().get_position()
            alloc=self.get_allocation()
            x=int(posx+alloc.x+event.x)
            y=int(posy+alloc.y+event.y)
            self.__calendar_window.move(x,y)
            self.grab_focus()
            self.__calendar_window.show_all()

    def __popdown_calendar(self,widget=None,event=None):
        """
        Hides calendar
        """
        self.__calendar_window.hide()
        if widget==self.__calendar:
            self.set_text(self.get_date_string())
        return True

    def get_year(self):
        """
        Returns year of date
        """
        return self.__calendar.get_date()[0]
    
    def get_month(self):
        """
        Returns month of date
        """
        return self.__calendar.get_date()[1]+1
    
    def get_day(self):
        """
        Return day of date
        """
        return self.__calendar.get_date()[2]

    def set_datetime(self,date):
        """
        Set date
        """
        self.__calendar.select_month(date.month-1,date.year)
        self.__calendar.select_day(date.day)

    def get_datetime(self):
        """
        Returns datetime object with selected date
        """
        return datetime(self.get_year(),self.get_month(),self.get_day())
        
    def get_date_string(self,format=None):
        """
        Returns date in string format
        """
        if not format:
            format=self.date_format
        return self.get_datetime().strftime(format)

    def get_date(self):
        """
        Wrapper for gtk.Calendar.get_date method
        """
        return self.__calendar.get_date()

    def select_day(self,day):
        """
        Wrapper for gtk.Calendar.select_day method
        """
        return self.__calendar.select_day(day)

    def select_month(self,month,year):
        """
        Wrapper for gtk.Calendar.select_month method
        """
        return self.__calendar.select_month(month,year)

    def do_get_property(self, property):
        """
        Property getting value handling
        """
        if property.name=='date-format':
            return self.date_format

    def do_set_property(self, property, value):
        """
        Property setting value handling
        """
        if property.name=='date-format':
            self.date_format=value
            self.__sync_calendar_date()
            
gobject.type_register(DatePicker)