# OmniRose

This repository holds the code for the [OmniRose website](http://www.omnirose.com).

## About

The OmniRose website lets you create a deviation table for your compass by entering deviations at certain bearings. For a one-off fee this table can then be used to create a conversion rose that greatly simplifies converting between true, magnetic and compass bearings.

## Contributing

We've made our code open source as we believe it is the right thing to do, and to enable the community to help make it better. We're certainly not the smartest people out there.

Contributions are very welcome. The code is hosted on GitHub as [OmniRose/OmniRose](https://github.com/OmniRose/OmniRose). We are happy to accept any bug reports as [issues on GitHub](https://github.com/OmniRose/OmniRose/issues) or even better fixes as [pull requests](https://github.com/OmniRose/OmniRose/pulls).

To work on the code you'll need to be familiar with Python and setting a unix like environment. For the browser based tests in the test suite you'll need to install FireFox.

    # After downloading the source set up the environment
    virtualenv .venv
    . .venv/bin/activate
    pip install -r omnirose/requirements.txt

    # Go to the code
    cd omnirose

    # Copy the local settings and edit then correctly
    cp local_settings_template.py local_settings.py
    nano local_settings.py

    # Create and setup the database
    createdb omnirose
    ./manage.py migrate

    # Run the tests
    ./manage.py test

    # Run the development server
    ./manage.py runserver
