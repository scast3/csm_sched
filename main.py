from Course import CourseCatalog
import pickle

# Load the course_dict from the file
with open('course_dict.pkl', 'rb') as file:
    course_dict = pickle.load(file)

# Access the value associated with the key 'MEGN200'
course = course_dict['MEGN315']

# Print the course details
print(course.print_info())

#Adding all the courses to the Catalog
# catalog = CourseCatalog()

# for course in course_dict:
#     catalog.add_course(course)
def plan():
    catalog = []
    while(True):
        terminal = input('Choice: ')
        semester_count=0

        #Add plan
        if terminal == 'ADD':
            semester = []
            semester_count = semester_count + 1
            print(f'Semester {semester_count}:')
            while (True):
                new_class = input("Add course code: ")
            
                if new_class == 'END':
                    break

                semester.append(new_class)
            catalog.append(semester)
        else:
            break
    print(catalog)
    #when using in practice, return catalog
def inputTransferCredit():
    transfer = []
    while(True):
        tclass = input('Class Code: ')
        if tclass == 'DONE':
            break
        transfer.append(tclass)

#determine if a prevoious class exists in current class' pre requisites
def isValid(plan):
     
    for sem in plan:
        csem = plan.index(sem)
        for course in sem:
            if course in 


