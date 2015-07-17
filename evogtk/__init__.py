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
# evogtk
# GTK development extensions by EVO Sistemas Libres main module
###############################################################################
# TODO: Application directory detection
# TODO: Find a way to execute default application in all systems
# TODO: Basic information about system in a variable (Screens, user directories, devices, etc)
# TODO: Library documentation and information
# TODO: Check all headers and documentation for typos
# TODO: Database module
# TODO: Localization
###############################################################################

# Python imports
from gettext import lgettext as _

# Import EVOGTK constants
from constants import *

# Check GTK Version requirements
try:
    import pygtk
    pygtk.require(GTK_REQUIRED_VERSION)
except ImportError:
    raise ImportError(_('EVOGTK: Can not import PyGTK module'))
    sys.exit(1)
except AssertionError:
    raise ImportError(_('EVOGTK: Can not import PyGTK required version %s') % GTK_REQUIRED_VERSION)
    sys.exit(1)

# Import GObject
try:
    import gobject    
except:
    raise ImportError(_('EVOGTK: Can not import GObject modules'))
    sys.exit(1)

# Import GTK
try:
    import gtk
    pygtk.require(GTK_REQUIRED_VERSION)
except:
    raise ImportError(_('EVOGTK) Can not import GTK modules'))
    sys.exit(1)

# Check GTK Sourceview support
try:
    import gtksourceview2
    HAS_GTKSOURCEVIEW=True
except:
    HAS_GTKSOURCEVIEW=False

# Check GTKMozEmbed support
try:
    import gtkmozembed
    HAS_GTKMOZEMBED=True
except:
    HAS_GTKMOZEMBED=False
    
# Check spplication indicators
try:
    import appindicator
    HAS_APPINDICATOR=True
except:
    HAS_APPINDICATOR=False

# Check linux desktop notifications
try:
    import pynotify
    HAS_PYNOTIFY=True
except:
    HAS_PYNOTIFY=False