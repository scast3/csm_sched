import requests
from bs4 import BeautifulSoup
from Course import Course
from Course import CourseCatalog
#IMPORTANT
#Change to add courses to directed graph rather than dict

import re

#Stores all course objects, can access through course code
course_dict={}

# Make an HTTP request to the website
url = 'https://catalog.mines.edu/coursesaz/'
response = requests.get(url)
html_content = response.content

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the <a> tags in the parsed HTML
links = soup.find_all('a')

# Extract the href attribute from each <a> tag to get the link
departmentcodes = []
for link in links:
    href = link.get('href')
    if href!=None and '/coursesaz/' in href and href!='/coursesaz/' and href!='/coursesaz/coursesaz.pdf':
        departmentcodes.append(href)

#outputs an array
def cleanText(s):
    course_code_pattern = r"\b[A-Za-z]+\d+\b"
    course_codes = re.findall(course_code_pattern, s)
    return course_codes

def remove_substrings(text, substrings):
    for substring in substrings:
        text = text.replace(substring, '')
    return text

#only outputs a string
def single_course_code(text):
    course_code_pattern = r"\b[A-Za-z]+\d+\b"
    course_code_match = re.search(course_code_pattern, text)
    if course_code_match:
        return course_code_match.group()
    return None

def add_department_classes(depturl):
    newurl = depturl
    response = requests.get(newurl)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    course_titles = soup.find_all('p', class_='courseblocktitle')
    course_descriptions = soup.find_all('p',class_='courseblockdesc')
    
    for title,desc in zip(course_titles,course_descriptions):
        text = title.text.strip()
        d = desc.text.strip()

        course_code, _, rest_text = text.partition('.')
        course_name = rest_text.split('.')[0][2:]
        credit_hours = rest_text.split('.')[1][2:]

        #accessing pre req and co req patterns
        prerequisite_pattern = r"Prerequisite:\s*(.*?)\."
        co_requisite_pattern = r"Co-requisite:\s*(.*?)\."

        prerequisite_match = re.search(prerequisite_pattern, d)
        co_requisite_match = re.search(co_requisite_pattern, d)

        prerequisites=[]
        co_requisites=[]

        if prerequisite_match:

            temp = prerequisite_match.group(1)
            prerequisites_string = remove_substrings(temp, ['(C- or better)', 'grade of C- or better', 'or equivalent'])
0
            if "," in prerequisites_string:
                comma_split = prerequisites_string.split(",")

                for p in comma_split:
                    if ' or ' in p:
                        temparr = cleanText(p)
                        prerequisites.append(temparr)
                    else:
                        prerequisites.append(single_course_code(p))

            elif ' or ' in prerequisites_string:
                prerequisites = cleanText(prerequisites_string)
            else:
                prerequisites.append(single_course_code(prerequisites_string))
        else:
            prerequisites = None

        if co_requisite_match:
            co_requisites = re.findall(r"\b[A-Za-z]+\d+\b", co_requisite_match.group(1))
        else:
            co_requisites = None
        #Can access a course object just by knowing its course code
        catalog = CourseCatalog()
        course = Course(course_code, credit_hours, course_name, prerequisites, co_requisites)
        #catalog.add_course(course_code)
        #use this so you don't have to create a new data structure? maybe?
        
        course_dict[course_code]=course
        #course.print_info()

def department_iterator():
    for code in departmentcodes:
        print(f'Loading classes for {code[11:]} ...')
        add_department_classes(f'https://catalog.mines.edu{code}')
    print('Done!')
    print()
    print('course_dict has been loaded')

department_iterator()

import pickle

# Save the course_dict to a file
with open('course_dict.pkl', 'wb') as file:
    pickle.dump(course_dict, file)
