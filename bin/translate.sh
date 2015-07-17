#!/bin/sh

LOCALE_DIR=
TRANSLATION_DOMAIN=$1
TRANSLATIONS="es en de it fr"

# Extract strings from user interface files
for I in `ls *.ui`
do
	# Fix missing translatables
	./fixmissingtranslatables.py $I
done

# Extract information from GUI files
intltool-extract --type=gettext/glade *.ui

# Extract information from code files
xgettext --language=Python --keyword=_ --keyword=N_ --output=$TRANSLATION_DOMAIN.pot *.py *.h

# Cleaning of generated .h files
for I in `ls *.ui`
do
	rm $I.h
done

# Create language directories
for I in $TRANSLATIONS
do
	mkdir -p ./locale/$I/LC_MESSAGES/
	if [ -z ./locale/$I/LC_MESSAGES/$TRANSLATION_DOMAIN.po ]
	then
		msginit -i $TRANSLATION_DOMAIN.pot -o ./locale/$I/LC_MESSAGES/$TRANSLATION_DOMAIN.po
	else
		msgmerge ./locale/$I/LC_MESSAGES/$TRANSLATION_DOMAIN.po $TRANSLATION_DOMAIN.pot -o ./locale/$I/LC_MESSAGES/$TRANSLATION_DOMAIN.po
	fi
done

# Compile language files
for I in $TRANSLATIONS
do
	msgfmt ./locale/$I/LC_MESSAGES/$TRANSLATION_DOMAIN.po -o ./locale/$I/LC_MESSAGES/$TRANSLATION_DOMAIN.mo
done

# Cleaning
for I in `ls *.ui`
do
	rm $I.h
done
