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
# browsers
# HTML Browser factory class
###############################################################################

# Import GTK
import gtk

# EVOGTK Imports
import evogtk

# GTK MozEmbed Imports
if evogtk.HAS_GTKMOZEMBED:
    import gtkmozembed

class WebBrowser(gtk.VBox):
    """
    Browser Factory Class
    """
    
    __gtype_name__ = 'WebBrowser'
    ## Default signal dictionary
    #__default_signal_dict={
    #    'link-message': self.__default_signal_handler, # Link message changed (Mouse over link)
    #    'js-status': self.__default_signal_handler, # JavaScript message changed
    #    'location': self.__default_signal_handler, # Document location changed
    #    'title': self.__default_signal_handler, # Document title changed
    #    'progress': self.__default_signal_handler, # Loading progress changed
    #    'net-state': self.__default_signal_handler, # Load document changed
    #    'net-start': self.__default_signal_handler, # Load document started
    #    'net-stop': self.__default_signal_handler, # Load document finished
    #    'new-window': self.__default_signal_handler, # New window creation
    #    'visibility': self.__default_signal_handler, # New window needs to be shown or hidden
    #    'destroy-browser': self.__default_signal_handler, # Browser widget destroyed
    #    'open-uri': self.__default_signal_handler, # Trying to load a new document
    #}

    def __init__(self,initialurl='http://www.google.com',toolbar=False,addressbar=False,statusbar=False):
        """
        Class constructor
        """
        # Check if we have GTKMozEmbed support before initialize
        if not evogtk.HAS_GTKMOZEMBED:
            raise ImportError('(EVOGTK - WebBrowser widget) There is no support for WebBrowser without GTKMozEmbed support')
        # Create browser instance
        self.__browser=gtkmozembed.MozEmbed()
        # Check if we have to create basic controls
        self.__toolbar=None
        self.__addressbar=None
        self.__statusbar=None
        if toolbar:
            self.__toolbar=gtk.Label('Barra de herramientas')
        # Check if we have to create address bar
        if addressbar:
            self.__addressbar=gtk.HBox()
            self.__addressbar.pack_start(gtk.Label('Barra de dirección'))
        # Check if we have to create basic status
        if statusbar:
            self.__statusbar=gtk.Label('Barra de estado')
        # Pack all widgets
        if self.__toolbar:
            self.pack_start(self.__toolbar,False,False)
        if self.__addressbar:
            self.pack_start(self.__addressbar,False,False)
        self.pack_start(self.__browser)
        if self.__statusbar:
            self.pack_start(self.__statusbar,False,False)
        self.show_all()

    def __normalize_url(self,url):
        """
        Normalizes URL for correct use in browser
        """
        # TODO: evogtk.widgets.webbrowser: URL Normalization
        return url

    def url(self):
        """
        Get current URL
        """
        return self.__browser.get_location()

    def load(self,url):
        """
        Load an URL into browser
        """
        urlnorm=self.__normalize_url(url)
        self.__browser.load_url(urlnorm)
        self.__browser.grab_focus()
    
    def stop(self):
        """
        Stop loading current page
        """
        self.browser.stop_load()
        
    def back(self):
        """
        Go back in browser history
        """
        if self.__browser.can_go_back():
            self.__browser.go_back()
        return self.__browser.can_go_back()

    def historystatus(self):
        """
        Return a tuple indicating if there is history to go back and forward
        """
        return (self.__browser.can_go_back(),self.__browser.can_go_forward())

    def next(self):
        """
        Go back in browser history
        """
        if self.__browser.can_go_forward():
            self.__browser.go_forward()
        return self.__browser.can_go_forward()
    
    def reloadnormal(self):
        """
        Reload current page normally
        """
        self.__browser.reload(gtkmozembed.FLAG_RELOADNORMAL)

    def reloadcache(self):
        """
        Reload current page bypassing cache
        """
        self.__browser.reload(gtkmozembed.FLAG_RELOADBYPASSCACHE)

    def reloadproxy(self):
        """
        Reload current page bypassing cache
        """
        self.__browser.reload(gtkmozembed.FLAG_RELOADBYPASSPROXY)

    def reloadcacheproxy(self):
        """
        Reload current page bypassing cache
        """
        self.__browser.reload(gtkmozembed.FLAG_RELOADBYPASSPROXYANDCACHE)
        
    def title(self):
        """
        Return current page title
        """
        return self.__browser.get_title()