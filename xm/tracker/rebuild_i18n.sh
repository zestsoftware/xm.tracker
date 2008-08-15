#!/bin/sh
PRODUCTNAME=tracker
I18NDOMAIN=xm.tracker

# Synchronise the .pot with the templates.
# Also merge it with generated.pot, which includes the items
# from schema.py
i18ndude rebuild-pot --pot locales/${PRODUCTNAME}.pot --create ${I18NDOMAIN} .

# Synchronise the resulting .pot with the .po files
i18ndude sync --pot locales/${PRODUCTNAME}.pot locales/nl/LC_MESSAGES/${PRODUCTNAME}.po

# Zope3 is lazy so we have to comile the po files ourselves
# When dropping Plone 3.0 support we can remove mo files from svn, because Zope got smart.

msgfmt -o locales/nl/LC_MESSAGES/${PRODUCTNAME}.mo locales/nl/LC_MESSAGES/${PRODUCTNAME}.po
