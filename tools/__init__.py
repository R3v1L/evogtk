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
# tools
# Tool functions used along the framework
###############################################################################

# Python Imports
import os
import time

# GTK Imports
import gobject
import gtk

# EVOGTK Imports
import evogtk

def formatColor(gtkcolor,format=evogtk.COLOR_FORMAT_HTML,alpha=65535,):
    """
    Returns a color in the desired format
        gtkcolor: A gtk.gdk.Color instance
        alpha: An alpha value (0..65535). Default is 65536
        format: The desired return format. Can be either:
            evogtk.COLOR_FORMAT_GTKCOLOR: A gtk.gdk.Color object
            evogtk.COLOR_FORMAT_GTKCOLORALPHA: A tuple with a gtk.gdk.Color object and an alpha value (0..65535)
            evogtk.COLOR_FORMAT_RGB: A tuple with red, green and blue values (0..65535)
            evogtk.COLOR_FORMAT_RGBA: A tuple with red, green, blue and alpha values (0..65535)
            evogtk.COLOR_FORMAT_GLCOLOR: A tuple with red, green, blue and alpha values (0.0..1.0)
            evogtk.COLOR_FORMAT_HTML: An html color formatted string
    Returns:
        Color in specified format
    """
    if format==evogtk.COLOR_FORMAT_GTKCOLOR:
        return gtkcolor
    elif format==evogtk.COLOR_FORMAT_GTKCOLORALPHA:
        return (gtkcolor,alpha)
    elif format==evogtk.COLOR_FORMAT_RGB:
        return (gtkcolor.red,gtkcolor.green,gtkcolor.blue)
    elif format==evogtk.COLOR_FORMAT_RGBA:
        return (gtkcolor.red,gtkcolor.green,gtkcolor.blue,alpha)
    elif format==evogtk.COLOR_FORMAT_GLCOLOR:
        return (gtkcolor.red/65535.0,gtkcolor.green/65535.0,gtkcolor.blue/65535.0,alpha/65535.0)
    elif format==evogtk.COLOR_FORMAT_HTML:
        r=hex(gtkcolor.red/256)[2:].upper()
        g=hex(gtkcolor.green/256)[2:].upper()
        b=hex(gtkcolor.blue/256)[2:].upper()
        if len(r)<2: r='0'+r
        if len(g)<2: g='0'+g
        if len(b)<2: b='0'+b
        return '#%s%s%s' % (r,g,b)
    else:
        raise TypeError('(EVOGTK - Tools) formatcolor requires a valid return format value.')

def processPendingEvents():
    """
    Proccesing of pending gtk events
    """
    while gtk.events_pending():
        gtk.main_iteration()

def openWithDefaultApp(filename):
    """
    Open a file in default system application
    """
    if os.name == 'nt':
        os.filestart(filename)
    elif os.name == 'posix':
        os.system('/usr/bin/xdg-open "%s"' % filename)

def setupComboBox(options,parent=None,active=0,pack_start=False,pack_end=False,expand=True,fill=True,padding=0,changed_callback=None):
    """
    Setups a combobox with given options
    """
    # TODO: evogtk.tools: setupComboBox to allow a given combobox and fill it with options (Move to factories)
    # Create new combobox
    combobox=gtk.combo_box_new_text()
    # Fill combobox
    data=options.keys()
    data.sort()
    index=0
    for value in data:
        if value==active:
            active=index
        combobox.append_text(value)
        index+=1
    combobox.set_active(active)
    combobox.show()
    # If parent is specified, add the combo to its parent
    if parent:
        if pack_start:
            parent.pack_start(combobox,expand,fill,padding)
        elif pack_end:
            parent.pack_end(combobox,expand,fill,padding)
        else:
            parent.add(combobox)
    if changed_callback:
        combobox.connect('changed',changed_callback)
    return combobox 

def newTextTag(attribs={},buffer=None,):
    """
    Text tag helper function for gtk.TextView
    
    Format of text tag attributes (are optional): 
        attribs = {
            'name': Name of tag. REQUIRED,
            'background': Color as string,
            'background-gdk': Color as gtk.gdk.Color,
            'direction': gtk.TEXT_DIR_NONE, gtk.TEXT_DIR_LTR or gtk.TEXT_DIR_RTL,
            'editable': True or False
            'family': 'Font family name',
            'font': Font description as string (I.E. Sans Italic 12),
            'font-desc' Font description as pango.FontDescription,
            'foreground': Color as string,
            'foreground-gdk': Color as gtk.gdk.Color,
            'indent': Pixels of indentation for the paragraph,
            'invisible': If True text is hidden,
            'justification': gtk.JUSTIFY_LEFT, gtk.JUSTIFY_RIGHT, gtk.JUSTIFY_CENTER or gtk.JUSTIFY_FILL,
            'language': ISO Code of the text language, 
            'left-margin': Pixels,
            'paragraph-background': Paragraph background color,
            'pixels-above-lines': Pixels of blank space above paragraphs,
            'pixels-below-lines': Pixels of blank space below paragraphs,
            'pixels-inside-wrap': Pixels of blank space between wrapped lines in a paragraph
            'right-margin': Pixels,
            'rise': Pixels (To set above or under (if negative) base text line),
            'scale': Pango relative scale (pango.SCALE_XX_SMALL, pango.SCALE_X_SMALL, pango.SCALE_SMALL, pango.SCALE_MEDIUM, pango.SCALE_LARGE, pango.SCALE_X_LARGE, pango.SCALE_XX_LARGE)
            'size': Font size in Pango units,
            'size-points': Font size in points,
            'stretch': pango.STRETCH_ULTRA_CONDENSED, pango.STRETCH_EXTRA_CONDENSED, pango.STRETCH_CONDENSED, pango.STRETCH_SEMI_CONDENSED, pango.STRETCH_NORMAL, pango.STRETCH_SEMI_EXPANDED, pango.STRETCH_EXPANDED, pango.STRETCH_EXTRA_EXPANDED, pango.STRETCH_ULTRA_EXPANDED,
            'strikethrough: If True, strike through the text,
            'style: pango.STYLE_NORMAL, pango.STYLE_OBLIQUE or pango.STYLE_ITALIC,
            'tabs': Custom tabs for this text,
            'underline': pango.UNDERLINE_NONE, pango.UNDERLINE_SINGLE, pango.UNDERLINE_DOUBLE or pango.UNDERLINE_LOW
            'variant': pango.VARIANT_NORMAL or pango.VARIANT_SMALL_CAPS,
            'weight': Font weight as an integer: pango.WEIGHT_ULTRALIGHT = 200, pango.WEIGHT_LIGHT = 300, pango.WEIGHT_NORMAL = 400, pango.WEIGHT_BOLD = 700, pango.WEIGHT_ULTRABOLD = 800, pango.WEIGHT_HEAVY = 900.
            'wrap-mode': gtk.WRAP_NONE, gtk.WRAP_CHAR or gtk.WRAP_WORD,
        }
    """
    if attribs.has_key('name'):
        tag = gtk.TextTag(attribs['name'])
        for attrib in attribs:
            if attrib != 'name':
                tag.set_property(attrib, attribs[attrib])
        if buffer:
            buffer.get_tag_table().add(tag)
        return tag
    else:
        raise Exception('EVOGTK: tools.netTextTag: No name specified in tag attributes')
    
def fadeWindow(window,visibility,delay=500,min=0,max=1,destroy=False,locking=False):
    """
    Animates show/hide for a window widget
    """
    # Check if input values are correct
    if max>1 or min < 0:
        raise Exception('(EVOGTK - Tools - fadeWindow) opacity range must be between 0 and 1')
    if delay < 100:
        raise Exception('(EVOGTK - Tools - fadeWindow) delay bust be at least 100ms')
    # Animation callback
    def animcallback(window,visibility,destroy,min,max):
        """
        Animation callback
        """
        transp=window.get_opacity()
        if visibility and transp < max:
            window.set_opacity(transp+0.01)
        elif not visibility and transp > min:
            window.set_opacity(transp-0.01)
        else:
            if destroy:
                window.destroy()
            return False
        return True
    # Initial animation setup
    if visibility:
        window.set_opacity(min)
    else:
        window.set_opacity(max)
    if locking:
        # Do animation with locking
        while animcallback(window,visibility,destroy,min,max):
            processPendingEvents()
            time.sleep(delay/100000.0)
    else:
        # Setup animation
        return gobject.timeout_add(delay/100,animcallback,window,visibility,destroy,min,max,priority=gobject.PRIORITY_HIGH)

def moveWindow(window,x,y,delay=200,locking=False):
    """
    Animates window widget movement
    """
    # Animation callback
    def animcallback(window,x,y):
        """
        Animation callback
        """
        # Get window position
        posx,posy=window.get_position()
        if posx==x and posy==y:
            return False
        if posx>x:
            posx-=1
        if posx<x:
            posx+=1
        if posy>y:
            posy-=1
        if posy<y:
            posy+=1
        window.move(posx,posy)
        return True
    if locking:
        # Do animation with locking
        while animcallback(window,x,y):
            processPendingEvents()
            time.sleep(delay/100000.0)
    else:
        # Setup animation
        return gobject.timeout_add(delay/100,animcallback,window,x,y,priority=gobject.PRIORITY_HIGH)

def resizeWindow(window,width,height,delay=500,locking=False):
    """
    Animates window widget resize
    """
    # Animation callback
    def animcallback(window,width,height):
        """
        Animation callback
        """
        # Get window position
        sizex,sizey=window.get_size()
        if sizex==width and sizey==height:
            return False
        if sizex>width:
            sizex-=2
        if sizex<width:
            sizex+=2
        if sizey>height:
            sizey-=2
        if sizey<height:
            sizey+=2
        window.resize(sizex,sizey)
        return True
    if locking:
        # Do animation with locking
        while animcallback(window,width,height):
            processPendingEvents()
            time.sleep(delay/100000.0)
    else:
        # Setup animation
        return gobject.timeout_add(delay/100,animcallback,window,width,height,priority=gobject.PRIORITY_HIGH)