bCheck
=========

Check live enrollment status and classes with open seats at Cal    

The POST requests to Berkeley's class scheduling service are powered by [requests](http://docs.python-requests.org/en/latest/). Retrieved information are then parsed and extracted with the help of [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/). Finally, data are populated in a beautiful bootstrap-compatible format by [DataTables.js](https://datatables.net/)   

The app is hosted with AppFog on its HP OpenStack Infrastructure. For some reason, the Berkeley site blocks all requests from Heroku and AWS, which breaks my heart... :/    

[See it in action](https://bcheck.hp.af.cm/)