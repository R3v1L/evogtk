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
# excepthandler
# Unhandled exception catcher and handling class
###############################################################################

# Python imports
import sys
import traceback

# GTK imports
import gobject
import gtk

# EVOGTK imports
import evogtk
from evogtk import tools

class _ExceptionHandler(object):
    """
    Exception catcher class
    """
    def __init__(self,catch_all=False):
        """
        Class initialization
        """
        self.__catch_all=catch_all
        # Catched exceptions dict
        self.__exception_handlers={}
        # Save original exception hook
        self.__orig_execpthook=sys.excepthook
        # Set new exception hook 
        sys.excepthook=self.__excepthook
        
    def __excepthook(self,type,value,trace):
        """
        Exception handling method
        """
        handler=self.get_handler(type)
        if not handler and self.__catch_all:   
            self.__default_handler(type,value,trace)
        elif handler:
            handler(type,value,trace)
        else:
            self.__orig_execpthook(type,value,trace)

    def __default_handler(self,type,value,trace):
        """
        Default exception handling method
        """
        # Extract traceback information
        stack=traceback.extract_tb(trace)
        dialog=gtk.MessageDialog(None,gtk.DIALOG_MODAL and gtk.DIALOG_DESTROY_WITH_PARENT,gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE)
        # Add dialog message
        dialog.set_markup('<b>%s</b>' % gobject.markup_escape_text(str(value).capitalize()))
        # Add dialog secondary message if specified
        if stack:
            dialog.format_secondary_markup('Stack trace follows')
        # Generate stack trace
        vbox=gtk.VBox(spacing=5)
        for calldata in stack:
            vbox.pack_start(self.__generate_stack_trace(calldata))
        dialog.get_content_area().pack_start(vbox,True,True)
        vbox.show_all()
        # Set dialog position and resizable
        dialog.set_position(gtk.WIN_POS_CENTER)
        dialog.set_resizable(True)
        # Show dialog and get the response
        dialog.run()
        dialog.destroy()

    def __generate_stack_trace(self,calldata):
        """
        Generates the widget structure for the stack trace
        """
        lbl=gtk.Label()
        lbl.set_markup('File: <b>%s</b>' % gobject.markup_escape_text(calldata[0]))
        fra=gtk.Frame()
        fra.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        fra.set_label_widget(lbl)
        lbl=gtk.Label()
        lbl.set_markup('<i>Line <b>%s</b> in <b>%s</b></i>' % (calldata[1],gobject.markup_escape_text(calldata[2])))
        exp=gtk.Expander()
        exp.set_label_widget(lbl)
        exp.set_expanded(True)
        exp.add(self.__generate_code_widget(calldata[0],calldata[1]))
        fra.add(exp)
        return fra

    def __generate_code_widget(self,file,linenum):
        """
        Generates a source code view
        """
        scr=gtk.ScrolledWindow(gtk.Adjustment(),gtk.Adjustment())
        scr.set_policy(gtk.POLICY_ALWAYS,gtk.POLICY_ALWAYS)
        # Check if we use GTK Sourceview for code widget
        if evogtk.HAS_GTKSOURCEVIEW:
            # Use GTK Sourceview
            import gtksourceview2
            buffer=gtksourceview2.Buffer()
            view=gtksourceview2.View(buffer)
            view.set_show_line_numbers(True)
            view.set_highlight_current_line(True)
            # Set code highlighting
            lm=gtksourceview2.language_manager_get_default()
            lang=lm.get_language('python')
            if lang:
                buffer.set_language(lang)
                buffer.set_highlight_syntax(True)
        else:
            # Use GTK TextView
            buffer=gtk.TextBuffer()
            view=gtk.TextView(buffer)
        # Set view basic parameters
        view.set_editable(False)
        view.set_cursor_visible(False)
        # Pack widgets
        scr.add(view)
        # Set buffer contents
        mark=self.__set_buffer_code(buffer, file, linenum)
        # Scroll to line
        view.scroll_to_mark(mark,0,use_align=True)
        return scr

    def __set_buffer_code(self,buffer,file,linenum,before=3,after=3):
        """
        Gets the code surrounding a selected line
        """
        # Check if file exists and is a .py file
        # Generate tags for code window
        tools.newTextTag({'name': 'normal','family': 'courier'},buffer)
        tools.newTextTag({'name': 'current','family': 'courier','background': 'yellow','weight': 700},buffer)
        # Open file
        fd=open(file,'r')
        # Read lines
        count=0
        for line in fd:
            count+=1
            # Add code to buffer
            if count==linenum:
                iter=buffer.get_end_iter()
                # Set mark for later scrolling
                mark=buffer.create_mark(None,iter,True)
                buffer.insert_with_tags_by_name(iter,line,'current')
                #buffer.insert(iter,line)   
            else: # count > linenum-before and count < linenum+after:
                iter=buffer.get_end_iter()
                buffer.insert_with_tags_by_name(iter,line,'normal')
                #buffer.insert(iter,line)   
        # Set cursor at line number and return mark to current line
        buffer.place_cursor(buffer.get_iter_at_line(linenum-1))
        return mark

    def set_handler(self,except_type,except_handler):
        """
        Assigns a new exception handler
        """
        if self.__exception_handlers.has_key(except_type):
            raise Exception('(EVOGTK - Exception handler) Trying to set an already set handler. Use remove first to set a new handler')
        self.__exception_handlers[except_type]=except_handler
        
    def get_handler(self,except_type):
        """
        Gets the current exception handler for an exception type
        """
        if self.__exception_handlers.has_key(except_type):
            return self.__exception_handlers[except_type]
        else:
            return None

    def remove_handler(self,except_type):
        """
        Removes an exception handler
        """
        if self.__exception_handlers.has_key(except_type):
            del(self.__exception_handlers[except_type])
