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
# srceditor
# EVOGTK Source editor widget
###############################################################################

# GTK Imports
import gobject,gtk,pango

# EVOGTK Imports
import evogtk

# GTK Source Editor Imports
if evogtk.HAS_GTKSOURCEVIEW:
    import gtksourceview2 as gtksourceview

class SourceEditor(gtk.VBox):
    """
    Sourceview enhanced widget class
    """
    __gtype_name__ = 'SourceEditor'
    
    __gsignals__ = { 
        'status-updated' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,())
    }
    
    class SourceEditorStatus(object):
        """
        Editor status class
        """
        line=0
        offset=0
        overwrite=False
        modified=False
        selection=False
        undo=False
        redo=False
        
    def __init__(self):
        """
        Initialization
        """
        # Check if we have GTKSourceview support before initialising
        if not evogtk.HAS_GTKSOURCEVIEW:
            raise ImportError('(EVOGTK) There is no support for Source Editor Widget without GTKSourceview support')
        # Initialize parent class
        gtk.VBox.__init__(self)
        # Create scroll for editor
        self.__scroll=gtk.ScrolledWindow(gtk.Adjustment(),gtk.Adjustment())
        # Get default language manager
        self.__langmanager=gtksourceview.language_manager_get_default()
        # Initialize source buffer
        self.__srcbuffer=gtksourceview.Buffer()
        # Initialize source view
        self.__srcview=gtksourceview.View()
        self.__srcview.set_buffer(self.__srcbuffer)
        # Widget packing
        self.__scroll.add(self.__srcview)
        self.pack_start(self.__scroll)
        # Connect signals for status updating
        signals={
            self.__srcbuffer: ['modified-changed','changed'],
            self.__srcview: ['move-cursor','toggle-overwrite','key-press-event','key-release-event','button-press-event','button-release-event'],
        }
        for obj in signals.keys():
            for signal in signals[obj]:
                obj.connect(signal,self.__update_status)     
        # Show widget contents   
        self.show_all()
        # Update status data
        self.__status=self.SourceEditorStatus()

    def __update_status(self,*args,**kwargs):
        """
        Updates status data
        """
        self.emit('status-updated')

    #===========================================================================
    # Configuration methods
    #===========================================================================
    def set_font(self,fontdesc):
        """
        Sets the editor general font
        """
        self.__srcview.modify_font(pango.FontDescription(fontdesc))
        
    def line_numbers(self,status=True):
        """
        Wrapper for line numbers method of the sourceview
        """
        self.__srcview.set_show_line_numbers(status)

    def line_markers(self,status=True):
        """
        Wrapper for line markers method of the sourceview
        """
        self.__srcview.set_show_line_marks(status)
    
    def margin(self,pos=80,status=True):
        """
        Wrapper for setting the margin of the sourceview
        """
        self.__srcview.set_right_margin_position(pos)
        self.__srcview.set_right_margin(status)

    def auto_indent(self,status=True):
        """
        Wrapper for setting automatic indentation in sourceview
        """
        self.__srcview.set_auto_indent(status)
        
    def tab_spaces(self,width=4,use_spaces=True):
        """
        Wrapper for using spaces instead of tabs
        """
        self.__srcview.set_tab_width(width)
        self.__srcview.set_insert_spaces_instead_of_tabs(use_spaces)
        
    def smart_home_end(self,status=True):
        """
        Wrapper for setting smart home and end keys
        """
        self.__srcview.set_smart_home_end(status)

    def highlight_current_line(self,status):
        """
        Wrapper for current line highlighting method of the sourceview
        """
        self.__srcview.set_highlight_current_line(True)

    def editable(self,status=True):
        """
        Wrapper for set editable method of the sourceview
        """
        self.__srcview.set_editable(status)

    def cursor_visible(self,status=True):
        """
        Wrapper for setting the cursor visibility on the sourceview
        """
        self.__srcview.set_cursor_visible(status)

    def highlight_syntax(self,status=True):
        """
        Wrapper for syntax highligting method of the sourcebuffer
        """
        self.__srcbuffer.set_highlight_syntax(status)

    def check_brackets(self,status=True):
        """
        Sets check for matching brackets
        """
        self.__srcbuffer.set_highlight_matching_brackets(status)

    def max_undo_levels(self,levels=50):
        """
        Wrapper for setting the maximum undo levels in sourcebuffer
        """
        self.__srcbuffer.set_max_undo_levels(levels)

    def current_language(self,langid,highlight=True):
        """
        Sets the programming language for the buffer
        """
        lang=self.__langmanager.get_language(langid)
        if lang:
            self.__srcbuffer.set_language(lang)
        else:
            raise Exception('EVOGTK - SourceEditor: Specified language %s is not supported' % lang)
        # Set syntax highlighting
        self.highlight_syntax(highlight)

    #===========================================================================
    # Editing methods
    #===========================================================================
    def undo(self):
        """
        Undo last action
        """
        if self.__srcbuffer.can_undo():
            self.__srcbuffer.undo()
            return True
        return False
    
    def redo(self):
        """
        Redo last undone action
        """
        if self.__srcbuffer.can_redo():
            self.__srcbuffer.redo()
            return True
        return False
    
    def select_all(self):
        """
        Select all the contents of the editor
        """
        self.__srcbuffer.select_range(*self.__srcbuffer.get_bounds())

    def go_to_line(self,line):
        """
        Go to the specified line
        """
        lines=self.__srcbuffer.get_line_count()
        if line>lines:
            line=lines
        cur=self.__srcbuffer.get_iter_at_line(line-1)
        self.__srcbuffer.place_cursor(cur)
        self.__srcview.scroll_to_iter(cur,0.4)

    def get_selection_text(self):
        """
        Get selected text
        """
        if self.__srcbuffer.get_has_selection():
            return self.__srcbuffer.get_text(*self.__srcbuffer.get_selection_bounds())
        else:
            return None

    def replace_selected(self,text):
        """
        Replace selected text with another given text
        """
        self.delete()
        self.__srcbuffer.insert_at_cursor(text.upper())

    def to_upper(self):
        """
        Convert selected text to uppercase
        """
        self.__srcbuffer.begin_user_action()
        text=self.get_selection_text()
        if text:
            self.replace_selected(text.upper())
        self.__srcbuffer.end_user_action()
    
    def to_lower(self):
        """
        Convert selected text to lowercase
        """
        self.__srcbuffer.begin_user_action()
        text=self.get_selection_text()
        if text:
            self.replace_selected(text.lower())
        self.__srcbuffer.end_user_action()

    def cut(self,clipboard):
        """
        Cut selected text to clipboard
        """
        if self.__srcbuffer.get_has_selection():
            self.__srcbuffer.cut_clipboard(clipboard,True)
    
    def copy(self,clipboard):
        """
        Copy selected text to clipboard
        """
        if self.__srcbuffer.get_has_selection():
            self.__srcbuffer.copy_clipboard(clipboard)
    
    def paste(self,clipboard):
        """
        Paste clipboard text to current cursor position
        """
        self.__srcbuffer.paste_clipboard(clipboard, None, True)
    
    def delete(self):
        """
        Delete selected text
        """
        if self.__srcbuffer.get_has_selection():
            self.__srcbuffer.delete_selection(False, False)

    def unselect(self):
        """
        Unselect current selection
        """
        if self.__srcbuffer.get_has_selection():
            self.__srcbuffer.place_cursor(self.__srcbuffer.get_selection_bounds()[1])

    def clear(self):
        """
        Clear text buffer
        """
        self.__srcbuffer.delete(*self.__srcbuffer.get_bounds())

    def set_modified(self,status=True):
        """
        Sets source buffer as modified based on status
        """
        self.__srcbuffer.set_modified(status)

    #===========================================================================
    # Main methods
    #===========================================================================    
    def load_file(self,path,langid=None,highlight=True,guess=True):
        """
        Load a file on the source editor
        """
        # Set editor language and syntax highlighting if enabled
        if not langid:
            if guess:
                langid=self.guess_language(path)
        if langid:
            self.current_language(langid,highlight)
        # Load file contents
        fd=open(path,'r')
        self.__srcbuffer.set_text(fd.read())
        fd.close()
        self.set_modified(False)

    def save_file(self,path):
        """
        Save a file with source editor contents
        """
        # Load file contents
        if self.__srcbuffer.get_modified():
            fd=open(path,'w')
            fd.write(self.__srcbuffer.get_text(*self.__srcbuffer.get_bounds()))
            fd.close()
            self.set_modified(False)

    def get_status(self):
        """
        Returns a dictionary with status data
        """
        # Cursor line and offset
        self.__status.overwrite=self.__srcview.get_overwrite()
        self.__status.modified=self.__srcbuffer.get_modified()
        self.__status.selection=self.__srcbuffer.get_has_selection()
        self.__status.undo=self.__srcbuffer.can_undo()
        self.__status.redo=self.__srcbuffer.can_redo()
        # Get current line and offset
        curiter=self.__srcbuffer.get_iter_at_offset(self.__srcbuffer.get_property('cursor-position'))
        self.__status.line=curiter.get_line()
        self.__status.offset=curiter.get_line_offset()    
        return self.__status

    def guess_language(self,filename):
        """
        Wrapper for guess_language method of the language manager
        """
        lang=self.__langmanager.guess_language(filename)
        if lang:
            return lang.get_id()
        else:
            return None

    def supported_languages(self):
        """
        Returns a dictionary with all supported language ids as keys and their names as values
        """
        ids=self.__langmanager.get_language_ids()
        langs={}
        for id in ids:
            lang=self.__langmanager.get_language(id)
            langs['id']=lang.get_name()
        return langs
    
    def grab_focus(self):
        """
        Set the focus on the source view
        """
        self.__srcview.grab_focus()