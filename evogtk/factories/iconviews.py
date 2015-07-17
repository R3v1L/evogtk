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
# iconviews
# IconView factory class
###############################################################################

# Import GTK
import gtk

###############################################################################
# IconView Factory class
###############################################################################
class IconViewFactory(object):
    """
    Icon View Factory Class
    """
    def __init__(self,iconview):
        """
        Class constructor
        """
        self.__iconview=iconview
        self.__iconlist=gtk.ListStore(str, gtk.gdk.Pixbuf)
        self.__iconview.set_model(self.__iconlist)
        self.__iconview.set_text_column(0)
        self.__iconview.set_pixbuf_column(1)

    def __load_icon(self,filename,width=None,height=None):
        """
        Load and return pixbuf with the loaded icon
        """
        if width and height:
            return gtk.gdk.pixbuf_new_from_file_at_size(filename,width,height)
        else:
            return gtk.gdk.pixbuf_new_from_file(filename)

    def search(self,text):
        """
        Search first occurence of a value in icon names and return iterator 
        """
        iter=self.__iconlist.get_iter_first()
        while iter:
            val=self.__iconlist.get_value(iter,0)
            if val==text:
                return iter
            iter=self.__iconlist.iter_next(iter)
        return None

    def append(self,filename,text,width=None,height=None):
        """
        Append new icon to iconview
        """
        self.__iconlist.append([text,self.__load_icon(filename,width,height)])

    def update(self,filename,text,width=None,height=None):
        """
        Updates an existing icon named by text
        """
        iter=self.search(text)
        if iter:
            if iter:
                self.__iconlist.set_value(iter,1,self.__load_icon(filename,width,height))
            return True
        return False
    
    def remove(self,text):
        """
        Removes icon with specified text
        """
        iter=self.search(text)
        self.__iconlist.remove(iter)
    
    def clear(self):
        """
        Clear icon view
        """
        self.__iconlist.clear()
        
    def selected(self):
        """
        Returns currently selected icon names in a list or an empty list if nothing selected
        """
        selected=self.__iconview.get_selected_items()
        data=[]
        for path in selected:
            iter=self.__iconlist.get_iter(path)
            data.append(self.__iconlist.get_value(iter,0))
        return data
