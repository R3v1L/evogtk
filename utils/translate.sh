#!/bin/sh

LOCALE_DIR=locale
TRANSLATION_DOMAIN=subprojector
TRANSLATIONS="es en de it fr"

# Extract strings from user interface files
intltool-extract --type=gettext/glade *.ui

xgettext --language=Python --keyword=_ --keyword=N_ --output=$TRANSLATION_DOMAIN.pot *.py *.h

# Create language directories
for I in $TRANSLATIONS
do
	mkdir -p $LOCALE_DIR/$I/LC_MESSAGES/
	if [ -z $LOCALE_DIR/$I/LC_MESSAGES/$TRANSLATION_DOMAIN.po ]
	then
		msginit -i $TRANSLATION_DOMAIN.pot -o $LOCALE_DIR/$I/LC_MESSAGES/$TRANSLATION_DOMAIN.po
	else
		msgmerge $LOCALE_DIR/$I/LC_MESSAGES/$TRANSLATION_DOMAIN.po $TRANSLATION_DOMAIN.pot -o $LOCALE_DIR/$I/LC_MESSAGES/$TRANSLATION_DOMAIN.po
	fi
done

#msgfmt subprojector.po  -o subprojector.mo
