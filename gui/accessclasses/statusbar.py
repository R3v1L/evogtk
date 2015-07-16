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
# statusbar
# EVOGTK Access class for gtk.Statusbar
###############################################################################

import gtk

class AccessClass:
    """
    Class for gtk.Statusbar
    """
    def supported_widgets(self):
        """
        Supported widgets for this access class
        """
        return [gtk.Statusbar,]

    def supported_types(self):
        """
        Supported types for this access class
        """
        return [str]

    def set_content(self,widget,content):
        """
        Method for setting the widget content
        """
        widget.push(widget.get_context_id(''),content)
    
    def get_content(self,widget):
        """
        Method for setting the widget content
        """
        return widget.pop(widget.get_context_id(''))
        