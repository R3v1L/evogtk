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
# preferences
# Preferences helper class
###############################################################################
# optionstruct={
#     # Link between sections, options, data types and widgets
#     'optsection': {
#         'optname': ('opttype','optWidgetName',defaultoptvalue),
#     }
# }
# Access to configuration options:
#     gui.preferences.section.option
###############################################################################

# Python imports
import os
import ConfigParser

class _PreferencesHelper(object):
    """
    Preferences helper class
    """
    def __init__(self,optionstruct,configfile,guidata):
        """
        Class constructor
        """
        if os.name == 'posix':
            self.__configfile=os.path.normpath('%s/.%s' % (os.path.expanduser('~'),configfile))
        else:
            self.__configfile=os.path.normpath('%s/%s' % (os.path.expanduser('~'),configfile))
        self.__optionstruct=optionstruct
        self.__guidata=guidata
        # Create configuration parser
        self.__config=ConfigParser.SafeConfigParser()
        # Create sections
        for section in self.__optionstruct:
            # Create section class
            vars(self)[section]=_PreferencesSection(self.__config,section,optionstruct[section],guidata)

    def __create_default_config(self):
        """
        Creates the default configuration file with default values
        """
        if not os.path.exists(self.__configfile):
            path=os.path.dirname(self.__configfile)
            try:
                os.makedirs(path)
            except:
                pass
            if os.path.exists(path):
                self.save(defaults=True)

    def load(self,filename=None):
        """
        Load preferences values and set corresponding widgets
        """
        if not filename:
            if self.__configfile:
                filename=self.__configfile
                self.__create_default_config()
            else:
                raise Exception('(EVOGTK - Preferences Helper) Need a filename for loading preferences')
        # Load file in config parser
        self.__config.read(filename)
        # Load sections and options
        for section in self.__optionstruct:
            for option in self.__optionstruct[section]:
                type=self.__optionstruct[section][option][0]
                widgets=self.__optionstruct[section][option][1]
                value=vars(self)[section].get_option(option)
                # Set widgets to value
                for widget in widgets:
                    self.__guidata.__setattr__(widget,value)
            
    def save(self,filename=None,defaults=False):
        """
        Save preferences to config file
        """
        # Check filename or use default filename
        if not filename:
            if self.__configfile:
                filename=self.__configfile
            else:
                raise Exception('(EVOGTK - Preferences Helper) Need a filename for saving preferences')
            # Set widget values on config parser
            for section in self.__optionstruct:
                for option in self.__optionstruct[section]:
                    widgets=self.__optionstruct[section][option][1]
                    if not defaults and widgets:
                        # Use widget value
                        value=self.__guidata.__getattr__(widgets[0])
                    else:
                        # Use internal value
                        value=vars(self)[section].get_option(option)
                    # Create section in file if not exists
                    if not self.__config.has_section(section):
                        self.__config.add_section(section)
                    value=vars(self)[section].set_option(option,value)
        # Write config to file
        fd=open(filename,'wb')
        self.__config.write(fd)
        fd.close()

class _PreferencesSection(object):
    """
    Preferences Section Helper Class
    """
    def __init__(self,config,section,options,guidata):
        """
        Class constructor
        """
        self.__config=config
        self.__section=section
        self.__options=options
        self.__guidata=guidata
        # Set class as initialized
        self.__initialised=True
        
    def __getattr__(self,name):
        """
        Get attribute method overload for accesing options
        """
        # Check if we are getting an option
        if name not in ['_PreferencesSection__section','_PreferencesSection__options',
                        '_PreferencesSection__config','_PreferencesSection__initialised','_PreferencesSection__get_option','_PreferencesSection__set_option']:
            if not self.__options.has_key(name):
                raise AttributeError('(EVOGTK - Preferences Helper) Preferences object has no attribute \'%s\'' % name)
            # Get option value
            return self.get_option(name)
        else:
            # Call original __getattr__ method
            return super(_PreferencesSection,self).__getattr__(name)
        
    def __setattr__(self,name,value):
        """
        Set attribute method overload for setting options content
        """
        # Assignment during initialisation
        if not self.__dict__.has_key('_PreferencesSection__initialised'):
            self.__dict__[name]=value
            return self.__dict__[name]
        # Assignment after initialisation
        if name not in ['_PreferencesSection__section','_PreferencesSection__options',
                        '_PreferencesSection__config','_PreferencesSection__initialised','__get_option','__set_option']:
            # Set option value
            return self.set_option(name,value)
        else:
            # Call original __setattr__ method
            raise Exception('(EVOGTK - Preferences Helper) Trying to set protected "%s" property' % name)

    def __check_option(self,name):
        """
        Checks if an option exists and give it's data to caller
        """
        # Check if option exists
        if not self.__options.has_key(name):
            raise AttributeError('(EVOGTK - Preferences Helper) Preferences object has no attribute \'%s\'' % name)
        # Check for option type
        if self.__options[name][0] not in ['str','int','float','bool']:
            raise TypeError('(EVOGTK - Preferences Helper) Inconsistent data type \'%s\' for option \'%s\'' % (type,name))        
        return self.__options[name]

    def get_option(self,name):
        """
        Get option value
        """
        opt=self.__check_option(name)
        type=opt[0]
        defaultvalue=opt[2]
        try:
            if type=='str':
                value=self.__config.get(self.__section,name)
            elif type=='int':
                value=self.__config.getint(self.__section,name)
            elif type=='float':
                value=self.__config.getfloat(self.__section,name)
            elif type=='bool':
                value=self.__config.getboolean(self.__section,name)
        except:
            return defaultvalue
        return value

    def set_option(self,name,value):
        """
        Get option value
        """
        opt=self.__check_option(name)
        type=opt[0]
        # Set option depending on type. If we get an error, raise exception
        if type=='str':
            self.__config.set(self.__section,name,str(value))
        elif type=='int':
            self.__config.set(self.__section,name,str(int(value)))
        elif type=='float':
            self.__config.set(self.__section,name,str(float(value)))
        elif type=='bool':
            self.__config.set(self.__section,name,str(bool(value)))
        # Set linked widgets
        for widget in self.__options[name][1]:
            self.__guidata.__setattr__(widget,value)
        return value