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
# filechooser
# EVOGTK Access class for gtk.FileChooser and gtk.FileChooserButton widgets
###############################################################################

# GTK Imports
import gtk

class AccessClass:
    """
    Class for gtk.FileChooser and gtk.FileChooserButton widgets access
    """
    def supported_widgets(self):
        """
        Supported widgets for this access class
        """
        return [gtk.Image,]

    def supported_types(self):
        """
        Supported types for this access class
        """
        return [str,gtk.gdk.Pixbuf]

    def set_content(self,widget,content):
        """
        Method for setting the widget content
        """
        if type(content)==gtk.gdk.Pixbuf:
            widget.set_from_pixbuf(content)
        if type(content)==str:
            widget.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(content))

    def get_content(self,widget):
        """
        Method for setting the widget content
        """
        return widget.get_pixbuf()
