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
# checkbutton
# EVOGTK Access class for gtk.CheckButton like widgets
###############################################################################

# GTK Imports
import gtk

# DBWidgets imports
from evogtk.widgets.dbwidgets.dbcheckbutton import DBCheckButton

class AccessClass:
    """
    Class for gtk.CheckButton like widgets
    """
        
    def supported_widgets(self):
        """
        Supported widgets for this access class
        """
        return [gtk.CheckButton,gtk.ToggleButton,gtk.ToggleAction,gtk.ToggleToolButton,gtk.CheckMenuItem,gtk.ToggleAction,
                gtk.RadioButton,gtk.RadioAction,gtk.RadioMenuItem,gtk.RadioToolButton,
                DBCheckButton]

    def supported_types(self):
        """
        Supported types for this access class
        """
        return [bool]
    
    def set_content(self,widget,content):
        """
        Method for setting the widget content
        """
        widget.set_active(content)
    
    def get_content(self,widget):
        """
        Method for setting the widget content
        """
        return widget.get_active()