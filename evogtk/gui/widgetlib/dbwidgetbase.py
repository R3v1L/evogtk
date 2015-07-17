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
# dbwidgetbase
# Database widget base class module
###############################################################################

# GTK Imports
import gobject

class DBWidgetBase(gobject.GObject):
    """
    Database gtk.CheckButton widget
    """
    __gtype_name__ = 'DBWidgetBase'
    # Widget properties
    __properties = {
        'db-table-name' : (gobject.TYPE_STRING,'Database Table name','Database table name for data','',gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
        'db-field-name' : (gobject.TYPE_STRING,'Database Field name','Database field name for data','',gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
        'help-text': (gobject.TYPE_STRING,'Help text','Help text of this widget','Help text',gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
        'inmediate-validation': (gobject.TYPE_BOOLEAN,'Inmediate validation','Validate data inmediately on every change',True,gobject.PARAM_CONSTRUCT | gobject.PARAM_READWRITE),
    }
    __gproperties__ = __properties    

    def __init__(self):
        """
        Class initialization
        """
        # Widget data
        self.table_name=''
        self.field_name=''
        self.help_text='Help text'
        self.inmediate_validation=True
        # Validators
        self.__validators=[]
        self.__validation_errors=[]

    def get_validation_errors(self):
        """
        Returns validation errors list
        """
        return self.__validation_errors

    def get_validation_errors_text(self):
        """
        Generates tooltip text from validation errors or help text
        """
        if self.__validation_errors:
            errorstext=''
            for error in self.__validation_errors:
                errorstext+=error + '\n'    
            return errorstext[:-1]
        return ''

    def get_widget_data(self):
        """
        Returns data stored in the widget to be validated
        """
        pass

    def set_invalidated(self):
        """
        Set this widget as invalidated
        """        
        pass
    
    def set_validated(self):
        """
        Set this widget as validated
        """
        pass

    def validate(self,*args,**kwargs):
        """
        Validates user data
        """
        self.__validation_errors=[]
        if self.__validators:
            for validator in self.__validators:
                result=validator(self.get_widget_data())
                if result:
                    self.__validation_errors.append(result)
            if self.__validation_errors:
                self.set_property('tooltip-markup',self.get_validation_errors_text())
                self.set_invalidated()
            else:
                self.set_property('tooltip-markup',self.help_text)
                self.set_validated()
        return self.__validation_errors
    
    def add_validators(self,*validators):
        """
        Adds a validator to the widget
        """
        for validator in validators:
            if not self.__validators.count(validator):
                self.__validators.append(validator)

    def get_validators(self):
        """
        Returns all validators in a list
        """
        return self.__validators

    def remove_validators(self,*validators):
        """
        Removes a validator from the widget
        """
        for validator in validators:
            while self.__validators.count(validator):
                self.__validators.remove(validator)

    def do_get_property(self, property):
        """
        Property getting value handling
        """
        if property.name=='table-name':
            return self.table_name
        elif property.name=='field-name':
            return self.field_name
        elif property.name=='help-text':
            return self.help_text
        elif property.name=='inmediate-validation':
            return self.inmediate_validation

    def do_set_property(self, property, value):
        """
        Property setting value handling
        """
        if property.name=='table-name':
            self.tablename=value
        elif property.name=='field-name':
            self.fieldname=value
        elif property.name=='help-text':
            self.help_text=value
            self.set_tooltip_markup(value)
        elif property.name=='inmediate-validation':
            self.inmediate_validation=value

gobject.type_register(DBWidgetBase)