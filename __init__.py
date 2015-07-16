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
# TODO: evogtk: Basic information about system in a variable (Screens, user directories, devices, etc)
# TODO: evogtk: Library documentation and information
# TODO: evogtk: Check all headers and documentation for typos
# TODO: evogtk: Database module
###############################################################################

# Import EVOGTK constants
from constants import *

# Check GTK Version requirements
try:
    import pygtk
    pygtk.require(GTK_REQUIRED_VERSION)
except ImportError:
    raise ImportError('(EVOGTK) Can not import PyGTK module')
    sys.exit(1)
except AssertionError:
    raise ImportError('(EVOGTK) Can not import PyGTK required version %s' % GTK_REQUIRED_VERSION)
    sys.exit(1)

# Import GObject
try:
    import gobject    
except:
    raise ImportError('(EVOGTK) EVOGTK: Can not import GObject modules')
    sys.exit(1)

# Import GTK
try:
    import gtk
    pygtk.require(GTK_REQUIRED_VERSION)
except:
    raise ImportError('(EVOGTK) Can not import GTK modules')
    sys.exit(1)

# Import GTK Sourceview
try:
    import gtksourceview2
    HAS_GTKSOURCEVIEW=True
except:
    print '(EVOGTK) Warning: Can not import GTK Sourceview modules'

# Import GTKMozEmbed
try:
    import gtkmozembed
    HAS_GTKMOZEMBED=True
except:
    print '(EVOGTK) Warning: Can not import GTKMozEmbed modules'
