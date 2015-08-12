# Todo items

## launch

* Improve flow from home page to create a new curve. For example if not logged in gather the user's email address as part of process.

* Set up payments for producing high quality tables and roses. Should lock the table.

* Improve layout of curve detail page

* Add instructions for converting between True and Compass to the deviation table print out. Also put in a sales pitch for purchasing an OmniRose.

### deployment related issues

* choose where to host the code

* configure email sending

* extract some things into a local_settings.py


## post launch

* Create a page with different ways to swing a ship.

* Create a tool that for a given location determines what the variation probably is (https://pypi.python.org/pypi/geomag/).

* Set up automated email to people who've created tables prompting them to buy roses. Do it about one week after they create the rose.

* Delete a curve (perhaps not paid curves though?). Have a trash system that empties 30 days after deletion so that undos are possible.

* Compress the number of readings shown - provide another page just with the readings on.

* Let people email in photos of their deviation tables and we'll enter them in and create an account for them.

* generate several roses into one pdf as separate pages

* store date that the deviations were collected on (can be free form text).

* breadcrumbs?

* require at least 3 readings before moving off reading edit page

* change rose so that the ticks are staggered away from the join - possibly have several rose designs that people can choose from

* Allow some tables to be marked as public (and give them a memorable slug)

* Change rows on deviation entry table to highlight when an input has focus

## maybe someday

* switch text rendering to be pango based (http://cairographics.org/pycairo_pango/)

* Make niceties of login work - eg pass the email address across from login to create account or forgot password.

