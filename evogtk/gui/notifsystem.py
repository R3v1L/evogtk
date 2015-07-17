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
# notification
# Notification system class
###############################################################################

# GTK Imports
import gobject
import gtk

# EVOGTK Imports
import evogtk
from evogtk.tools import fadeWindow,moveWindow
from evogtk.widgets import FloatingWindow

class DummyNotificationSystem(object):
    """
    Dummy notification system class
    """
    def __init__(self,appname,*args,**kwargs):
        """
        Dummy Class initialization
        """
        self.appname=appname
        self.run_queue()

    def run_queue(self):
        """
        Dummy Start/Resume queue processing
        """
        self._queue_running=True

    def stop_queue(self):
        """
        Dummy stop queue processing
        """
        self._queue_running=False

    def queue_msg(self,msg,title=None,icon=None,color=None,padding=10,permanent=False):
        """
        Dummy Enqueue a message in the notification system and print to stdout
        """
        if not title:
            title=self.appname
        if self._queue_running:
            print '%s: %s' % (title,msg)

    def queue_custom(self,widget,color=None,permanent=False):
        """
        Dummy Enqueue a custom notification with a specified widget
        """
        pass

class NotificationSystem(object):
    """
    Notification system class
    """
    def __init__(self,appname,timeout=10000,
                 xoffset=30,yoffset=30,width=350,height=None,
                 bgcolor='#444444',titlecolor='#FFFFFF',fgcolor='#FFFFFF',
                 inmediate=True,position=evogtk.NOTIF_TOP_RIGHT,fading=True):
        """
        Class initialization
        """
        # App name for setting window titles
        self.__appname=appname
        # Default timeout for msg
        self.__timeout=timeout
        # Offsets
        self.__offset=(xoffset,yoffset)
        # Notification size
        self.__size=(width,height)
        # Notification position
        if position in [evogtk.NOTIF_TOP_LEFT,evogtk.NOTIF_TOP_RIGHT,evogtk.NOTIF_BOTTOM_LEFT,evogtk.NOTIF_BOTTOM_RIGHT]:
            self.__position=position
        else:
            raise Exception('(EVOGTK - Notification System) Position for notifications must be gtk.CORNER_TOP_LEFT, gtk.CORNER_TOP_RIGHT, gtk.CORNER_BOTTOM_LEFT or gtk.CORNER_BOTTOM_RIGHT')
        # Colors
        self.__bgcolor=bgcolor
        self.__titlecolor=titlecolor
        self.__fgcolor=fgcolor
        # Inmediately show notifications
        self.__inmediate=inmediate
        # Fade in and out notifications
        self.__fading=fading
        # Notification queue
        self.__notifqueue=[]
        # Checking if a notification is already being shown
        self.__current=False
        # Checking if we are moving/resizing
        self.__moving=None
        # Create needed widgets
        self.__create_notif_window()
        # Start queue processing
        self.run_queue()

    def __ghost_window(self,widget,event):
        """
        Ghosts the notification window to be semi-transparent
        """
        fadeWindow(self.__notifwindow,False,min=0.5)

    def __deghost_window(self,widget,event):
        """
        Return notification window to normal state
        """
        if self.__current:
            fadeWindow(self.__notifwindow,True,min=0.5)

    def __create_notif_window(self):
        """
        Creates the inmediate window and box
        """
        # Generate notification window
        self.__notifbox=gtk.VBox()
        width=self.__size[0] and self.__size[0] or -1
        height=self.__size[1] and self.__size[1] or -1
        self.__notifbox.set_size_request(width,height)
        self.__notifwindow=FloatingWindow(title=self.__appname,color=self.__bgcolor,width=self.__size[0],height=self.__size[1],rounded=True,maximize=evogtk.MAXIMIZE_NONE)
        self.__notifwindow.add(self.__notifbox)
        self.__notifbox.show()
        # Set callbacks for ghosting
        self.__notifwindow.connect('enter-notify-event',self.__ghost_window)
        self.__notifwindow.connect('leave-notify-event',self.__deghost_window)        
        # Set notification window initial position
        self.__move_notif()

    def __create_message(self,data):
        """
        Creates a message notification
        """
        # Create containers
        hbox=gtk.HBox(spacing=10)
        hbox.set_border_width(10)
        vbox=gtk.VBox(spacing=5)
        align=gtk.Alignment(xalign=0, yalign=0.5, xscale=0, yscale=0)
        align.add(vbox)
        hbox.pack_end(align)
        # Create title label
        title=gtk.Label('<span color="%s"><b>%s</b></span>' % (self.__titlecolor,data[2] and data[2] or self.__appname))
        title.set_use_markup(True)
        title.set_line_wrap(True)
        title.set_alignment(0,0.5)
        vbox.pack_start(title,False,False)
        # Create icon widget if needed
        if data[4]:
            img=gtk.Image()
            pixbuf=gtk.gdk.pixbuf_new_from_file_at_size(data[4],48,48)
            img.set_from_pixbuf(pixbuf)
            hbox.pack_start(img,False,False)
        # Create message label
        msg=gtk.Label()
        msg.set_markup('<span color="%s">%s</span>' % (self.__fgcolor,gobject.markup_escape_text(data[1])))
        msg.set_line_wrap(True)
        msg.set_alignment(0,0.5)
        vbox.pack_start(msg,False,False)
        # Return notification widget and if it should be permanent        
        return(hbox,data[5])

    def __move_notif(self,animated=False):
        """
        Gets the position where we have to move the notification
        """
        # Get window size and calculate width and height
        width,height=self.__notifwindow.size_request()
        width=self.__size[0] and self.__size[0] or width
        height=self.__size[1] and self.__size[1] or height
        # Get monitor information
        monitor=gtk.gdk.screen_get_default().get_monitor_geometry(0)
        # Calculate where to move depending on specified position
        if self.__position==evogtk.NOTIF_TOP_LEFT:
            x,y=self.__offset
        elif self.__position==evogtk.NOTIF_TOP_RIGHT:
            x=monitor.width-width-self.__offset[0]
            y=self.__offset[1]
        elif self.__position==evogtk.NOTIF_BOTTOM_LEFT:
            x=self.__offset[0]
            y=monitor.height-height-self.__offset[1]
        else: # gtk.CORNER_BOTTOM_RIGHT            
            x=monitor.width-width-self.__offset[0]
            y=monitor.height-height-self.__offset[1]
        # Move window
        if animated:
            if self.__moving:
                gobject.source_remove(self.__moving)
            self.__moving=moveWindow(self.__notifwindow,x,y,)
        else:
            self.__notifwindow.move(x,y)

    def __queue_process(self):
        """
        Queue processing callback
        """
        if self.__notifqueue and self._queue_running and (self.__inmediate or not self.__current):    
            self.__prepare_current(self.__notifqueue.pop())
        return self._queue_running

    def __prepare_current(self,current):
        """
        Prepares current notification
        """
        # Create notification content based on notification type
        if current[0]=='msg':
            widget,permanent=self.__create_message(current)
        elif current[0]=='custom':
            widget=current[1]
            permanent=current[3]
        else:
            raise ('(EVOGTK - Notification System) Unknown notification type %s' % current[0])
        # If we have run out of vertical space for notifications wait until all notifications go away
        monitor=gtk.gdk.screen_get_default().get_monitor_geometry(0)
        if monitor.height-self.__offset[1]*2-widget.size_request()[1] < self.__notifwindow.size_request()[1]:
            while self.__notifbox.get_children():
                while gtk.events_pending():
                    gtk.main_iteration()
        # Show current notification
        self.__show_current(widget,permanent)

    def __show_current(self,widget,permanent):
        """
        Show current inmediate notification
        """
        # Show all widget data
        widget.show_all()
        # Add new notification
        self.__notifbox.pack_start(widget,False,False)
        # Position the notification window
        self.__move_notif(self.__inmediate)
        # Show window if not shown
        if not self.__notifwindow.get_property('visible'):
            if self.__fading:
                self.__notifwindow.set_opacity(0)
                self.__notifwindow.show_all()
                fadeWindow(self.__notifwindow,True)
            else:
                self.__notifwindow.show_all()        
        if not permanent:
            # Set a timeout for notification destroy if not a permanent notification
            gobject.timeout_add(self.__timeout,self.__clear_notif,widget,priority=gobject.PRIORITY_HIGH)
            self.__current=True

    def __clear_notif(self,widget):
        """
        Clear current notification
        """
        # Check if we have childs to remove
        childs=self.__notifbox.get_children()
        if childs:
            # If this is the last child, hide the window
            if len(childs)==1:
                if self.__fading:
                    fadeWindow(self.__notifwindow,False,locking=True)
                self.__notifwindow.hide()
                widget.destroy()
                self.__current=False
            else:
                # Destroy child
                widget.destroy()
                # Resize and move window
                self.__notifwindow.resize(self.__size[0],self.__notifbox.size_request()[1])
                self.__move_notif(self.__inmediate)

    def run_queue(self):
        """
        Start/Resume queue processing
        """
        self._queue_running=True
        gobject.timeout_add(100,self.__queue_process,priority=gobject.PRIORITY_HIGH)

    def stop_queue(self):
        """
        Start/Resume queue processing
        """
        self._queue_running=False

    def queue_msg(self,msg,title=None,icon=None,color=None,padding=10,permanent=False):
        """
        Enqueue a message in the notification system
        """
        if permanent:
            self.__prepare_current(('msg',msg,title,color,icon,permanent))
        else:
            self.__notifqueue.insert(0,('msg',msg,title,color,icon,permanent))
        
    def queue_custom(self,widget,color=None,permanent=False):
        """
        Enqueue a custom notification with a specified widget
        """
        if permanent:
            self.__prepare_current(('custom',widget,color,permanent))
        else:
            self.__notifqueue.insert(0,('custom',widget,color,permanent))

class PyNotifyNotificationSystem(DummyNotificationSystem):
    """
    PyNotify notification system class
    """
    def __init__(self,appname,*args,**kwargs):
        """
        Class initialization
        """
        import pynotify
        self.pynotify=pynotify
        self.appname=appname
        if not self.pynotify.is_initted():
            self.pynotify.init(appname)
        self.run_queue()

    def queue_msg(self,msg,title=None,icon=None,color=None,padding=10,permanent=False):
        """
        Enqueue a message in the notification system
        """
        if self._queue_running:
            if not title:
                title=self.appname    
            notif=self.pynotify.Notification(title,msg)
            if icon:
                pixbuf=gtk.gdk.pixbuf_new_from_file_at_size(icon,48,48)
                notif.set_icon_from_pixbuf(pixbuf)
            notif.show()
