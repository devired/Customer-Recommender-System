# emotive
There are 3 components to this project : HTML, DB and the Python Webservice

The HTML components are kept in the templates folder because thats how flask(Python Webservice Package) finds it. All the HTML files are kept in this folder.

The following are the HTML files:

dashboard.html = The dashboard for each machine

The other files like Javascript, Bootstrap and CSS should be kept in the static folder as again thats where flask searches for it.

The DB is a postgresql database : More on this you can find in the DB.md file.

The Twilio and Azure sentiment analysis API Integration,s & Webservice are written in Python using the flask package

To run just type python main.py
