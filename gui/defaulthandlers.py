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
# defaulthandlers
# EVOGTK default handler functions for default handlers
###############################################################################

# Import GTK
import gtk

def gtk_widget_show(widget,*args):
    """
    Show widget default handler
    """
    widget.show()

def gtk_widget_hide(widget,*args):
    """
    Hide widget default handler
    """
    widget.hide()
    return True

def gtk_widget_grab_focus(widget,*args):
    """
    Grab focus default handler
    """
    widget.grab_focus()

def gtk_widget_destroy(widget,*args):
    """
    Destroy widget default handler
    """
    widget.destroy()

def gtk_true(*args):
    """
    GTK True default handler
    """
    return True

def gtk_false(*args):
    """
    GTK False default handler
    """
    return False

def gtk_main_quit(*args):
    """
    Quit main loop default handler
    """
    gtk.main_quit()