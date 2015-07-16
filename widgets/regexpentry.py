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
# regexpentry
# EVOGTK Regular Expression gtk.Entry widget
###############################################################################

# Python Imports
import re

# GTK Imports
import gobject,gtk

class RegExpEntry(gtk.Entry):
    """
    Sourceview enhanced widget class
    """
    __gtype_name__ = 'RegExpEntry'
    __properties = {
        'regular-expression' : (gobject.TYPE_STRING,'Regular Expression','Regular expression to math widget contents','',gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
        'match-error-text' : (gobject.TYPE_STRING,'Match error text','Message displayed when data doesn\' matches regular expression','Invalid data',gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
        'match-error-description' : (gobject.TYPE_STRING,'Match error description','Description displayed when data doesn\' matches regular expression','Data doesn\'t matchs regular expression',gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
        'show-regexp-expression': (gobject.TYPE_BOOLEAN,'Show regular expression description','Show regular expression in description of match error dialog',True,gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
    }
    __gproperties__ = __properties

    def __init__(self,regexp=''):
        """
        Initialization
        """        
        # Initialize parent class
        gtk.Entry.__init__(self)
        # Initialize properties
        self.regular_expression=regexp
        self.__regexp=re.compile(regexp)
        self.match_error_text='Invalid data'
        self.match_error_description='Data doesn\'t matchs regular expression'
        self.show_regexp_expression=True
        # Initialize regular expression match
        self.__regexp_match=None
        # Connect signals to validate regular expression
        self.connect('activate',self.__validate_regexp)
        self.connect('focus-out-event',self.__validate_regexp)

    def __validate_regexp(self,widget=None,event=None):
        """
        Parses contents in gtk.Entry to match regular expression when activated or if widget loses focus
        """
        if self.get_text():
            self.__regexp_match=self.__regexp.search(self.get_text())
            if not self.__regexp_match:
                self.set_text('')
                gobject.timeout_add(0,self.__invalid_match,priority=gobject.PRIORITY_HIGH)

    def __invalid_match(self):
        """
        Shows a dialog to state that we introduced an invalid date format
        """
        dialog=gtk.MessageDialog(self.get_toplevel(),gtk.DIALOG_MODAL and gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE)
        dialog.set_markup('<b>%s</b>' % gobject.markup_escape_text(self.match_error_text))
        if self.show_regexp_expression:
            dialog.format_secondary_markup('%s <b>%s</b>' % (self.match_error_description,self.regular_expression))
        else:
            dialog.format_secondary_markup(self.match_error_description)
        dialog.run()
        dialog.destroy()

    def get_group(self,group):
        self.__validate_regexp()
        if self.__regexp_match:
            if self.__regexp_match.groupdict().has_key(group):
                return self.__regexp_match.group(group)
            else:
                raise Exception('(EVOGTK - %s) There is no group named %s' % (self.__gtype_name__,group))
        else:
            return None

    def do_get_property(self, property):
        """
        Property getting value handling
        """
        if property.name=='regular-expression':
            return self.regular_expression
        elif property.name=='match-error-text':
            return self.match_error_text
        elif property.name=='match-error-description':
            return self.match_error_description
        elif property.name=='show-regexp-expression':
            return self.show_regexp_expression

    def do_set_property(self, property, value):
        """
        Property setting value handling
        """
        if property.name=='regular-expression':
            self.regular_expression=value
            self.__regexp=re.compile(value)
        elif property.name=='match-error-text':
            self.match_error_text=value
        elif property.name=='match-error-description':
            self.match_error_description=value
        elif property.name=='show-regexp-expression':
            self.show_regexp_expression=value
            
gobject.type_register(RegExpEntry)