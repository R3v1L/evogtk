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
# floatingwindow
# EVOGTK Floating window widget
###############################################################################

# GTK Imports
import gtk

# EVOGTK Imports
import evogtk

class FloatingWindow(gtk.Window):
    """
    Floating window widget
    """
    # Widget type
    __gtype_name__ = 'FloatingWindow'

    def __init__(self,title=None,color=None,width=None,height=None,rounded=False,alwaysontop=False,dragable=False,maximize=evogtk.MAXIMIZE_BOTH):
        """
        Class Initialization
        """
        self.__rounded=rounded
        self.__dragable=dragable
        if not width:
            width=-1
        if not height:
            height=-1
        self.__size=(width,height)
        # Window initialization
        super(gtk.Window,self).__init__(type=gtk.WINDOW_POPUP)
        # Window setup
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_keep_above(alwaysontop)
        self.set_size_request(*self.__size)
        # Set title
        if title:
            self.set_title(title)
        # Set dragging signals
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK|gtk.gdk.BUTTON_RELEASE_MASK|gtk.gdk.POINTER_MOTION_MASK)   
        self.connect('button-press-event',self.__set_drag)
        self.connect('button-release-event',self.__set_drag)
        self.connect('motion-notify-event',self.__drag) 
        self.__dragging=None
        # Set maximize variable
        self.__maximized=None
        # Generate mask on resizes
        self.connect('check-resize',self.__check_resize)
        # Set background color
        if color:
            self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(color))
        # Set maximization
        if maximize in [evogtk.MAXIMIZE_NONE,evogtk.MAXIMIZE_HORIZONTAL,evogtk.MAXIMIZE_VERTICAL,evogtk.MAXIMIZE_BOTH]:
            self.__maximization=maximize
        else:
            raise Exception('(EVOGTK - FloatingWindow) Maximization orientation have to be None, gtk.ORIENTATION_HORIZONTAL, gtk.ORIENTATION_VERTICAL or gtk.ORIENTATION_HORIZONTAL|gtk.ORIENTATION_VERTICAL')
    
    def __generate_mask(self,widget=None):
        """
        Generates mask for rounded windows
        """
        # Get window size for mask generation
        width,height=self.size_request()
        if self.__rounded and self.window:
            # Check if we have a fixed size to set
            if self.__size[0]>0:
                width=self.__size[0]
            if self.__size[1]>0:
                height=self.__size[1]
            if width and height:        
                # Generate window mask XPM data
                maskhead=[
                    '%s %s 2 1' % (width,height),
                    '     c None',
                    '.    c #000000',
                    ' '*5 + '.'*(width-10) + ' '*5,
                    ' '*3 + '.'*(width-6) + ' '*3,
                    ' '*2 + '.'*(width-4) + ' '*2,
                    ' ' + '.'*(width-2) + ' ',
                    ' ' + '.'*(width-2) + ' ',
                ]
                maskfoot=[
                    ' ' + '.'*(width-2) + ' ',
                    ' ' + '.'*(width-2) + ' ',
                    ' '*2 + '.'*(width-4) + ' '*2,
                    ' '*3 + '.'*(width-6) + ' '*3,
                    ' '*5 + '.'*(width-10) + ' '*5,
                ]
                mask=[]
                mask.extend(maskhead)
                mask.extend(['.'*width]*(height-10))
                mask.extend(maskfoot)
                # Set Mask
                self.window.shape_combine_mask(gtk.gdk.pixmap_create_from_xpm_d(self.window,None,mask)[1], 0, 0)
        
    def __check_resize(self,widget):
        """
        Regenerate mask in each window resize
        """
        self.__generate_mask()

    def __set_drag(self,widget,event):
        """
        Set dragging mode 
        """
        if event.type==gtk.gdk.BUTTON_PRESS:
            self.__dragging=(event.x,event.y)
        elif event.type==gtk.gdk._2BUTTON_PRESS:
            self.toggle_maximize()
        else:
            self.__dragging=None
        return False
        
    def __drag(self,widget,event):
        """
        Drag window
        """
        if self.__dragable and self.__dragging:
            pos=self.get_position()
            x=int(pos[0]+(event.x-self.__dragging[0]))
            y=int(pos[1]+(event.y-self.__dragging[1]))
            maxx,maxy=self.get_size()
            maxx=gtk.gdk.screen_width()-maxx
            maxy=gtk.gdk.screen_height()-maxy
            if x<0: x=0
            if y<0: y=0
            if x>maxx: x=maxx
            if y>maxy: y=maxy
            self.move(x,y)
        return False

    def toggle_maximize(self):
        """
        Maximize or restore size of window
        """
        if self.__maximization!=evogtk.MAXIMIZE_NONE:
            if self.__maximized:
                self.set_size_request(*self.__size)
                self.move(self.__maximized[0],self.__maximized[1])
                self.__maximized=None
            else:
                # Save position and size values for unmaximize window
                posx,posy=self.get_position()
                width,height=self.size_request()
                self.__maximized=(posx,posy)
                # Get screen size
                screen=gtk.gdk.screen_get_default()
                monitor=screen.get_monitor_geometry(screen.get_monitor_at_window(self.window))
                # Check how maximizes
                if self.__maximization==evogtk.MAXIMIZE_BOTH:
                    posx=monitor.x
                    posy=monitor.y
                    width=monitor.width
                    height=monitor.height
                elif self.__maximization==evogtk.MAXIMIZE_HORIZONTAL:
                        posx=monitor.x
                        width=monitor.width
                elif self.__maximization==evogtk.MAXIMIZE_VERTICAL:
                    posy=monitor.y
                    height=monitor.height
                self.set_size_request(width,height)
                self.move(posx,posy)
