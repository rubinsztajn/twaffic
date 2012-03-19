twaffic
========

A simple Twitter listener that monitors @MassDOT and sends an SMS when
there is a traffic alert or update. Twaffic can be toggled on or off
by a tweet from a defined twitter account.

To install:
----------

1. pip install -r requirements.pip
1. cp config.py.template config.py and edit according to your account
details, etc...
1. ./twaffic.py >> taffic.log &

Twaffic will run in the background, listening for commands or traffic
updates, and send texts accordingly.


