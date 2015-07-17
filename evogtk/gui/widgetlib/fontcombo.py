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
# Author: (C) 2010 Oliver Gutiérrez <ogutsua@evosistemas.com>
# Module: evogtk.widgets.fontcombo
# Created: 27/12/2010 09:26:25
# Description: Font combobox widget
###############################################################################

# Python imports
import string

# GTK Imports
import gobject,gtk,pango,pangocairo

# EVOGTK imports
from evogtk.factories.treeviews import TreeViewFactory

class FontCombo(gtk.Button):
    """
    Font combobox widget class
    """
    __gtype_name__ = 'FontCombo'
#    __properties = {
#        'predefined-colors' : (gobject.TYPE_STRING,'Predefined colors','List of comma separated HTML format predefined colors','',gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
#    }
#    __gproperties__ = __properties

    __gsignals__ = { 
        'changed' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,(gobject.TYPE_OBJECT,))
    }

    def __init__(self):
        """
        Initialization
        """        
        # Initialize parent class
        gtk.Button.__init__(self)
        # Initialize popup window
        self.__popup_window=gtk.Window(gtk.WINDOW_POPUP)
        self.__popup_window.set_decorated(False)
        self.__popup_window.set_resizable(False)
        self.__popup_window.set_keep_above(True)
        self.__popup_window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_COMBO)
        # Initialize treeview with font list
        self.__scroller=gtk.ScrolledWindow(gtk.Adjustment(),gtk.Adjustment())
        self.__tview=gtk.TreeView()
        self.__tview.set_flags(gtk.CAN_FOCUS)
        self.__scroller.add(self.__tview)
        self.__popup_window.add(self.__scroller)
        self.__hide_signal=None
        # Connect signals to show/hide popup
        self.connect('clicked',self.__popup)
        self.connect('key-release-event',self.__scroll_to_font)
        self.__tview.connect('cursor-changed',self.__sync_font)
        self.__tview.connect('row-activated',self.__popdown_forced)
        # Enable search in treeview
        self.__tview.set_search_column(0)        
        # Initialize popup window
        self.__popup_window.show_all()
        self.__csalloc=self.__popup_window.get_allocation()
        self.__popup_window.hide()
        # Construct the widget
        hbox=gtk.HBox()
        self.__label=gtk.Label()
        self.__label.set_ellipsize(pango.ELLIPSIZE_END)
        arrow=gtk.Arrow(gtk.ARROW_DOWN,gtk.SHADOW_NONE)
        arrow.set_size_request(11,11)
        vsep=gtk.VSeparator()
        vsep.set_size_request(10,10)
        hbox.pack_start(self.__label,True,True)
        hbox.pack_start(vsep,False,False)
        hbox.pack_start(arrow,False,False)
        hbox.show_all()
        self.add(hbox)
        # Initialize font list
        self.__initialize_font_list()

    def __scroll_to_font(self,widget,event):
        """
        Scroll to a font
        """
        if event.string in string.letters+string.digits:
            print event.string
            iter=self.__fontlist.search(event.string,startwith=True)
            if iter:
                self.__tview.scroll_to_cell(self.__fontlist.storagemodel.get_path(iter))

    def do_changed(self,widget,event=None): 
        pass

    def __initialize_font_list(self):
        """
        Construct font list
        """

        def compare_data(model, iter1, iter2):
            """
            Sorting function for the fonts list store
            """
            data1 = model.get_value(iter1,0)
            data2 = model.get_value(iter2,0)
            return cmp(data1, data2)        

        self.__fontlist=TreeViewFactory('list', ['str','markup'], [],treeview=self.__tview)
        
        # Get all system fonts
        self.__font_families=pangocairo.cairo_font_map_get_default().list_families()
        for family in self.__font_families:
            escaped=gobject.markup_escape_text(family.get_name())
            markedup='<span face="%s">%s</span>' % (escaped,escaped)
            self.__fontlist.append([family.get_name(),markedup])
        self.__tview.set_headers_visible(False)
        self.__tview.get_column(0).set_property('visible',False)
        self.__scroller.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)
        self.__fontlist.storagemodel.set_sort_func(0,compare_data)
        self.__fontlist.storagemodel.set_sort_column_id(0,gtk.SORT_ASCENDING)

    def __sync_font(self,widget,event=None):
        """
        Synchronize font list selection with widget label and value
        """
        # Get currently selected font
        self.__selected=self.__fontlist.selected()
        self.__label.set_markup(self.__selected[1])
        self.emit('changed', self)
        self.__popup_window.hide()

    def __popup(self,widget=None,event=None):
        """
        Shows popup
        """
        if not self.__popup_window.get_property('visible'):
            # Get main window absolute position
            x,y = self.get_toplevel().get_window().get_origin()
            # Get caller widget absolute position using main window coords
            alloc=widget.get_allocation()
            self.__popup_window.move(x+alloc.x,y+alloc.y+alloc.height)
            self.__popup_window.set_size_request(alloc.width,300)
            self.__popup_window.show()
            self.__popup_window.set_focus(self.__tview)
        else:
            self.__popup_window.hide()

    def __popdown_forced(self,*args,**kwargs):
        """
        Forced popdown of popup window
        """
        self.__popup_window.hide()

    def get_font_name(self):
        """
        Get the current font name
        """
        return self.__selected[0]
    
    def set_font_name(self,value):
        """
        Set the current font name
        """
        if self.__fontlist.select(value):
            self.__label.set_markup(self.__selected[1])

#    def do_get_property(self, property):
#        """
#        Property getting value handling
#        """
#        if property.name=='predefined-colors':
#            return self.predefined_colors
#
#    def do_set_property(self, property, value):
#        """
#        Property setting value handling
#        """
#        if property.name=='predefined-colors':
#            self.predefined_colors=value
#            self.__initialize_predefined_colors()

gobject.type_register(FontCombo)