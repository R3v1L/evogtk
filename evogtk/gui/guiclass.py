# -*- coding: utf-8 -*-
###############################################################################
# Copyright (C) 2008 EVO Sistemas Libres <central@evosistemas.com>
###############################################################################
"""

:mod:`guiclass` -- EVOGTK GUI class definition module
=====================================================

This is the module that contains all base GUI utility classes

.. module:: guiclass
    :platform: Unix, Windows
    :synopsis: EVOGTK GUI class definition module
.. moduleauthor:: Oliver Gutiérrez

"""

# Python Imports
import sys,os,inspect,gettext
from gettext import lgettext as _

# Import gtk
import glib,gobject,gtk.glade

# Import default handler callbacks
import defaulthandlers

# Import EVOGTK for checks
import evogtk

# Import GUI widgets helper class
from guiwidgets import GUIWidgets

# Import widget access helper class
from widgetaccess import WidgetAccess

# Import shortcut helper class
from shortcuts import ShortcutsHelper

# Import notification system
import notifsystem

# Import preferences helper class
from preferences import _PreferencesHelper

# Import threaded tasks module
import threadtasks

# Import exception handler class
from excepthandler import _ExceptionHandler

# Import dialog factory
from evogtk.factories.dialogs import DialogFactory

# GUI helper class
class GUIClass(object):
    """
    **GUI helper base class**
    
    *This class will allow you to start the application*
            
    .. note:: You always want to subclass this class. There are some methods you would like to
        redefine such as initialize

        .. code-block:: python
            :emphasize-lines: 1,2
            
            class MyAppClass(GUIClass):
                pass
    """

    # Application metadata
    metadata={
        'APP_NAME': 'EVOGTK Project',
        'APP_CODENAME': 'evogtkproject',
        'APP_VERSION': '1.0',
        'APP_DESC': 'EVOGTK application project',
        'APP_COPYRIGHT': '(C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>',
        'APP_WEBSITE': 'http://www.evosistemas.com',
    }

    # Task modes
    TASKS_MODES={
        evogtk.TASK_MODE_INITIAL: {
            'enable': [],
            'disable': [],
            'show': [],
            'hide': [],
            'activate': [],
            'deactivate': [],
            'callback': None
        },
    }

    def __init__(self,guifiles=[],configfile=None,mainapp=True,env=None,controlled_quit=True,dialogs=True,splash=True,debug=False,localedir='locale',pixmapsdir='pixmaps',disablenotifsys=False,forceinternalnotifsys=False,**kwargs):
        """
        Class constructor
        """
        # Setting up variables
        self.__guifiles=guifiles
        self.__main_app=mainapp
        self.__debug=debug
        self.__splashscreen=None

        self.APP_DIR=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe().f_back)))
        self.PIXMAPS_DIR=self.APP_DIR + '/' + pixmapsdir
        self.LOCALE_DIR=self.APP_DIR + '/' + localedir
        # Main app initialization
        if mainapp:
            # Setup glib application name
            glib.set_application_name(self.metadata['APP_CODENAME'])
            # Set up exception handler if this is the main app
            self.excepthandler=_ExceptionHandler(catch_all=debug)
            # If controlled quit is enabled set a handler
            self.excepthandler.set_handler(KeyboardInterrupt,self.__control_c_handler)
            
            # Initialize notifications system
            if disablenotifsys:
                # No graphical notifications system. Fallback to dummy notification system
                self.notifsys=notifsystem.DummyNotificationSystem(self.metadata['APP_NAME'])
            else:
                if not forceinternalnotifsys and evogtk.HAS_PYNOTIFY:
                    # Use PyNotify as notification system
                    self.notifsys=notifsystem.PyNotifyNotificationSystem(self.metadata['APP_NAME'])
                else:
                    # Use internal notification system
                    self.notifsys=notifsystem.NotificationSystem(self.metadata['APP_NAME'])
            if splash:
                self.show_splash()
        # Create GtkBuilder instance
        self.__builder_instance=gtk.Builder()
        # Setup internationalization
        gettext.textdomain(self.metadata['APP_CODENAME'])
        gettext.bindtextdomain(self.metadata['APP_CODENAME'], self.LOCALE_DIR)
        gtk.glade.bindtextdomain(self.metadata['APP_CODENAME'], self.LOCALE_DIR)
        gtk.glade.textdomain(self.metadata['APP_CODENAME'])
        
        self.__builder_instance.set_translation_domain(self.metadata['APP_CODENAME'])

        # Load GUI files
        for guifile in guifiles:
            self.__builder_instance.add_from_file(self.APP_DIR + '/' + guifile)
        # Prepare widgets for easy access
        self.widgets=GUIWidgets(self.__builder_instance)
        # Load default widget access shortcuts
        self.ui=WidgetAccess(self.widgets)
        # Connect GUI signals
        self.__connect_signals()
        # Load shortcuts helper
        self.shortcuts=ShortcutsHelper(self)
        # Set application environment
        if env:
            self.set_environment(env)
        # Create preferences helper if needed
        if self.metadata.has_key('APP_PREFERENCES'):
            self.preferences=_PreferencesHelper(self.metadata['APP_PREFERENCES'],'%s/settings.conf' % self.metadata['APP_NAME'],self.ui)
            # Load Application preferences
            self.preferences.load()
        else:
            self.preferences=None
        # Load current icon theme
        self.icon_theme=gtk.icon_theme_get_default()
        # Set current task mode to unknown
        self.__current_task_mode=None
        # Set class as initialized
        self.__initialised=True
        self.__quit=False
        # Dialog module initialization
        if dialogs:
            self.dialogs=DialogFactory(self,self.widgets.winMain)
        # Call application initialization method passing extra parameters
        self.initialize(**kwargs)

    def __setattr__(self,name,value):
        """
        Set attribute method overload for protecting of class specific attributes
        """
        # Check if we are trying to set a protected property
        if name not in ['widgets','ui','preferences','__notifications'] or not self.__dict__.has_key('_GUIClass__initialised'):
            return super(GUIClass,self).__setattr__(name,value)
        else:
            raise Exception(_('EVOGTK: Setting to %s property is not allowed') % name)

    def __connect_signals(self):
        """
        Connects the GUI signals
        """
        # Add default handlers to callbacks
        defaulthandlerlist=['gtk_widget_show','gtk_widget_hide','gtk_widget_grab_focus','gtk_widget_destroy','gtk_true','gtk_false','gtk_main_quit']
        for handler in defaulthandlerlist:
            if not vars(self).has_key(handler):
                vars(self)[handler]=vars(defaulthandlers)[handler]
        # Connect signals
        self.__builder_instance.connect_signals(self)

    def __control_c_handler(self,*args,**kwargs):
        """
        Catches when the user uses Ctrl+C to finish application and launchs the quit method
        """
        self.quit(userbreak=True)

    def show_splash(self,splashimg='splash.png',seconds=3):
        """
        Shows an splash screen using an image
        """
        if not self.__debug:
            splash=gtk.Window(type=gtk.WINDOW_POPUP)
            splash.set_resizable(False)
            splash.set_keep_above(True)
            splash.set_position(gtk.WIN_POS_CENTER)
            splash.add(gtk.image_new_from_file(self.PIXMAPS_DIR + '/' + splashimg))
            splash.show_all()
            self.__splashscreen=(splash,seconds)

    def hide_splash(self,callback=None):
        """
        Hides the splash screen
        """
        if self.__splashscreen:
            self.__splashscreen[0].destroy()
            if callback:
                callback()

    def show_mainwindow(self,window):
        """
        Show main window ant take care about splash screen hiding
        """
        if self.__debug:
            window.show()
        else:
            gobject.timeout_add_seconds(self.__splashscreen[1],self.hide_splash,window.show)

    def set_gui_task(self,mode):
        """
        Setups GUI for an specified task
        """
        if self.TASKS_MODES.has_key(mode):
            self.__current_task_mode=mode
            task=self.TASKS_MODES[mode]
            # Disable widgets
            for widget in task['disable']:
                self.widgets.get_widget(widget).set_sensitive(False)
            # Hide widgets
            for widget in task['hide']:
                self.widgets.get_widget(widget).hide()
            # Enable widgets
            for widget in task['enable']:
                self.widgets.get_widget(widget).set_sensitive(True)
            # Show widgets
            for widget in task['show']:
                self.widgets.get_widget(widget).show()
            # Activate widgets
            for widget in task['activate']:
                self.widgets.get_widget(widget).set_active(True)
            # Deactivate widgets
            for widget in task['deactivate']:
                self.widgets.get_widget(widget).set_active(False)
            # Call specific callback
            if task['callback']:
                getattr(self,task['callback'])()
        else:
            raise Exception(_('EVOGTK: Trying to setup unspecified GUI task mode: %s') % mode)

    def get_gui_task(self):
        """
        Returns current GUI task mode
        """
        return self.__current_task_mode

    def initialize(self):
        """
        Dummy initialize method for application
        """
        pass

    def set_environment(self,env,strict=True):
        """
        Set application environment if needed
        """
        for var in env:
            if self.__dict__.has_key(var):
                if not strict:
                    print _('EVOGTK: Setting member %s from environment initialization to an already set property or method') % var
                if strict:
                    raise Exception(_('EVOGTK: Setting member %s from environment initialization to an already set property or method') % var)
            elif var in ['widgets','ui','preferences','trayicon','notify']:
                raise Exception(_('EVOGTK: Setting varable %s from environment initialization to a protected property is not allowed') % var)       
            self.__dict__[var]=env[var]

    def run(self):
        """
        Launch main application loop
        """
        if self.__main_app:
            EVOGTK_SETTINGS=gtk.settings_get_default()
            EVOGTK_SETTINGS.set_property('gtk-button-images',True)
            gtk.main()
        else:
            raise Exception(_('EVOGTK: Trying to run an application that is not a main application'))

    def quit(self,userbreak=False,status=0):
        """
        Finish application
        
        :param userbreak: Allow user to use Ctrl-C to finish application
        :type userbreak: bool
        :param status: Specifies which status code is returned on application quit
        :type status: int
        
        .. warning:: This method will try to quit application, and will wait for all threads to finish.
            So if you have threads working, application will remain stopped while waiting. 
        """
        # Call application unload callback
        self.unload()
        # Quit application
        if not self.__quit:
            self.__quit=(True,userbreak)
            # Check if there are pending tasks
            if self.__main_app and threadtasks.pending_tasks()>1:
                # Generate the progress bar
                align=gtk.Alignment(xalign=0.5, yalign=0.5, xscale=1, yscale=1)
                align.set_padding(25,25,25,25)
                progress=gtk.ProgressBar()
                progress.set_text(_('Waiting for pending tasks to finish'))
                align.add(progress)
                # Callback for not quit until all pending tasks are finished
                def wait_for_tasks(progress):
                    if threadtasks.pending_tasks()==1:
                        if gtk.main_level():
                            gtk.main_quit()
                        sys.exit(status)
                    progress.pulse()
                    return True
                # Set all widgets to insensitive status
                self.widgets.disable_toplevels()
                # Callback for timeout on waiting for tasks
                gobject.timeout_add(100,wait_for_tasks,progress,priority=gobject.PRIORITY_HIGH)
                # Launch a permanent notification
                if self.notifsys:
                    self.notifsys.queue_custom(align,permanent=True)                
                # If the user used CTRL+C to quit, show message and run gtk loop to make application responsive
                if userbreak:
                    print _('EVOGTK: Finishing tasks, please wait or press CTRL+C again to finish')
                    gtk.main()
            elif self.__main_app:
                if gtk.main_level():
                    gtk.main_quit()
                sys.exit(status)
        else:
            if not self.__quit[1]:
                print _('EVOGTK: Finishing tasks, please wait or press CTRL+C again to finish')
                gtk.main()

    def unload(self):
        """
        Dummy cleanup method for application finish
        
        .. note:: This method should be overloaded mostly for use in plugins
        """
        pass
    
    def debug_status(self):
        """
        Returns debug setting
        """
        return self.__debug
    
    #===========================================================================
    # Default application event handlers
    #===========================================================================

    def showAbout(self,widget=None):
        """
        Show default about dialog
        """
        self.dialogs.aboutDialog(self.metadata)
        return True

    def quitApplication(self,widget,event=None):
        """
        Show default quit dialog
        """
        if self.dialogs.msgDialog(_('¿Do you want to exit %s?') % self.metadata['APP_NAME'], 'question',default=gtk.RESPONSE_NO):
            self.savePreferences()
            self.quit()
        return True

    def showPreferences(self,widget=None):
        """
        Show preferences dialog
        """
        if self.widgets.widget_exists('winPreferences'):
            if self.dialogs.openDialog(self.widgets.winPreferences, close=True)==1:
                self.savePreferences()

    def savePreferences(self,widget=None):
        """
        Save application preferences
        """
        if self.preferences:
            self.preferences.save()
        return True
