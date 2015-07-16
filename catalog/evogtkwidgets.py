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
# widgets
# EVOGTK Custom Widgets
###############################################################################
# TODO: evogtk.catalog: Find a way to make adaptors working
###############################################################################

# EVOGTK Imports
import evogtk

# Widget imports
from evogtk.widgets.cairocanvas import CairoCanvas
from evogtk.widgets.cairoscroller import CairoScroller
from evogtk.widgets.floatingwindow import FloatingWindow
from evogtk.widgets.trayicon import TrayIcon
from evogtk.widgets.regexpentry import RegExpEntry
from evogtk.widgets.datepicker import DatePicker
from evogtk.widgets.colorpicker import ColorPicker
from evogtk.widgets.fontcombo import FontCombo

# DB Widgets
from evogtk.widgets.dbwidgets.dbentry import DBEntry
from evogtk.widgets.dbwidgets.dbspinbutton import DBSpinButton
from evogtk.widgets.dbwidgets.dbcombobox import DBComboBox
from evogtk.widgets.dbwidgets.dbcheckbutton import DBCheckButton
from evogtk.widgets.dbwidgets.dbregexpentry import DBRegExpEntry
from evogtk.widgets.dbwidgets.dbdatepicker import DBDatePicker

# Conditional imports
if evogtk.HAS_GTKSOURCEVIEW:
    from evogtk.widgets.srceditor import SourceEditor
if evogtk.HAS_GTKMOZEMBED:
    from evogtk.widgets.webbrowser import WebBrowser
