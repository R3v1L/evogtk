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
# Module: evogtk.widgets.colorpicker
# Created: 27/12/2010 09:26:25
# Description: Color picker widget
###############################################################################

# GTK Imports
import gobject,gtk

class ColorPicker(gtk.Button):
    """
    Color picker widget class
    """
    __gtype_name__ = 'ColorPicker'
    __properties = {
        'predefined-colors' : (gobject.TYPE_STRING,'Predefined colors','List of comma separated HTML format predefined colors','',gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
        'show-predef-palette': (gobject.TYPE_BOOLEAN,'Show predefined palette','Shows the predefined colors palette',True,gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
        'show-color-palette': (gobject.TYPE_BOOLEAN,'Show color palette','Shows the color palette',True,gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
        'show-gray-palette': (gobject.TYPE_BOOLEAN,'Show grayscale palette','Shows the grayscale palette',True,gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
        'show-color-selector': (gobject.TYPE_BOOLEAN,'Shows color selector','Shows the color selector widget',False,gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
    }
    __gproperties__ = __properties

    __gsignals__ = { 
        'changed' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,(gobject.TYPE_OBJECT,))
    }

    def __init__(self,predefined_colors='',show_palette=True,show_color_selector=True):
        """
        Initialization
        """        
        # Initialize parent class
        gtk.Button.__init__(self)
        # Initialize popup window
        self.__popup_window=gtk.Window()
        self.__popup_window.set_decorated(False)
        self.__popup_window.set_resizable(False)
        self.__popup_window.set_keep_above(True)
        self.__popup_window.set_border_width(10)
        # Initialize color selection widget
        self.__popup_vbox=gtk.VBox()
        self.__colorsel=gtk.ColorSelection()
        self.__popup_vbox.pack_start(self.__colorsel)
        self.__popup_window.add(self.__popup_vbox)
        # Connect signals to show popup
        self.connect('clicked',self.__popup)
        # Connect signals to sync color
        self.__colorsel.connect('color-changed', self.__sync_color)
        # Construct the widget
        hbox=gtk.HBox()
        self.__eventbox=gtk.EventBox()
        self.__eventbox.set_size_request(20,10)
        arrow=gtk.Arrow(gtk.ARROW_DOWN,gtk.SHADOW_NONE)
        arrow.set_size_request(11,11)
#        arrowup=gtk.Arrow(gtk.ARROW_DOWN,gtk.SHADOW_ETCHED_OUT)
#        arrowdown=gtk.Arrow(gtk.ARROW_DOWN,gtk.SHADOW_ETCHED_OUT)
#        arrowup.set_size_request(11,11)
#        arrowdown.set_size_request(11,11)
#        fixedarrows=gtk.Fixed()
        vsep=gtk.VSeparator()
        vsep.set_size_request(10,10)
        hbox.pack_start(self.__eventbox)
        hbox.pack_start(vsep,False,False)
        hbox.pack_start(arrow,False,False)
#        hbox.pack_start(fixedarrows,False,False)
#        fixedarrows.put(arrowup,0,0)
#        fixedarrows.put(arrowdown,0,8)
        hbox.show_all()
        self.add(hbox)
        # Palettes initialization
        self.__vbox_palette=gtk.VBox(spacing=5)
        self.__generate_grayscale_palette()
        self.__generate_color_palette()
        # Pack palette
        self.__popup_vbox.pack_start(self.__vbox_palette)
        self.__predef_palette=self.__create_palette_table(1,18)
        self.__predef_palette.color_buttons=[]
        self.__vbox_palette.pack_start(self.__predef_palette)
        self.__vbox_palette.pack_start(self.__grayscale_palette)
        self.__vbox_palette.pack_start(self.__color_palette)
        self.__vbox_palette.show_all()
        # Calculate popup window allocation
        self.__popup_window.show_all()
        self.__csalloc=self.__popup_window.get_allocation()
        self.__popup_window.hide()

    def do_changed(self,widget,event=None): 
        pass

    def __create_palette_table(self,rows,cols,spacing=1):
        """
        Returns a palete table instance 
        """
        table=gtk.Table(rows,cols)
        table.set_row_spacings(1)
        table.set_col_spacings(1)
        return table
        
    def __create_palette_color_button(self,color):
        """
        Returns a palette color button instance
        """
        but=gtk.EventBox()
        but.set_size_request(10,10)
        for state in [gtk.STATE_ACTIVE,gtk.STATE_INSENSITIVE,gtk.STATE_NORMAL,gtk.STATE_PRELIGHT,gtk.STATE_SELECTED]:
            but.color_obj=color
            but.modify_bg(state,but.color_obj)
        but.connect('button-press-event',self.__color_button_handler)
        return but

    def __generate_predefined_palette(self):
        """
        Construct predefined colors widgets
        """
        for cb in self.__predef_palette.color_buttons:
            cb.destroy()
        self.__predef_palette.color_buttons=[]
        colors=self.predefined_colors.split(',')
        rows=len(colors)/18
        if len(colors)%18>0:
            rows+=1
        self.__predef_palette.resize(rows,18)
        row=0
        col=0
        for color in colors:
            if color.strip():
                but=self.__create_palette_color_button(gtk.gdk.color_parse(color.strip()))
                self.__predef_palette.color_buttons.append(but)
                self.__predef_palette.attach(but,col,col+1,row,row+1)
                col+=1
                if col == 18:
                    row+=1
                    col=0
        self.__predef_palette.show_all()

    def __generate_color_palette(self):
        """
        Initializes a default palette
        """
        # Color palette
        self.__color_palette=self.__create_palette_table(2,3)
        factor=65535/5
        for i in range(3):
            for j in range(2):
                pal=self.__create_palette_table(6,6)
                self.__color_palette.attach(pal,i,i+1,j,j+1,)
                for col in range(6):
                    for row in range(6):
                        but=self.__create_palette_color_button(gtk.gdk.Color((i+j*3)*factor,col*factor,row*factor))
                        pal.attach(but,col,col+1,row,row+1)

    def __generate_grayscale_palette(self):
        # Grayscale palette
        self.__grayscale_palette=gtk.HBox(spacing=1)
        for val in range(18):
            col=val*(65535/18)
            but=self.__create_palette_color_button(gtk.gdk.Color(col,col,col))
            self.__grayscale_palette.pack_start(but)

    def __color_button_handler(self,widget,event=None):
        """
        Sets current color to the color of the clicked color button
        """
        self.set_color(widget.color_obj)

    def __connect_hide_signal(self):
        """
        Starts the handling of popup hiding when mouse leaves it
        """
        self.__hide_signal=self.__popup_window.connect('leave-notify-event',self.__popdown)

    def __sync_color(self,widget,event=None):
        """
        Synchronize color selector with color shown in the button
        """
        # Set color in the button
        for state in [gtk.STATE_ACTIVE,gtk.STATE_INSENSITIVE,gtk.STATE_NORMAL,gtk.STATE_PRELIGHT,gtk.STATE_SELECTED]:
            self.__eventbox.modify_bg(state, self.__colorsel.get_current_color())
        self.emit('changed', self)

    def __popup(self,widget=None,event=None):
        """
        Shows popup
        """
        if not self.__popup_window.get_property('visible'):
            # Get main window absolute position
            x,y = self.get_toplevel().get_window().get_origin()
            # Get caller widget absolute position using main window coords
            alloc=widget.get_allocation()
            self.__popup_window.move(x+alloc.x-self.__csalloc.width+alloc.width,y+alloc.y+alloc.height)
            gobject.timeout_add(1000,self.__connect_hide_signal)
            self.__popup_window.show()
        else:
            self.__popup_window.hide()

    def __popdown(self,widget=None,event=None):
        """
        Hides calendar
        """
        alloc=widget.get_allocation()
        if event.x < 0 or event.y < 0 or event.x > alloc.width-10 or event.y > alloc.height-10:
            self.__popup_window.hide()
            self.__popup_window.disconnect(self.__hide_signal)
            return True

    def set_color(self,color):
        """
        Sets the current color
        """
        self.__colorsel.set_current_color(color)

    def get_color(self):
        """
        Gets the current color
        """
        return self.__colorsel.get_current_color()

    def do_get_property(self, property):
        """
        Property getting value handling
        """
        if property.name=='predefined-colors':
            return self.predefined_colors
        if property.name=='as-palette':
            return self.as_palette

    def do_set_property(self, property, value):
        """
        Property setting value handling
        """
        if property.name=='predefined-colors':
            self.predefined_colors=value
            if value:
                self.__generate_predefined_palette()
        if property.name=='show-color-palette':
            self.show_palette=value
            self.__color_palette.set_property('visible',value)
        if property.name=='show-grayscale-palette':
            self.show_palette=value
            self.__grayscale_palette.set_property('visible',value)
        if property.name=='show-color-selector':
            self.show_color_selector=value
            self.__colorsel.set_property('visible',value)
        # Recalculate popup allocation
        self.__popup_window.show()
        self.__csalloc=self.__popup_window.get_allocation()
        self.__popup_window.hide()

gobject.type_register(ColorPicker)