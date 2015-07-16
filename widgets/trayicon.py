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
# trayicon
# Tray Icon helper class
###############################################################################

# GTK Imports
import gobject
import gtk

class TrayIcon(gtk.StatusIcon):
    """
    Tray Icon widget class
    """
    
    __gtype_name__ = 'TrayIcon'
    
    def __init__(self,icon='pixmaps/icon.png',tooltip=None,menu=None,action=None,menucallback=None,visible=False):
        """
        Class constructor
        """
        # Parent class initialization
        super(gtk.StatusIcon,self).__init__()
        # Save menu for later use
        self.__menu=menu
        # Set icon image
        self.set_from_file(icon)
        # Set visibility
        self.set_visible(visible)
        # Set icon tooltip
        if tooltip:
            self.set_tooltip(tooltip)
        # Bind menu callback
        if action:
            self.connect('activate',action)
        if menu and not menucallback:
            self.connect('popup-menu',self.__default_menu_callback)
        elif menucallback:
            self.connect('popup-menu',menucallback)

    def __default_menu_callback(self,widget,button,timestamp):
        """
        Show status icon menu
        """
        if self.__menu.get_sensitive():
            self.__menu.popup(None,None,None,1,0)

    def __stop_blinking(self):
        """
        Stop blinking for tray icon
        """
        self.blink(False)
        return False

    def blink(self,status=True,duration=5000):
        """
        Set blinking status of tray icon
        """
        self.set_blinking(status)
        if status and duration:
            gobject.timeout_add(duration,self.__stop_blinking,priority=gobject.PRIORITY_HIGH)
        
    def show(self):
        """
        Shows tray icon
        """
        self.set_visible(True)
        
    def hide(self):
        """
        Hide tray icon
        """
        self.set_visible(False)

