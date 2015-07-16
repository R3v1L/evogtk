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
# fontcombo
# EVOGTK Access class for EVOGTK FontCombo like widgets
###############################################################################

# GTK imports
import gtk

# EVOGTK Widgets imports
from evogtk.widgets.fontcombo import FontCombo

class AccessClass:
    """
    Class for EVOGTK FontCombo like widgets access
    """
    def supported_widgets(self):
        """
        Supported widgets for this access class
        """
        return [FontCombo,gtk.FontButton,gtk.FontSelection,gtk.FontSelectionDialog]

    def supported_types(self):
        """
        Supported types for this access class
        """
        return [str]

    def set_content(self,widget,content):
        """
        Method for setting the widget content
        """
        widget.set_font_name(content)
    
    def get_content(self,widget):
        """
        Method for setting the widget content
        """
        return widget.get_font_name()
        