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
# threading
# Threading management
###############################################################################

# Python imports
import threading

# GTK Imports
import gobject

# Initialize threads
gobject.threads_init()

# Define task types
TYPE_SIMPLE=0 
TYPE_GENERATOR=1
TYPE_DAEMON=2 
TYPE_CUSTOM=3

class ThreadTask(object):
    """
    Thread task object

    Task types:
        TYPE_SIMPLE (Simple task): Runs task callback, GUI callback and end callback secuentially
        TYPE_GENERATOR (Generator task): Task callback returns a generator using yield. GUI callback
            receives the generator data until generator ends. End callback doesn't receive parameters
            and executes when generator ends.
        TYPE_DAEMON (Daemon task): Run task callback in a forever loop until user calls stop method
            explicitly. GUI callback is called in every loop with task callback return value as parameter.
            End callback doesn't receive parameters and is called after user stopped daemon loop.
        TYPE_CUSTOM (Custom task): Task callback is the only callback running and user take care about
            sending GUI and ending operations to GTK main loop
    """
    def __init__(self,type,task_callback,gui_callback=None,end_callback=None):
        """
        Class initialization
        """
        self.__task_running=False
        self.__task_type=self.__check_task_type(type)
        self.__task_callback=task_callback
        self.__gui_callback=gui_callback
        self.__end_callback=end_callback

    def __check_task_type(self,type):
        """
        Checks if specified task type is known
        """
        if type not in [TYPE_SIMPLE,TYPE_GENERATOR,TYPE_DAEMON,TYPE_CUSTOM]:
            raise Exception('(EVOGTK - Threaded tasks) Invalid task type specified. Must be TYPE_SIMPLE, TYPE_GENERATOR, TYPE_DAEMON or TYPE_CUSTOM')
        else:
            return type

    def __run_generator(self,*args,**kwargs):
        """
        Generator running loop
        """
        # Execute task callback to get the generator
        gen=self.__task_callback(args,kwargs)
        resp=True
        # Loop until generator end
        while resp:
            try:
                resp=gen.next()
            except StopIteration:
                break
            # Execute GUI callback
            if self.__gui_callback:
                gobject.idle_add(self.__gui_callback,*resp)
        # Execute end callback
        if self.__end_callback:
            gobject.idle_add(self.__end_callback)

    def __run_simple(self,*args,**kwargs):
        """
        Simple task running loop
        """
        resp=self.__task_callback(args,kwargs)
        if self.__gui_callback:
            gobject.idle_add(self.__gui_callback,*resp)
        if self.__end_callback:
            gobject.idle_add(self.__end_callback)
 
    def __run_daemon(self,*args,**kwargs):
        """
        Daemon task running loop
        """
        self.__daemon_running=True
        while self.__daemon_running:
            resp=self.__task_callback(args,kwargs)
            if self.__gui_callback:
                gobject.idle_add(self.__gui_callback,*resp)
        if self.__end_callback:
            gobject.idle_add(self.__end_callback)
        
    def __run_wrapper(self,*args,**kwargs):
        """
        Run task according to its type
        """
        # Set task status to running
        self.__task_running=True
        if self.__task_type==TYPE_SIMPLE:
            self.__run_simple(args,kwargs)
        elif self.__task_type==TYPE_GENERATOR:
            self.__run_generator(args,kwargs)
        elif self.__task_type==TYPE_DAEMON:
            self.__run_daemon(args,kwargs)
        elif self.__task_type==TYPE_CUSTOM:
            self.__task_callback(args,kwargs)
        # Set task status to stopped
        self.__task_running=False

    def start(self,*args,**kwargs):
        """
        Generates the thread and starts its execution
        """
        # Generate thread
        self.__thread=threading.Thread(target=self.__run_wrapper,args=args,kwargs=kwargs)
        # Run in daemon mode if type is set to TYPE_DAEMON
        if self.__task_type==TYPE_DAEMON:
            self.__thread.daemon=True
        # Start thread
        self.__thread.start()

    def stop(self):
        """
        Stops the thread and delete it
        """
        self.__daemon_running=False
        
    def is_running(self):
        """
        Returns task running status
        """
        return self.__task_running

def pending_tasks():
    """
    Return total pending tasks
    """
    return threading.active_count()