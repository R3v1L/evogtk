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
# guiwidgets
# GUI Widgets helper class
###############################################################################

# Container class for widgets coming from GUI
class GUIWidgets(object):
    """
    Container class for storing widgets from GUI data
    """
    def __init__(self,guidata):
        """
        Class constructor
        """
        self.__guidata=guidata
        self.__addedwidgets={}
        self.__initialised=True
        
    def __getattr__(self,name):
        """
        Get attribute method overload for accessing widgets
        """
        if not name in self.__dict__:
            if not name in self.__addedwidgets:
                return self.__guidata.get_object(name)
            else:
                return self.__addedwidgets[name]
        else:
            return self.__dict__[name]

    def __setattr__(self,name,value):
        """
        Set attribute method overload for accessing widgets
        """
        # Assignment in initialisation
        if not self.__dict__.has_key('_GUIWidgets__initialised'):
            self.__dict__[name]=value
            return self.__dict__[name]
        # Assignment after initialisation
        raise Exception('(EVOGTK - GUI Widgets) Trying to set a widget into protected widget container')

    def widget_exists(self,name):
        """
        Check if a widget exists
        """
        return (name in self.__addedwidgets) or (self.__guidata.get_object(name) != None)

    def get_widget_list(self):
        """
        Returns a list with all loaded widgets
        """
        return self.__guidata.get_objects() + self.__addedwidgets.values()

    def add_widget(self,widget,name=None):
        """
        Add a widget to this widget container
        """
        if not name:
            name=widget.get_name()
        self.__addedwidgets[name]=widget
        return widget

    def get_widget(self,name):
        """
        Returns the specified widget
        """
        if name in self.__addedwidgets:
            return self.__addedwidgets[name]
        else:
            return self.__guidata.get_object(name)
    
    def get_toplevels(self):
        """
        Returns a list with all toplevel widgets
        """
        toplevels=[]
        for widget in self.get_widget_list():
            try:
                if widget.get_toplevel() not in toplevels:
                    toplevels.append(widget)
            except:
                pass
        return toplevels
    
    def disable_toplevels(self):
        """
        Disables all toplevel windows
        """
        for widget in self.get_toplevels():
            widget.set_sensitive(False)

    def enable_toplevels(self):
        """
        Disables all toplevel windows
        """
        for widget in self.get_toplevels():
            widget.set_sensitive(True)
