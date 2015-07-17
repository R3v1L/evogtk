#!/usr/bin/python
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
# evogtk.bin.fixmissingtranslatables
# EVOGTK util for fix UI files on objects that are not translatables by default
###############################################################################

import sys,codecs
import xml.dom.minidom

UNTRANSLATABLE_CLASSES={
	'GtkAction': ['label','short_label','tooltip'],
	'GtkRadioAction': ['label','short_label','tooltip'],
	'GtkToggleAction': ['label','short_label','tooltip'],
}

# Load UI file
document=xml.dom.minidom.parse(sys.argv[1])

# Check UI file objects
for obj in document.getElementsByTagName('object'):
	objid=obj.getAttribute('id')
	objclass=obj.getAttribute('class')
	if objclass in UNTRANSLATABLE_CLASSES:
		for prop in obj.getElementsByTagName('property'):
			if prop.getAttribute('name') in UNTRANSLATABLE_CLASSES[objclass]:
				if not prop.getAttribute('translatable'):
					prop.setAttribute('translatable','yes')
					print objclass,'object: %s attribute' % objid,prop.getAttribute('name'),'is not translatable. FIXED'

fd=codecs.open(sys.argv[1],'w','utf-8')
document.writexml(fd,encoding='utf-8')
fd.close()


