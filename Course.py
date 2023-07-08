class Course:
    def __init__(self, course_code, credit_hours, course_name, prerequisites=None, corequisites=None):
        #Course department is the first 4 characters e.g MEGN
        self.course_dept = course_code[0:4]
        #Course number is the number after the code
        self.course_number = course_code[4:7]

        self.course_code = course_code #e.g. MEGN300
        
        self.credit_hours = credit_hours
        self.course_name = course_name

        self.isUndergrad = True

        if(int(self.course_number)>500):
            self.isUndergrad = False
        
        self.prerequisites = [] if prerequisites is None else list(prerequisites)
        self.corequisites = [] if corequisites is None else list(corequisites)

    def print_info(self):
        print(f"Course Department: {self.course_dept}")
        print(f"Course Number: {self.course_number}")
        print(f"Course Name: {self.course_name}")
        print(f"Credit Hours: {self.credit_hours}")
        print(f"Prerequisites: {self.prerequisites}")
        print(f"Corequisites: {self.corequisites}")
        print()

class CourseCatalog:
    def __init__(self):
        self.course_map = {}

    def add_course(self, course):
        self.course_map[course.course_code] = course

    def add_prerequisite(self, course_code, prerequisite_code):
        if course_code in self.course_map and prerequisite_code in self.course_map:
            course = self.course_map[course_code]
            prerequisite = self.course_map[prerequisite_code]
            course.add_prerequisite(prerequisite)

    def add_corequisite(self, course_code, corequisite_code):
        if course_code in self.course_map and corequisite_code in self.course_map:
            course = self.course_map[course_code]
            corequisite = self.course_map[corequisite_code]
            course.add_corequisite(corequisite)

    #Use to find what classes need to be taken in what order
    def find_path(self, start_code, target_code):
        visited = set()
        path = []
        self._dfs(start_code, target_code, visited, path)
        return path

    def _dfs(self, current_code, target_code, visited, path):
        if current_code == target_code:
            path.append(current_code)
            return True

        visited.add(current_code)
        course = self.course_map[current_code]

        for prerequisite in course.prerequisites:
            if prerequisite.course_code not in visited:
                if self._dfs(prerequisite.course_code, target_code, visited, path):
                    path.append(current_code)
                    return True

        for corequisite in course.corequisites:
            if corequisite.course_code not in visited:
                if self._dfs(corequisite.course_code, target_code, visited, path):
                    path.append(current_code)
                    return True

        return False





