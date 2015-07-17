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
# dialogs
# Dialog factory class
###############################################################################

# Import GTK
import glib,gobject,gtk

# EVOGTK imports
from evogtk.tools import formatColor,setupComboBox
from evogtk.gui import defaulthandlers

###############################################################################
# Dialog Factory class
###############################################################################
class DialogFactory(object):
    """
    Dialog Factory Class
    """

    # Message dialog mode declarartions
    MSG_DIALOG_MODES={
        'info': (gtk.MESSAGE_INFO,gtk.BUTTONS_OK),
        'warning': (gtk.MESSAGE_WARNING,gtk.BUTTONS_CLOSE),
        'question': (gtk.MESSAGE_WARNING,gtk.BUTTONS_YES_NO),
        'error': (gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE),
    }

    # File chooser dialog mode declarations
    FILE_DIALOG_MODES={
        'open': (gtk.FILE_CHOOSER_ACTION_OPEN,'Open file',
                 ('gtk-cancel',gtk.RESPONSE_CANCEL,'gtk-open',gtk.RESPONSE_OK)),
        'save': (gtk.FILE_CHOOSER_ACTION_SAVE,'Save file',
                 ('gtk-cancel',gtk.RESPONSE_CANCEL,'gtk-save',gtk.RESPONSE_OK)),
        'selfolder': (gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,'Select folder',
                 ('gtk-cancel',gtk.RESPONSE_CANCEL,'gtk-ok',gtk.RESPONSE_OK)),
        'newfolder': (gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER,'Create folder',
                 ('gtk-cancel',gtk.RESPONSE_CANCEL,'gtk-ok',gtk.RESPONSE_OK)),
    }
    
    # Dialog positions
    DIALOG_POSITIONS={
        'none': gtk.WIN_POS_NONE,
        'center': gtk.WIN_POS_CENTER,
        'mouse': gtk.WIN_POS_MOUSE,
        'centeralways': gtk.WIN_POS_CENTER_ALWAYS,
        'centerparent': gtk.WIN_POS_CENTER_ON_PARENT,
    }
   
    ###############################################################################
    # Dialog factory functions
    ###############################################################################
    
    def __init__(self,gui,parent=None,defaultposition=None):
        """
        Class constructor
            parent: Parent window for this dialog factory instance
            defaultposition: Default position for generated dialogs. Can be either:
                center, centerparent, 
        """
        self.gui=gui
        self.parent=parent
        self.position=None
        self.position=self.__dialogposition(defaultposition)
  
    # Dialog position chooser helper
    def __dialogposition(self,position):
        if self.DIALOG_POSITIONS.has_key(position):
            pos=self.DIALOG_POSITIONS[position]
        else:
            if not self.position:
                if self.parent:
                    pos=self.DIALOG_POSITIONS['centerparent']
                else:
                    pos=self.DIALOG_POSITIONS['center']
            else:
                pos=self.position
        return pos

    # Message dialog creation
    def msgDialog(self,msg,mode='info',desc=None,cancel=False,position=None,default=gtk.RESPONSE_OK):
        """
        Shows a message dialog and return a response
            msg: Message to be shown
            mode: Dialog mode. Can be either info (default), warning, question or error
            desc: Secondary message shown under main message text
            cancel: Specifies if a cancel button has to be shown in dialog
            position: Default dialog position
            default: Default response
        Returns:
            True if Yes, Ok or Close button is pressed,
            False if window is deleted, cancel button is pressed or other response is received
        """
        # Check if dialog mode is allowed
        if self.MSG_DIALOG_MODES.has_key(mode):
            mode=self.MSG_DIALOG_MODES[mode]
        else:
            raise TypeError('(EVOGTK - Dialog Factory) msgDialog requires a valid dialog mode.')
        # Dialog creation
        dialog=gtk.MessageDialog(self.parent,gtk.DIALOG_MODAL and gtk.DIALOG_DESTROY_WITH_PARENT,mode[0],mode[1])
        if cancel:
            dialog.add_button('gtk-cancel', gtk.RESPONSE_CANCEL)
        # Add dialog message
        dialog.set_markup('<b>' + glib.markup_escape_text(msg) + '</b>')
        # Add dialog secondary message if specified
        if desc:
            dialog.format_secondary_markup(desc)
        # Set default response and buttons separator
        dialog.set_default_response(default)
        # Set dialog position
        dialog.set_position(self.__dialogposition(position))
        # Show dialog and get the response
        resp=self.openDialog(dialog,delete=True)
        # Response parsing
        if resp==gtk.RESPONSE_OK or resp==gtk.RESPONSE_YES or resp==gtk.RESPONSE_CLOSE:
            resp=True
        else:
            resp=False
        return resp

    def fileSelDialog(self,mode='open',title=None,multiple=False,curfolder=None,buttons=None,position=None,filters=None,default_filter=None,confirm=True):
        """
        Generates a file selection dialog
            mode: Dialog mode. Can be either open (default), save, selfolder or newfolder
            title: Title to be used for the dialog window (by default, the associated mode title is used)
            multiple: Specifies if dialog can select multiple files
            curfolder: Folder that will be shown when the dialog is opened
            buttons: A list of tuples specifying customized buttons in format (button_identifier, button_response)
            filters: Only shows files according to filters. Is a dict in format {'Filter Name': ['Pattern 1','Pattern 2',],}
        Returns:
            A tuple that contains:
                A list of selected filenames or an empty list if the OK/Selection button has not been pressed
                The response value of the pressed button
        """
        # Check if dialog mode is allowed
        if self.FILE_DIALOG_MODES.has_key(mode):
            mode=self.FILE_DIALOG_MODES[mode]
        else:
            raise TypeError('(EVOGTK - Dialog Factory) fileSelDialog requires a valid dialog mode.')
        # Set title
        if not title:
            title=mode[1]
        # Set buttons
        if not buttons:
            buttons=mode[2]
        dialog=gtk.FileChooserDialog(title,self.parent,mode[0],buttons=buttons)
        # Set multiple selection
        dialog.set_select_multiple(multiple)
        # Set current folder
        if curfolder:
            dialog.set_current_folder(curfolder)
        # Set overwrite confirmation
        dialog.set_do_overwrite_confirmation(confirm)
        # Set file filters
        if filters:
            for filter in filters:
                filefilter=gtk.FileFilter()
                filefilter.set_name(filter)
                for pattern in filters[filter]:
                    filefilter.add_pattern(pattern)
                dialog.add_filter(filefilter)
                if filter==default_filter:
                    dialog.set_filter(filefilter)
        # Set default response
        dialog.set_default_response(gtk.RESPONSE_OK)
        # Set dialog position
        dialog.set_position(self.__dialogposition(position))
        # Show dialog and get the response
        files=[]
        resp=self.openDialog(dialog)
        if resp==gtk.RESPONSE_OK:
            # Get filenames list
            files=dialog.get_filenames()
        dialog.destroy()
        return (files,resp)

    def fontSelDialog(self,title='Font selection',fontname=None,previewtext=None,position=None):
        """
        Generates a font selection dialog
            title: Title to be used for the dialog window
            fontname: Font to be selected by default
            previewtext: Text to be used to preview the fonts in the dialog
        Returns:
            The font name string if Ok button pressed or None if dialog is canceled or deleted
        """
        dialog=gtk.FontSelectionDialog(title)
        if fontname:
            dialog.set_font_name(fontname)
        if previewtext:
            dialog.set_preview_text(previewtext)
        # Set default response
        dialog.set_default_response(gtk.RESPONSE_OK)
        # Set dialog position
        dialog.set_position(self.__dialogposition(position))
        # Show dialog and get the response
        resp=self.openDialog(dialog)
        font=None
        if resp==gtk.RESPONSE_OK:
            # Get font name
            font=dialog.get_font_name()
        dialog.destroy()
        return font

    def colorSelDialog(self,title='Color selection',currentcolor='#000',usealpha=False,currentalpha=0,returnfmt='html',position=None):
        """
        Generates a color selection dialog
            title: Title to be used for the dialog window
            currentcolor: Current color in named (red,blue,navajowhite...) or hexadecimal format (#FFF,#FFFFFF,#FFFFFFFFF...)
            usealpha: User can control alpha value
            currentalpha: Current alpha value (0..65535)
            returnfmt: Format of the color to be returned. (See tools.formatcolor Function)
        """
        # Check if return mode is allowed
        dialog=gtk.ColorSelectionDialog(title)
        colorsel=dialog.colorsel
        colorsel.set_has_opacity_control(usealpha)
        colorsel.set_current_alpha(currentalpha)
        setcolor=gtk.gdk.color_parse(currentcolor)
        colorsel.set_current_color(setcolor)
        # Set default response
        dialog.set_default_response(gtk.RESPONSE_OK)
        # Set dialog position
        dialog.set_position(self.__dialogposition(position))
        # Show dialog and get the response
        resp=self.openDialog(dialog)
        color=None
        alpha=None
        if resp==gtk.RESPONSE_OK:
            # Get color
            color=colorsel.get_current_color()
            alpha=colorsel.get_current_alpha()
            dialog.destroy()
            return formatColor(color,alpha,returnfmt)
        dialog.destroy()
        return None

    def aboutDialog(self,metadata,license=None,licensewrap=False,position=None):
        """
        Generates an about dialog
            metadata: Dictionary with application info
                Required keys:
                    APP_NAME: Application name
                    APP_CODENAME: Application codename (Alphanumeric without spaces)
                    APP_DESC: Application short description
                    APP_VERSION: Current version for application
                    APP_COPYRIGHT: Copyright holder of the application
                Optional keys:
                    APP_WEBSITE: Website for the application
                    APP_AUTHORS: List of application authors
                    APP_DOCUMENTERS: List of application documenters
                    APP_ARTISTS: List of application art designers
                    APP_TRANSLATORS: String with application translation credits
                    APP_LOGO: Filename of application logo
            license: License Text. By default, license isn't set
            licensewrap: Specifies if license text must be wrapped. By default, it's disabled.
        """
        # Create dialog
        dialog=gtk.AboutDialog()
        # Load required metadata into the dialog
        dialog.set_name(metadata['APP_NAME'])
        dialog.set_comments(metadata['APP_DESC'])
        dialog.set_version(metadata['APP_VERSION'])
        dialog.set_copyright(metadata['APP_COPYRIGHT'])
        # Load optional metadata into the dialog
        if metadata.has_key('APP_WEBSITE'):
            dialog.set_website(metadata['APP_WEBSITE'])
        # Set authors, doucmenters, artists and traductors
        if metadata.has_key('APP_AUTHORS'):
            dialog.set_authors(metadata['APP_AUTHORS'])
        if metadata.has_key('APP_DOCUMENTERS'):
            dialog.set_documenters(metadata['APP_DOCUMENTERS'])
        if metadata.has_key('APP_ARTISTS'):
            dialog.set_artists(metadata['APP_ARTISTS'])
        if metadata.has_key('APP_TRANSLATORS'):
            dialog.set_translator_credits(metadata['APP_TRANSLATORS'])
        # Loading app logo
        if metadata.has_key('APP_CODENAME'):
            try:
                dialog.set_logo(gtk.gdk.pixbuf_new_from_file(self.gui.PIXMAPS_DIR + '/%s.png' % metadata['APP_CODENAME']))
            except:
                print '(EVOGTK - Dialog Factory) WARNING: Logo filename can not be loaded from %s/%s.png' % (self.gui.PIXMAPS_DIR,metadata['APP_CODENAME'])
        # Load license
        dialog.set_license(license)
        dialog.set_wrap_license(licensewrap)
        # Set dialog default response
        dialog.set_default_response(gtk.RESPONSE_CLOSE)
        # Set dialog position
        dialog.set_position(self.__dialogposition(position))
        # Show dialog and get the response
        resp=self.openDialog(dialog,delete=True)
        return resp==gtk.RESPONSE_CLOSE

    def comboDialog(self,title,options,position=None):
        """
        Generates a dialog with a combo box for selecting an option
        """
        #Generate the dialog
        buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OK,gtk.RESPONSE_OK)
        dialog=gtk.Dialog(title,flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,buttons=buttons)
        # Generate the combo box
        combobox=setupComboBox(options,dialog.vbox)
        # Open dialog and return response
        dialog.set_position(self.__dialogposition(position))
        resp=self.openDialog(dialog, delete=True)
        return (combobox.get_active_text(),resp==gtk.RESPONSE_OK)

    def categoryListDialog(self,title,options,header='',width=250,height=400,position=None):
        """
        Generates a dialog with a combo box and a list for selecting a category and an option
        """
        #Generate the dialog
        buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OK,gtk.RESPONSE_OK)
        dialog=gtk.Dialog(title,flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,buttons=buttons)
        # Generate the combo box
        combobox=setupComboBox(options,dialog.vbox,pack_start=True,expand=False,fill=False)      
        # Generate the scroll
        scroll=gtk.ScrolledWindow()
        dialog.vbox.pack_start(scroll, True, True, 0)
        scroll.show()
        # Generate the list
        liststore=gtk.ListStore(str)
        treeview=gtk.TreeView(liststore)
        tvcolumn=gtk.TreeViewColumn(header)
        treeview.append_column(tvcolumn)
        cell=gtk.CellRendererText()
        tvcolumn.pack_start(cell,True)
        tvcolumn.add_attribute(cell, 'text', 0)
        scroll.add(treeview)
        # Show header if specified
        if not header:
            treeview.set_headers_visible(False)
        treeview.show()
        # Associate event for changing list contents when change the category
        def LoadListContents(widget):
            # Clear actual data in list
            liststore.clear()
            categ=combobox.get_active_text()
            for option in options[categ]:
                liststore.append((option,))
        combobox.connect('changed',LoadListContents)
        # Associate event to activate the current row
        def ActivateRow(widget,iter,col):
            dialog.response(gtk.RESPONSE_OK)
        treeview.connect('row_activated',ActivateRow)
        # Establish dialog size
        dialog.resize(width,height)
        # Select first category
        combobox.set_active(0)
        # Open dialog and return response
        dialog.set_position(self.__dialogposition(position))
        resp=self.openDialog(dialog)        
        model,iter=treeview.get_selection().get_selected()
        # Fix problem with categorylist dialog
        if iter:
            selected=model.get_value(iter,0)
            self.closeDialog(dialog, delete=True)        
            return (combobox.get_active_text(),selected,resp==gtk.RESPONSE_OK)
        else:
            self.closeDialog(dialog, delete=True)
            return (None,None,False)

    # Message dialog creation
    def statusDialog(self,title,msg,callback=None,pulse_delay=100,cancel=False):
        """
        Generates a status dialog that locks the GUI until application hides it
            msg: Message to be shown
            cancel: Specifies if a cancel button has to be shown in dialog
        Returns:
            The status dialog
        """
        # Generate the dialog
        buttons=None
        if cancel:
            buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OK,gtk.RESPONSE_OK)
        dialog=gtk.Dialog(title,flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,buttons=buttons)
        # Cancel delete events
        dialog.connect('delete-event',defaulthandlers.gtk_true)
        # Generate the progress bar
        dialog.progress=gtk.ProgressBar()
        dialog.progress.set_text(msg)
        dialog.vbox.pack_start(dialog.progress)
        # Show widgets
        dialog.vbox.show_all()

        # Callback for dialog pulses
        dialog.callback=callback
        if not callback:            
            def __callback(dialog=False):
                if dialog:
                    dialog.progress.pulse()
                    return True
            dialog.callback=__callback
            dialog.finish=__callback

        # Setup callback for dialog pulses into gtk main loop
        gobject.timeout_add(pulse_delay,dialog.callback,dialog,priority=gobject.PRIORITY_HIGH)
        return dialog

    def setParent(self,parent):
        """
        Set parent widget
        """
        self.parent=parent

    def setPosition(self,position):
        """
        Set parent widget
        """
        self.position=self.__dialogposition(position)

    # Dialog opening helper function
    def openDialog(self,dialog,delete=False,close=False,delresponse=gtk.RESPONSE_DELETE_EVENT,position=None):
        """
        Open a dialog and gets a response
        """
        # Set dialog position
        dialog.set_position(self.__dialogposition(position))
        resp=dialog.run()
        if resp==delresponse or close or delete:
            self.closeDialog(dialog,delete=delete)
        return resp

    # Dialog closing helper function
    def closeDialog(self,dialog,delete=False):
        """
        Close a dialog
        """
        if delete:
            dialog.destroy()
        else:
            dialog.hide()
        return True
