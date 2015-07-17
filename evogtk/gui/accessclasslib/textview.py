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
# textview
# EVOGTK Access class for gtk.TextView widgets
###############################################################################

# GTK Imports
import gtk

# EVOGTK Imports
import evogtk

class AccessClass:
    """
    Class for gtk.TextView widgets access
    """
    def supported_widgets(self):
        """
        Supported widgets for this access class
        """
        if evogtk.HAS_GTKSOURCEVIEW:
            import gtksourceview2
            return [gtk.TextView,gtksourceview2.View]
        return [gtk.TextView,]

    def supported_types(self):
        """
        Supported types for this access class
        """
        return [str]

    def set_content(self,widget,content):
        """
        Method for setting the widget content
        """
        buffer=widget.get_buffer()
        buffer.set_text(str(content))
    
    def get_content(self,widget):
        """
        Method for setting the widget content
        """
        buffer=widget.get_buffer()
        start=buffer.get_start_iter()
        end=buffer.get_end_iter()
        return str(buffer.get_text(start,end))
        