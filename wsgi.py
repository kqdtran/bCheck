#!/usr/bin/env python

import os
import requests
import re
import json

from bottle import Bottle, route, run, static_file, template, view, request
from rec_scrape import MLStripper, Rec, strip_tags, Course
from bs4 import BeautifulSoup as Soup

application = app = Bottle()
headers = {
    'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
    'X-Requested-With' : 'XMLHttpRequest'
}

# -------- Resources are loaded below ---------
@app.route('/static/js/<filename>')
def js_static(filename):
    return static_file(filename, root='./static/js')

@app.route('/static/img/<filename>')
def img_static(filename):
    return static_file(filename, root='./static/img')

@app.route('/static/css/<filename>')
def img_static(filename):
    return static_file(filename, root='./static/css')
# ------------------------------------------- #

@app.route("/")
@view("main")
def hello():
    """The main view, with a page title"""
    return dict(title = "bCheck")

@app.route('/checkEnrollment', method='POST')
def check_enrollment():
    """Check enrollment status for a list of Course Control Numbers (CCNs)"""

    def is_CCN(num):
        """Check if a given string is a valid CCN. We only check for formatting for.
        If the 5-digit combination is not used by the school, the result will be an error"""
        return len(num) == 5 and num.isdigit()

    def strip_white_space(text):
        """Strip all extra whitespace and turn them into one single whitespace"""
        return " ".join(text.strip().split())

    # Retrieve the CCNs, and split them by comma
    text = strip_white_space(request.forms.get('text'))
    CCNs = [code.strip() for code in text.split()]
    url = "https://telebears.berkeley.edu/enrollment-osoc/osc"
    all_courses = []

    for ccn in CCNs:
        notFound = False
        if is_CCN(ccn):
            values = dict(_InField1 = "RESTRIC", _InField2 = ccn, _InField3 = "13D2")
            html = requests.post(url, data=values, headers=headers)
            soup = Soup(html.content, from_encoding="utf-8")
            group = []
            i = 0

            info = soup.find_all("div", {"class" : "layout-div"})
            for sp in info:
                if "CCN Not Found" in strip_white_space(sp.text):
                    course = Course("No such course with the given CCN", ccn, "None", "", "None") 
                    notFound = True
                    break
                if i == 2 or i == 5 or i == 6:
                    group.append(strip_white_space(sp.text))
                i += 1
                if i > 6: break 

            if notFound: # No course with the given CCN found
                all_courses.append(course) 
                continue

            categories = []
            for category in soup.find_all("li"):
                categories.append(category.text)
            if len(group) == 3:
                course = Course(group[0], ccn, group[1], group[2], "<br><br>".join(categories))
            else: # shenanigan
                course = Course("No such course... Shenanigan!", ccn, "None", "", "None") 
        else:
            course = Course("No such course. Wrong CCN format!", ccn, "None", "", "None")  
        all_courses.append(course)    

    check_classes = [dict(course = "<strong>" + c.course + " (" + c.CCN + ")</strong>", stats = c.enrollment_status + "<br><br>" + c.waitlist, \
                            category = c.categories) for c in all_courses]
    return dict(result = check_classes)

@app.route('/scrapeOpen', method='POST')
def scrape_open_classes():
    """Scrape all open classes, as suggested by the Schedule of Classes :-(
        Soooo... no live update here"""

    html = requests.get("http://or.berkeley.edu/SUGGESTEDCOURSES/DisplaySuggestedCourses.aspx?ID=261", headers=headers)
    soup = Soup(html.content, from_encoding="utf-8")
    i = 0
    allrecs = []
    group = []

    # Group contents into one object, which consists of the course name, instructor, CCN, 
    # recommendation from past students (if any), and course description/textbook
    for sp in soup.find_all("span", id=re.compile("^ctl00_contentMain_gvSuggestedCourses")):
        if i == 0: # append the entire thing for the first span
            group.append(sp)
        elif i != 3 and i != 5: # only append text here
            group.append(sp.text)
        i += 1
        if i == 6:
            # bold a few specific terms to make them more readable
            instructor, course = strip_tags(group[0].decode_contents().replace("<br/>", "\n")).strip().split("\n")
            rec = Rec(course, instructor, group[1], group[2], group[3])
            allrecs.append(rec)
            
            # reset for next 6 iterations
            i = 0
            group = []

    open_classes = [dict(course = cl.course, instructor = cl.instructor.replace("Instructor", "<strong>Instructor</strong>"), \
                        CCN = cl.CCN.replace("CCN", "<strong>CCN</strong>"), \
                        rec = cl.recommendation.replace("Recommendation", "<strong>Recommendation</strong>"), desc = cl.description) \
                    for cl in allrecs]
    return dict(result = open_classes)

if __name__ == "__main__":
    run(app, host='localhost', port=5000, reloader=True)
