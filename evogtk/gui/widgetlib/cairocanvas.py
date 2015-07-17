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
# cairocanvas
# EVOGTK Cairo Canvas
###############################################################################

# Python imports
from math import pi

# Cairo imports
import cairo

# GTK Imports
import gtk

class CairoCanvas(gtk.DrawingArea):
    """
    Cairo Canvas Widget
    """
    __gtype_name__ = 'CairoCanvas'

    QUEUE_TYPES={
    }
    
    def __init__(self,drawcallback=None,width=800,height=600,queue=[]):
        """
        Class Initialization
        """
        # DrawingArea initialization
        gtk.DrawingArea.__init__(self)
        # Set initial size of canvas
        self.set_size_request(width, height)
        # Set initial scale and translation for canvas drawing
        self.__scale=(1,1)
        self.__translate=(0,0)
        # Drawing callback
        self.__drawcallback=drawcallback
        # Drawing queue
        self.__queue=queue
        # Connect expose event for canvas drawing 
        self.__expose_handler_id=self.connect('expose-event', self.__expose)

    def __expose(self,widget,event):
        """
        Expose event handler
        """
        # Get the Cairo Context
        ctx = widget.window.cairo_create()
        # Limit drawing to shown rectangle
        ctx.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        ctx.clip()
        # Set drawing scale and translation
        ctx.scale(*self.__scale)
        ctx.translate(*self.__translate)
        # Drawing queue
        if self.__queue:
            self.render_queue(ctx)
        # Call draw callback
        if self.__drawcallback:
            self.__drawcallback(ctx)

    def set_draw_callback(self,callback):
        """
        Sets draw callback
        """
        self.__drawcallback=callback

    def render_queue(self,ctx):
        """
        Draws all objects in the queue
        """
        pass

    def set_scale(self,swidth,sheight):
        """
        Sets current scale for Cairo drawing
        """
        self.__scale=(swidth,sheight)

    def get_scale(self):
        """
        Sets current scale for Cairo drawing
        """
        return self.__scale

    def set_translation(self,swidth,sheight):
        """
        Sets current scale for Cairo drawing
        """
        self.__translate=(swidth,sheight)

    def draw_rect(self,ctx,x,y,w,h,color=(1,1,1),bordercolor=(0,0,0),borderwidth=1,border=True,fill=True):
        """
        Draws a rectangle
        """
        if fill:
            ctx.set_source_rgb(*color)
            ctx.rectangle(x,y,w,h)
            ctx.fill()
        if border:
            ctx.set_line_width(borderwidth)
            ctx.set_source_rgb(*bordercolor)
            ctx.rectangle(x,y,w,h)
            ctx.stroke()
        
    def draw_arc(self,ctx,x,y,r,s=0,e=2*pi,color=(1,1,1),bordercolor=(0,0,0),borderwidth=1,border=True,fill=True):
        """
        Draws an arc
        """
        if fill:
            ctx.set_source_rgb(*color)
            ctx.arc(x,y,r,s,e)
            ctx.fill()
        if border:
            ctx.set_line_width(borderwidth)
            ctx.set_source_rgb(*bordercolor)
            ctx.arc(x,y,r,s,e)
            ctx.stroke()
            
    def draw_png(self,ctx,x,y,img=None,filename=None):
        """
        Draws a png pixmap
        """
        if not img and not filename:
            raise Exception('EVOGTK: cairocanvas: No image or filename specified')
        # If a filename is specified, open file and create a new image
        if filename:
            img=cairo.ImageSurface.create_from_png(filename)
        # Paint image
        ctx.set_source_surface(img,x,y)
        ctx.paint()