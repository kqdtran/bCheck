import requests
import re
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup as Soup

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
    'From': 'snipehunter.1610@gmail.com' 
}

class MLStripper(HTMLParser):
    """Strip text from HTML tags with this cccccombo breaker"""
    
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class Rec:
    """Holds all recommendations for open classes"""
    
    def __init__(self, course, instructor, CCN, recommendation, description):
        self.course = course
        self.instructor = instructor
        self.CCN = CCN.strip()
        self.recommendation = recommendation.strip()
        self.description = description.strip()

    def __str__(self):
        strings = []
        strings.append(self.course)
        strings.append(self.instructor)
        strings.append(self.CCN)
        if self.recommendation:
            strings.append(self.recommendation)
        strings.append("Description: " + self.description)
        return "\n".join(strings).encode("utf-8")

# This is merely for command-line testing        
def scrape():
    html = requests.get("http://or.berkeley.edu/SUGGESTEDCOURSES/DisplaySuggestedCourses.aspx?ID=261", headers=headers)
    soup = Soup(html.content, from_encoding="utf-8")
    i = 0
    allrecs = []
    group = []

    for sp in soup.find_all("span", id=re.compile("^ctl00_contentMain_gvSuggestedCourses")):
        if i == 0: # append the entire thing for the first span
            group.append(sp)
        elif i != 3 and i != 5: # only append text here
            group.append(sp.text)
        i += 1
        if i == 6:
            instructor, course = strip_tags(group[0].decode_contents().replace("<br/>", "\n")).strip().split("\n")
            rec = Rec(course, instructor, group[1], group[2], group[3])
            allrecs.append(rec)
            
            # reset for next 6 iterations
            i = 0
            group = []

class Course():
    """Holds the enrollment result for each course"""
    
    def __init__(self, course, CCN, enrollment_status, waitlist, categories):
        self.course = course
        self.CCN = CCN
        self.enrollment_status = enrollment_status
        self.waitlist = waitlist
        self.categories = categories

    def __str__(self):
        strings = []
        strings.append(self.course)
        strings.append(self.CCN)
        strings.append(self.enrollment_status + " " + self.waitlist)
        strings.append(self.categories)
        return "\n".join(strings).encode("utf-8")

# This is merely for command-line testing     
def check_enrollment():
    def is_CCN(num):
        """Check if a given string is a valid CCN. We only check for formatting for.
        If the 5-digit combination is not used by the school, the result will be an error"""
        return len(num) == 5 and num.isdigit()

    def strip_white_space(text):
        """Strip all extra whitespace and turn them into one single whitespace"""
        return " ".join(text.strip().split())

    url = "https://telebears.berkeley.edu/enrollment-osoc/osc"
    for ccn in ["25010", "12999", "1277", "25017"]:
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
                print course, "\n"
                continue

            categories = []
            for category in soup.find_all("li"):
                categories.append(category.text)
            if len(group) == 3:
                course = Course(group[0], ccn, group[1], group[2], "<br><br>".join(categories))
            else: # shenanigan
                course = Course("No such course. Shenanigan!", ccn, "None", "", "None") 
        else:
            course = Course("No such course wrong format CCN", ccn, "None", "", "None") 
        print course, "\n"

    
if __name__ == "__main__":
    #scrape()
    check_enrollment()
