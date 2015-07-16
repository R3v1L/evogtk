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
# shortcuts
# Shortcuts helper class
###############################################################################
# TODO: evogtk.gui.shortcuts: Add methods for deleting a shortcut, clear shortcuts for a widget or all, and disconnnect a widget

# GTK Imports
import gtk

class _ShortcutsHelper(object):
    """
    Shortcuts helper class
    """
    def __init__(self,gui_instance):
        """
        Class constructor
        """
        self.__gui_instance=gui_instance
        self.__shortcutlist={}
        self.__connected_widgets={}

    def __shortcuts_handler(self,widget,event):
        """
        Handles the shortcuts
        """
        # Check widget
        if self.__shortcutlist.has_key(widget):
            shift=bool(event.state & gtk.gdk.SHIFT_MASK)
            ctrl=bool(event.state & gtk.gdk.CONTROL_MASK)
            alt=bool(event.state & gtk.gdk.MOD1_MASK)
            # Check shortcut
            if self.__shortcutlist[widget].has_key((event.keyval,shift,ctrl,alt)):
                callback,task_list,pass_shortcut,user_params=self.__shortcutlist[widget][(event.keyval,shift,ctrl,alt)]
                # Check task list
                if not task_list or (self.__gui_instance.get_gui_task() in task_list):
                    # Check if we have to pass any params to callback and call it
                    if pass_shortcut:
                        return self.__shortcutlist[widget][(event.keyval,shift,ctrl,alt)][0](widget,event,(event.keyval,shift,ctrl,alt,task_list),**user_params)
                    else:
                        return self.__shortcutlist[widget][(event.keyval,shift,ctrl,alt)][0](widget,event,**user_params)

    def bind_shortcut(self,widget,callback,key,shift=False,ctrl=False,alt=False,task_list=None,pass_shortcut=True,**user_params):
        """
        Binds a shortcut to a given widget
        """
        # Create widget shortcut dict
        if not self.__shortcutlist.has_key(widget):
            self.__shortcutlist[widget]={}
        # Connect window key-press-event to shortcuts handler
        if not self.__connected_widgets.has_key(widget):
            self.__connected_widgets[widget]=widget.connect('key-press-event',self.__shortcuts_handler)
        # Add shortcut to widget
        self.__shortcutlist[widget][(key,shift,ctrl,alt)]=(callback,task_list,pass_shortcut,user_params)
