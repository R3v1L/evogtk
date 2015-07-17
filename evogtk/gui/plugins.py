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
# plugins
# Plugin system class
###############################################################################

# Python Imports
import os

# EVOGTK Imports
import evogtk

class PluginLoader(object):
    """
    Plugin factory class
    """
    
    def __init__(self,plugindir=evogtk.DEFAULT_PLUGIN_DIR):
        """
        Class initialization
        """
        # Generate plugin list
        self.__plugindir=plugindir
        self.__plugins={}

    def plugin_list(self):
        """
        Method for getting available plugins list from plugindir
        """
        pluginlist=[]
        filelist=os.listdir(self.__plugindir)
        for file in filelist:
            if os.path.isdir('%s/%s' % (self.__plugindir,file)):
                if os.path.exists('%s/%s/__init__.py' % (self.__plugindir,file)):
                    pluginlist.append(file)
        return pluginlist

    def loaded_plugins(self):
        """
        Method for getting loaded plugins list
        """
        return self.__plugins.keys()

    def load_plugin(self,pluginname,env={}):
        """
        Method for plugin loading
        """
        # Load plugin module
        try:
            module=__import__('%s.%s' % (self.__plugindir,pluginname),globals(),locals(),[pluginname],0)
        except:
            raise Exception('(EVOGTK - Plugins) Can\'t load plugin named %s' % pluginname)
        self.__plugins[pluginname]=module.Plugin
        if module.Plugin.metadata.has_key('PLUGIN_DOCK'):
            # Add plugin instance as a class property
            self.__dict__[pluginname]=module.Plugin(['%s/%s/%s.ui' % (self.__plugindir,pluginname,pluginname)],env=env)
        else:
            # Plugin simple class
            self.__dict__[pluginname]=module.Plugin(env=env)

    def get_plugin_instance(self,pluginname):
        """
        Method for accessing plugin instance by name
        """
        if self.__plugins.has_key(pluginname):
            return self.__dict__[pluginname]
        else:
            raise Exception('(EVOGTK - Plugins) There is no loaded plugin called "%s"' % pluginname)

    def get_plugin_class(self,pluginname):
        """
        Method for accessing plugin class by name
        """
        if self.__plugins.has_key(pluginname):
            return self.__plugins[pluginname]
        else:
            raise Exception('(EVOGTK - Plugins) There is no loaded plugin called "%s"' % pluginname)

    def unload_plugin(self,pluginname):
        """
        Method for plugin unloading
        """
        # Check if plugin is loaded
        if self.__plugins.has_key(pluginname):
            # Call plugin cleanup method
            self.__dict__[pluginname].unload()
            # Remove plugin from plugin list
            del(self.__plugins[pluginname])
            # Remove plugin instance
            del self.__dict__[pluginname]
        else:
            raise Exception('(EVOGTK - Plugins) There is no loaded plugin called %s' % pluginname)
