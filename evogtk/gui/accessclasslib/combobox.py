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
# combobox
# EVOGTK Access class for gtk.ComboBox
###############################################################################

# GTK Imports
import gtk

# DBWidgets imports
from evogtk.widgets import DBComboBox

class AccessClass:
    """
    Class for gtk.ComboBox
    """
        
    def supported_widgets(self):
        """
        Supported widgets for this access class
        """
        return [gtk.ComboBox,DBComboBox,]
    
    def supported_types(self):
        """
        Supported types for this access class
        """
        return [str]
    
    def set_content(self,widget,content):
        """
        Method for setting the widget content
        """
        widget.set_active_iter(widget.get_model().get_iter_from_string(content))
    
    def get_content(self,widget):
        """
        Method for getting the widget content
        """
        return widget.get_model().get_string_from_iter(widget.get_active_iter())
