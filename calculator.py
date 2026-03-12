# JNTUK Grade System
# S=10, A=9, B=8, C=7, D=6, E=5, F=0

GRADE_POINTS = {
    'S': 10,
    'A': 9,
    'B': 8,
    'C': 7,
    'D': 6,
    'E': 5,
    'F': 0
}

def get_grade(grade_letter):
    return GRADE_POINTS.get(grade_letter.upper(), 0)

def calculate_sgpa(subjects):
    """
    subjects = [
        {"name": "Maths", "credits": 4, "grade": "A"},
        ...
    ]
    """
    total_credits = 0
    total_points = 0

    for sub in subjects:
        credits = sub['credits']
        grade_point = get_grade(sub['grade'])
        total_points += credits * grade_point
        total_credits += credits

    if total_credits == 0:
        return 0

    sgpa = total_points / total_credits
    return round(sgpa, 2)

def calculate_cgpa(semesters):
    """
    semesters = list of semester data, each with subjects
    """
    total_credits = 0
    total_points = 0

    for sem in semesters:
        for sub in sem['subjects']:
            credits = sub['credits']
            grade_point = get_grade(sub['grade'])
            total_points += credits * grade_point
            total_credits += credits

    if total_credits == 0:
        return 0

    cgpa = total_points / total_credits
    return round(cgpa, 2)

def get_backlogs(semesters):
    """Returns list of failed subjects across all semesters"""
    backlogs = []
    for sem in semesters:
        for sub in sem['subjects']:
            if sub['grade'].upper() == 'F':
                backlogs.append({
                    "semester": sem['semester'],
                    "subject": sub['name'],
                    "credits": sub['credits']
                })
    return backlogs

def sgpa_to_percentage(sgpa):
    """JNTUK Official Formula: Percentage = (SGPA - 0.5) * 10"""
    return round((sgpa - 0.5) * 10, 2)

def get_class(cgpa):
    """Returns degree class based on CGPA"""
    if cgpa >= 9.0:
        return "🏆 Outstanding"
    elif cgpa >= 8.0:
        return "⭐ First Class with Distinction"
    elif cgpa >= 6.5:
        return "✅ First Class"
    elif cgpa >= 5.5:
        return "📘 Second Class"
    elif cgpa >= 5.0:
        return "📗 Pass Class"
    else:
        return "❌ Fail"