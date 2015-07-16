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
# dbcombobox
# Database gtk.ComboBox widget module
###############################################################################

# GTK Imports
import gobject, gtk

# DBWidget base class
from dbwidgetbase import DBWidgetBase

class DBComboBox(gtk.ComboBox,DBWidgetBase):
    """
    Database gtk.ComboBox widget
    """
    __gtype_name__ = 'DBComboBox'
    # Widget properties
    __properties = {
        'choices' : (gobject.TYPE_STRING,'Choices','Separated values of choice for the widget (separator character is used as separator)','',gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
        'separator-char' : (gobject.TYPE_STRING,'Separator','Separator character used to separate choice values',',',gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
    }
    __properties.update(DBWidgetBase._DBWidgetBase__properties)
    __gproperties__ = __properties     
    
    def __init__(self,*args,**kwargs):
        """
        Class initialization
        """
        # Initialize DBWidget base class
        DBWidgetBase.__init__(self,*args,**kwargs)
        # Initialize parent widget
        gtk.ComboBox.__init__(self)
        # List store for data
        self.__liststore = gtk.ListStore(str,gtk.gdk.Pixbuf)
        self.set_model(self.__liststore)
        # Cell renderers for combobox
        crt = gtk.CellRendererText()
        self.pack_start(crt, True)
        self.add_attribute(crt, 'text', 0)        
        crp = gtk.CellRendererPixbuf()
        crp.set_property('xalign',1)
        self.pack_start(crp, True)
        self.add_attribute(crp, 'pixbuf', 1)
        # Blank and error pixbufs
        self.__blankpixbuf=gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,True,8,1,1)
        self.__errorpixbuf=self.render_icon(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_MENU)
        # Widget properties
        if self.inmediate_validation:
            self.connect('changed',self.validate)

    def get_widget_data(self):
        """
        Returns widget data
        """
        iter=self.get_active_iter()
        if iter:
            return self.__liststore.get_value(iter,0)
        else:
            return None

    def set_invalidated(self):
        """
        Set this widget as invalidated
        """
        iter=self.__liststore.get_iter_first()
        while iter:
            self.__liststore.set_value(iter,1,self.__blankpixbuf)    
            iter=self.__liststore.iter_next(iter)
        iter=self.get_active_iter()
        if iter:
            self.__liststore.set_value(iter,1,self.__errorpixbuf)

    def set_validated(self):
        """
        Set this widget as validated
        """
        self.__validationerrors=[]
        iter=self.__liststore.get_iter_first()
        while iter:
            self.__liststore.set_value(iter,1,self.__blankpixbuf)    
            iter=self.__liststore.iter_next(iter)

    def do_get_property(self, property):
        """
        Property getting value handling
        """
        if property.name=='choices':
            return self.choices
        elif property.name=='separator-char':
            return self.separator_char
        else:
            return DBWidgetBase.do_get_property(self, property)

    def do_set_property(self, property, value):
        """
        Property setting value handling
        """        
        if property.name=='choices':
            self.choices=value
            # Set values
            self.__liststore.clear()
            if value:
                for choice in value.split(self.separator_char):
                    self.__liststore.append([choice,self.__blankpixbuf])
            self.set_active(0)
        elif property.name=='separator-char':
            self.separator_char=value
        else:
            DBWidgetBase.do_set_property(self, property, value)

gobject.type_register(DBComboBox)