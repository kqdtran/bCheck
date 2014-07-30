bCheck
=========

Check live enrollment status at Cal    

## Quick Overview

The POST requests to Berkeley's class scheduling service are powered by [requests](http://docs.python-requests.org/en/latest/). Retrieved information are then parsed and extracted with the help of [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/). Finally, data are populated in a beautiful bootstrap-compatible format by [DataTables.js](https://datatables.net/)   

The app is hosted with AppFog on its HP OpenStack Infrastructure. For some reason, Berkeley seems to block all requests from Heroku and AWS... :/    

[See it in action](https://bcheck.hp.af.cm/)

## I want to run it locally

Cool! You need to have `virtualenv` and (optionally) `virtualenvwrapper` installed to avoid any dependency conflict with your other projects. Clone the repo, then do

```
cd bCheck
mkvirtualenv bCheck
pip install -r requirements.txt
python wsgi.py
```

and navigate to port 5001 to see the app run on localhost.

## Problems/Questions?

Send me an email, or raise an issue. The app is occasionally down (check [AppFog Status](https://twitter.com/AppFogStatus) for more info),
so it is recommended that you run it locally.