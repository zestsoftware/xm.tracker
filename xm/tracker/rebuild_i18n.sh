#!/bin/sh
PRODUCTNAME=tracker
I18NDOMAIN=tracker

# Synchronise the .pot with the templates.
i18ndude rebuild-pot --pot locales/${PRODUCTNAME}.pot --create ${I18NDOMAIN} .

# Synchronise the resulting .pot with the .po files
i18ndude sync --pot locales/${PRODUCTNAME}.pot locales/*/LC_MESSAGES/${PRODUCTNAME}.po

# Zope3 is lazy so we have to compile the po files ourselves
# When dropping Plone 3.0 support we can remove mo files from svn, because Zope got smart.
msgfmt -o locales/nl/LC_MESSAGES/${PRODUCTNAME}.mo locales/nl/LC_MESSAGES/${PRODUCTNAME}.po
msgfmt -o locales/en/LC_MESSAGES/${PRODUCTNAME}.mo locales/en/LC_MESSAGES/${PRODUCTNAME}.po
