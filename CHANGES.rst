History of xm.tracker
=====================


1.0.7 (2014-03-31)
------------------

- Never cache the tracker view.  It always needs to be fresh.
  [maurits]


1.0.6 (2012-09-12)
------------------

- Moved to github: https://github.com/zestsoftware/xm.tracker
  [maurits]


1.0.5 (2011-05-03)
------------------

- Removed base2 library from head section. [jladage]

- Fixed translation of invalid time message.
  [maurits]


1.0.4 (2010-09-24)
------------------

- Explicitly load the permissions.zcml file from
  Products.eXtremeManagement, otherwise you can get a
  ComponentLookupError on zope startup.
  [maurits]

- Added z3c.autoinclude.plugin target plone.
  [maurits]

- For entries, always round up to the nearest minute.
  [maurits]


1.0.3 (2010-05-03)
------------------

- Fixed rounding error: hours in entries were counted twice (2:15
  tracked in the timer would mean 2 hours plus (2*60 + 15 = 135)
  minutes = 4 hours, 15 minutes tracked.
  [maurits]


1.0.2 (2010-05-01)
------------------

- Round booked time up to multiple of 15 minutes.  Round tracked time
  up to complete minutes.
  Fixes http://plone.org/products/extreme-management-tool/issues/175
  [maurits]

- Specify egenix-mx-base as dependency in setup.py.  It is
  easy_installable now.  When this is not pulled in automatically you
  can run into seemingly unrelated problems, certainly when you do not
  start the instance on the foreground; not all zcml will be loaded.
  Having it as an official dependency should work fine now, and if it
  fails it is at least explicit about what fails.
  [maurits]

- added german translation. [jensens]


1.0.2 (2009-05-05)
------------------

- Nothing changed yet.


1.0.1 (2009-05-05)
------------------

- Added div #task_selection_form_content to unassigned_task_select.pt
  to provide styling for the unassigned tasks form. [laurens]


1.0 (2009-03-15)
----------------

- select tasks button is now placed inside track time toolbar
  [laurens]


1.0rc1 (2009-01-25)
-------------------

- Tooltip now displays total booked and total tracked. [jladage]


0.6 (2009-01-15)
----------------

- I made changes and didn't publish them in the history file. :) [laurens]


0.5 (2009-01-09)
----------------

- Fix buttons on the 'select task for unassigned entry' form. [mark]

- Reinstate class on 'book to task' button which triggers the
  KSS. [reinout, mark]


0.4 (2009-01-07)
----------------

- Moved "eXtremeManagement: View Tracker" permission to
  Products.eXtremeManagement as we do not actually use that permission
  in the xm.tracker package.  [maurits]

- Display a warning in a task when it is orphaned (removed, in the
  wrong state).  [maurits]

- CSS changes to the tracker interface to visually distinguish tasks with and
  without bookings. [simon]

- Added project-grouping of tasks in the tracker view. [simon]

- Moved timer display to a separate viewlet. And added kss-refreshing of that
  viewlet in two places so that the timer (and especially the tooltip showing
  the booked hours) gets updated on stopping the timer, on editing the time of
  an entry and on adding entries. [reinout]

- Fixed http://plone.org/products/extreme-management-tool/issues/79 by
  not using unicode in one small place. [reinout]

- Added KSS and template changes to allow the 'seconds' part of the tracker
  timer to be individually styled. (This relates to kss.plugin.timer r72297.)
  [simon]


0.3 (2008-09-18)
----------------

- Show the total hours booked plus tracked today as a tooltip on the
  timer.  [maurits+simon]

- Do not store the portal_url in the task_url; copying a Data.fs from
  production to a development machine would give you a url to the
  tasks on the production site, which is not handy and can be
  dangerous.  After this change you need to remove existing tracker
  tasks and add them again unfortunately.  [maurits+simon]

- Bug fix: when the tracker pointed to a task with a Discussion Item
  (comment) in it you would get: 'TypeError: a float is required'.
  [maurits]


0.2 (2008-09-17)
----------------

- Bug fix: a booking for 75 minutes would get stored as 1 hour and
  75 minutes instead of 1 hour and 15 minutes.  [maurits]


0.1.1 (2008-09-16)
------------------

- Removed egenix-mx-base from the install_requires of setup.py as it
  is not easy_installable.  Improved docs/INSTALL.txt to explain about
  how to install mx.DateTime.  [maurits]


0.1 (2008-09-16)
----------------

- First version. [maurits, reinout, jladage, simon]
