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

# GTK Imports
import gtk

# EVOGTK Imports
from evogtk.widgets import CairoCanvas

class CairoScroller(gtk.ScrolledWindow):
    """
    Cairo Scroller Widget
    """
    __gtype_name__ = 'CairoScroller'
    
    def __init__(self,drawcallback=None,width=320,height=240,
                 zooming=True,zoomoptimal=True,actualzoom=1.0,maxzoom=3.0,minzoom=0.5,zoomstep=1.10,zoomautoadj=True,
                 queue=[]):
        """
        Class Initialization
        """        
        # ScrolledWindow initialization
        gtk.ScrolledWindow.__init__(self,gtk.Adjustment(),gtk.Adjustment())
        self.set_policy(gtk.POLICY_ALWAYS,gtk.POLICY_ALWAYS)
        # Create a gtk.Viewport for Cairo Canvas scrolling support
        self.viewport=gtk.Viewport()
        # Create Cairo Canvas
        self.canvas=CairoCanvas(drawcallback,width,height,queue)
        # Pack widgets
        self.alignment=gtk.Alignment(0.5,0.5)
        self.alignment.add(self.canvas)
        self.viewport.add(self.alignment)
        self.add(self.viewport)
        self.show_all()
        # Initialize zoom parameters
        if zooming:
            # Set zoom parameters
            self.set_zoom_parameters(width,height,zoomoptimal,actualzoom,maxzoom,minzoom,zoomstep,zooming,zoomautoadj)
            # Activate capturing of mouse events
            self.canvas.add_events(gtk.gdk.SCROLL_MASK)
            self.viewport.connect('scroll-event',self.__mouseScroll)
            # Activate autoadjust callback
            self.connect('size-allocate',self.__autoadj)
        else:
            self.__zoom=None

    def __autoadj(self,widget=None,event=None):
        """
        Auto Adjust contents based on zoom parameters
        """
        if self.__zoom and self.__zoom['autoadj'] and self.__zoom['optimal']:
            self.zoomOptimal(widget, event)
        return True
        
    def __mouseScroll(self,widget,event):
        """
        Handles mouse zooming and scrolling
        """
        if event.state & gtk.gdk.CONTROL_MASK:
            # Mouse zooming
            if event.direction == gtk.gdk.SCROLL_UP:
                self.zoomIn(widget,event)
            else:
                self.zoomOut(widget,event)
        elif event.state & gtk.gdk.SHIFT_MASK:
            # Mouse horizontal scrolling
            hadj=self.get_hadjustment()
            act=hadj.get_value()
            inc=hadj.get_step_increment()
            pagesize=hadj.get_page_size()
            lower=hadj.get_lower()
            upper=hadj.get_upper()-pagesize
            if event.direction == gtk.gdk.SCROLL_UP:
                if act>=lower+inc:
                    hadj.set_value(act-inc)
                else:
                    hadj.set_value(lower)
            else:
                if act<=upper-inc:
                    hadj.set_value(act+inc)
                else:
                    hadj.set_value(upper)
        else:
            return False
        return True

    def set_zoom_parameters(self,origwidth=320,origheight=200,zoomoptimal=True,actualzoom=1.0,maxzoom=3.0,minzoom=0.10,zoomstep=1.25,zooming=True,zoomautoadj=True):
        """
        Set zoom parameters after initialization
        """
        self.__zoom={
                'optimal': zoomoptimal,
                'width': origwidth,
                'height': origheight,
                'actual': actualzoom,
                'max': maxzoom,
                'min': minzoom,
                'step': zoomstep,  
                'autoadj': zoomautoadj,
                'maxed': False,
                'mined': False,
        }

    def redrawCanvas(self,widget=None,event=None):
        """
        Redraw the canvas
        """
        # Set new canvas scale
        if self.__zoom:
            cwindow=self.canvas.window
            if cwindow:
                cwindow.freeze_updates()     
            newsize=int(self.__zoom['width']*self.__zoom['actual']), int(self.__zoom['height']*self.__zoom['actual'])
            self.canvas.set_scale(self.__zoom['actual'],self.__zoom['actual'])
            self.canvas.set_size_request(*newsize)
            if self.__zoom and self.__zoom['autoadj']:
                calloc=self.canvas.get_allocation()
                valloc=self.viewport.get_allocation()
                hadj=self.get_hadjustment().get_value()
                vadj=self.get_vadjustment().get_value()
                xsinc=float(newsize[0])/calloc.width
                ysinc=float(newsize[1])/calloc.height
                xadj=event and xsinc*event.x-(event.x-hadj) or hadj
                yadj=event and ysinc*event.y-(event.y-vadj) or vadj
                needadj=newsize[0] > valloc.width and newsize[1] > valloc.height
                # Zoom autoadjust
                if needadj:   
                    self.viewport.get_vadjustment().props.value=yadj
                    self.viewport.get_hadjustment().props.value=xadj
            if cwindow:
                cwindow.thaw_updates()            
        self.canvas.queue_draw()

    def zoomOptimal(self,widget=None,event=None):
        """
        Zoom to optimal viewing of map
        """
        if self.__zoom:
            alloc=self.viewport.get_allocation()            
            a=float(alloc.width-self.get_vscrollbar().size_request()[0])/self.__zoom['width']
            b=float(alloc.height-self.get_hscrollbar().size_request()[1])/self.__zoom['height']
            if a<=b:
                low=a
            else:
                low=b
            if self.__zoom['min'] <= low:
                if low <= self.__zoom['max']: 
                    self.__zoom['actual']=low
                else:
                    self.__zoom['actual']=self.__zoom['max']
            else:
                self.__zoom['actual']=self.__zoom['min']
            self.__zoom['optimal']=True
            self.redrawCanvas()

    def zoomOriginal(self,widget=None,event=None):
        """
        Zoom to original size of canvas
        """
        if self.__zoom:
            self.__zoom['actual']=1
            self.__zoom['optimal']=False
            self.redrawCanvas()
    
    def zoomIn(self,widget=None,event=None):
        """
        Zoom in into canvas
        """
        if self.__zoom:
            if not self.__zoom['maxed']:
                self.__zoom['actual']*=self.__zoom['step']    
            if self.__zoom['actual']<=self.__zoom['max']:
                self.__zoom['maxed']=False
            else:
                self.__zoom['maxed']=True
            self.__zoom['optimal']=False
            self.redrawCanvas(widget,event)
    
    def zoomOut(self,widget=None,event=None):
        """
        Zoom out of canvas
        """
        if self.__zoom:
            if not self.__zoom['mined']:
                self.__zoom['actual']/=self.__zoom['step']
            if self.__zoom['actual']>=self.__zoom['min']:
                self.__zoom['mined']=False
            else:
                self.__zoom['mined']=True
            self.__zoom['optimal']=False
            self.redrawCanvas(widget,event)
    
    def getZoomScale(self):
        """
        Return current Horizontal Zoom Scale
        """
        if self.__zoom:
            return self.__zoom['actual']
        else:
            return 0
