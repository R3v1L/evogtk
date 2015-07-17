#!/bin/sh

LOCALE_DIR=locale
TRANSLATION_DOMAIN=subprojector

# Compile language files
for I in `ls $LOCALE_DIR`
do
	msgfmt $LOCALE_DIR/$I/LC_MESSAGES/subprojector.po  -o $LOCALE_DIR/$I/LC_MESSAGES/subprojector.mo
done
