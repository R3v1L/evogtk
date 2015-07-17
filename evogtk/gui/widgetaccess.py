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
# widgetaccess
# Widget access helper class
###############################################################################

# Import widget access shortcuts
import accessclasses

class WidgetAccess(object):
    """
    Class for widget content access
    """
    def __init__(self,widgets):
        """
        Class constructor
        """
        # GUI Widgets for getting and setting data
        self.__widgets=widgets
        # Dictionary for widget access mapping
        self.__accessmap={}
        # Search in access classes module path for widget accesss class definitions
        accessmodules=dir(accessclasses.accessclasslib)
        # Register default access classes
        for accessclassname in accessmodules:
            if accessclassname[:2]!='__':
                try:
                    # Import access class module
                    accessmodule=__import__('accessclasslib.%s' % accessclassname,globals(),locals(),[accessclassname],-1)
                    # Register the access class
                    self.__register_access_class(accessmodule.AccessClass)
                except:
                    print '(EVOGTK - WidgetAccess) WARNING: Widget access class module "%s" can not be imported' % accessclassname
        # Set class as initialized
        self.__initialised=True

    def __getattr__(self,name):
        """
        Get attribute method overload for accesing widgets content
        """
        # Check if we are getting a widget
        if name not in ['__widgets','__accessmap','__initialized']:
            widget=self.__widgets.get_widget(name)
            # Get the widget contents
            return self.__get_widget_content(widget)
        else:
            # Call original __getattr__ method
            return super(WidgetAccess,self).__getattr__(name)
        
    def __setattr__(self,name,value):
        """
        Set attribute method overload for accesing widgets content
        """
        # Assignment during initialisation
        if not self.__dict__.has_key('_WidgetAccess__initialised'):
            self.__dict__[name]=value
            return self.__dict__[name]
        # Assignment after initialisation
        # Check if we are setting a widget
        widget=self.__widgets.get_widget(name)
        if widget:
            # Set widget contents
            self.__set_widget_content(widget,value)
        else:
            # Call original __setattr__ method
            return super(WidgetAccess,self).__setattr__(name,value)

    def __set_widget_content(self,widget,content):
        """
        Sets the widget value based on its type
        """
        wclass=widget.__class__
        if self.__accessmap.has_key(wclass):
            contenttype=type(content)
            supportedtypes=self.__accessmap[wclass].supported_types()
            if contenttype in supportedtypes or not supportedtypes:
                self.__accessmap[wclass].set_content(widget,content)
            else:
                raise TypeError('(EVOGTK - Widget Access) Widget class %s doesn\'t support type %s in assignation' % (wclass,contenttype))
        else:
            raise TypeError('(EVOGTK - Widget Access) Widget class %s is not supported for direct access' % wclass)
        
    def __get_widget_content(self,widget):
        """
        Gets the widget content based on its type
        """
        wclass=widget.__class__
        if self.__accessmap.has_key(wclass):
            return self.__accessmap[wclass].get_content(widget)
        else:
            return None

    def __register_access_class(self,accessclass):
        """
        Registers a new access class
        """
        # Instantiate the accessclass
        aclass=accessclass()
        for widgetclass in aclass.supported_widgets():
            self.__accessmap[widgetclass]=aclass
