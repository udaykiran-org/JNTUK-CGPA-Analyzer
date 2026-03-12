import json
import os
from colorama import Fore, Back, Style, init
from calculator import calculate_sgpa, calculate_cgpa, sgpa_to_percentage, get_class, get_backlogs
from visualizer import plot_semester_sgpa, plot_subject_grades, plot_cgpa_progress
from pdf_export import export_pdf

init(autoreset=True)

DATA_FILE = "data.json"

# ── Helpers ──────────────────────────────────────────
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"student": {}, "semesters": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def banner():
    clear()
    print(Fore.CYAN + Style.BRIGHT + "=" * 55)
    print(Fore.CYAN + Style.BRIGHT + "   🎓  JNTUK CGPA ANALYZER  🎓")
    print(Fore.CYAN + Style.BRIGHT + "   Built for B.Tech Students")
    print(Fore.CYAN + Style.BRIGHT + "=" * 55)
    print()

def divider():
    print(Fore.BLUE + "-" * 55)

# ── Student Info ─────────────────────────────────────
def enter_student_info(data):
    banner()
    print(Fore.YELLOW + Style.BRIGHT + "📋 STUDENT INFORMATION")
    divider()
    data['student']['name']    = input(Fore.WHITE + "Enter your Name        : ")
    data['student']['roll']    = input(Fore.WHITE + "Enter your Roll Number : ")
    data['student']['branch']  = input(Fore.WHITE + "Enter your Branch      : ")
    data['student']['college'] = input(Fore.WHITE + "Enter your College     : ")
    save_data(data)
    print(Fore.GREEN + "\n✅ Student info saved!")
    input(Fore.WHITE + "\nPress Enter to continue...")

# ── Add Semester ─────────────────────────────────────
def add_semester(data):
    banner()
    print(Fore.YELLOW + Style.BRIGHT + "➕ ADD SEMESTER DATA")
    divider()

    existing_sems = [s['semester'] for s in data['semesters']]
    print(Fore.CYAN + f"Already added semesters: {existing_sems if existing_sems else 'None'}")

    try:
        sem_no = int(input(Fore.WHITE + "\nEnter Semester Number (1-8): "))
    except ValueError:
        print(Fore.RED + "❌ Invalid input!")
        input("Press Enter to continue...")
        return

    if sem_no in existing_sems:
        print(Fore.RED + f"❌ Semester {sem_no} already exists! Delete it first to re-enter.")
        input("Press Enter to continue...")
        return

    try:
        num_subjects = int(input(Fore.WHITE + "How many subjects this semester? : "))
    except ValueError:
        print(Fore.RED + "❌ Invalid input!")
        input("Press Enter to continue...")
        return

    subjects = []
    print(Fore.CYAN + "\nGrade Scale: S=10  A=9  B=8  C=7  D=6  E=5  F=Fail")
    divider()

    for i in range(num_subjects):
        print(Fore.YELLOW + f"\nSubject {i+1}:")
        name    = input(Fore.WHITE + "  Subject Name   : ")
        
        while True:
            try:
                credits = float(input(Fore.WHITE + "  Credits        : "))
                break
            except ValueError:
                print(Fore.RED + "  ❌ Enter a valid number!")

        while True:
            grade = input(Fore.WHITE + "  Grade (S/A/B/C/D/E/F) : ").upper()
            if grade in ['S', 'A', 'B', 'C', 'D', 'E', 'F']:
                break
            print(Fore.RED + "  ❌ Invalid grade! Use S/A/B/C/D/E/F only")

        subjects.append({
            "name": name,
            "credits": credits,
            "grade": grade
        })

    sem_data = {"semester": sem_no, "subjects": subjects}
    sgpa = calculate_sgpa(subjects)

    print(Fore.GREEN + f"\n✅ Semester {sem_no} added!")
    print(Fore.CYAN + f"📊 SGPA for Semester {sem_no}: {sgpa}")
    print(Fore.CYAN + f"📈 Percentage: {sgpa_to_percentage(sgpa)}%")

    data['semesters'].append(sem_data)
    data['semesters'].sort(key=lambda x: x['semester'])
    save_data(data)
    input(Fore.WHITE + "\nPress Enter to continue...")

# ── View Results ─────────────────────────────────────
def view_results(data):
    banner()
    print(Fore.YELLOW + Style.BRIGHT + "📊 YOUR ACADEMIC RESULTS")
    divider()

    if not data['semesters']:
        print(Fore.RED + "❌ No semester data found! Add semesters first.")
        input("\nPress Enter to continue...")
        return

    # Student info
    s = data['student']
    if s:
        print(Fore.CYAN + f"👤 Name    : {s.get('name','N/A')}")
        print(Fore.CYAN + f"🎓 Roll No : {s.get('roll','N/A')}")
        print(Fore.CYAN + f"🏫 Branch  : {s.get('branch','N/A')}")
    divider()

    # Semester wise
    for sem in data['semesters']:
        sgpa = calculate_sgpa(sem['subjects'])
        pct  = sgpa_to_percentage(sgpa)
        print(Fore.YELLOW + Style.BRIGHT + f"\n📚 SEMESTER {sem['semester']}")
        print(Fore.WHITE + f"{'Subject':<35} {'Credits':>7} {'Grade':>6} {'Points':>7} {'Status':>7}")
        print(Fore.BLUE + "-" * 65)

        for sub in sem['subjects']:
            from calculator import get_grade
            gp     = get_grade(sub['grade'])
            status = Fore.GREEN + "Pass" if sub['grade'] != 'F' else Fore.RED + "FAIL"
            print(f"{Fore.WHITE}{sub['name']:<35} {sub['credits']:>7} {sub['grade']:>6} {gp:>7}  {status}")

        print(Fore.BLUE + "-" * 65)
        print(Fore.CYAN + f"  SGPA: {sgpa}   |   Percentage: {pct}%")

    # Overall
    divider()
    cgpa    = calculate_cgpa(data['semesters'])
    pct     = sgpa_to_percentage(cgpa)
    cls     = get_class(cgpa)
    backlogs = get_backlogs(data['semesters'])

    print(Fore.GREEN + Style.BRIGHT + f"\n🏆 OVERALL CGPA      : {cgpa}")
    print(Fore.GREEN + Style.BRIGHT + f"📈 PERCENTAGE        : {pct}%")
    print(Fore.GREEN + Style.BRIGHT + f"🎖  DEGREE CLASS     : {cls}")

    if backlogs:
        print(Fore.RED + Style.BRIGHT + f"\n⚠️  BACKLOGS ({len(backlogs)}):")
        for b in backlogs:
            print(Fore.RED + f"   Sem {b['semester']} → {b['subject']} ({b['credits']} credits)")
    else:
        print(Fore.GREEN + "\n✅ No Backlogs! Clean record!")

    input(Fore.WHITE + "\nPress Enter to continue...")

# ── Delete Semester ───────────────────────────────────
def delete_semester(data):
    banner()
    print(Fore.YELLOW + Style.BRIGHT + "🗑️  DELETE SEMESTER")
    divider()

    existing = [s['semester'] for s in data['semesters']]
    print(Fore.CYAN + f"Existing semesters: {existing}")

    try:
        sem_no = int(input(Fore.WHITE + "\nEnter semester number to delete: "))
    except ValueError:
        print(Fore.RED + "❌ Invalid input!")
        input("Press Enter to continue...")
        return

    data['semesters'] = [s for s in data['semesters'] if s['semester'] != sem_no]
    save_data(data)
    print(Fore.GREEN + f"✅ Semester {sem_no} deleted!")
    input("Press Enter to continue...")

# ── Graphs ────────────────────────────────────────────
def show_graphs(data):
    banner()
    print(Fore.YELLOW + Style.BRIGHT + "📊 VISUAL CHARTS")
    divider()

    if not data['semesters']:
        print(Fore.RED + "❌ No data found! Add semesters first.")
        input("\nPress Enter to continue...")
        return

    print(Fore.CYAN + "1. Semester wise SGPA Chart")
    print(Fore.CYAN + "2. Subject wise Grades (per semester)")
    print(Fore.CYAN + "3. CGPA Progress Line Chart")
    print(Fore.CYAN + "4. All Charts")

    choice = input(Fore.WHITE + "\nChoose (1/2/3/4): ")

    if choice == '1':
        plot_semester_sgpa(data['semesters'])
    elif choice == '2':
        existing = [s['semester'] for s in data['semesters']]
        print(Fore.CYAN + f"Available semesters: {existing}")
        try:
            sem_no = int(input(Fore.WHITE + "Enter semester number: "))
            sem_data = next((s for s in data['semesters'] if s['semester'] == sem_no), None)
            if sem_data:
                plot_subject_grades(sem_data)
            else:
                print(Fore.RED + "❌ Semester not found!")
        except ValueError:
            print(Fore.RED + "❌ Invalid input!")
    elif choice == '3':
        plot_cgpa_progress(data['semesters'])
    elif choice == '4':
        plot_semester_sgpa(data['semesters'])
        plot_cgpa_progress(data['semesters'])
    else:
        print(Fore.RED + "❌ Invalid choice!")

    input(Fore.WHITE + "\nPress Enter to continue...")

# ── Export PDF ────────────────────────────────────────
def export_result_pdf(data):
    banner()
    print(Fore.YELLOW + Style.BRIGHT + "📄 EXPORT PDF REPORT")
    divider()

    if not data['semesters']:
        print(Fore.RED + "❌ No data found! Add semesters first.")
        input("\nPress Enter to continue...")
        return

    print(Fore.CYAN + "Generating your PDF report...")
    filename = export_pdf(data['student'], data['semesters'])
    print(Fore.GREEN + f"✅ PDF saved as: {filename}")
    input(Fore.WHITE + "\nPress Enter to continue...")

# ── Main Menu ─────────────────────────────────────────
def main():
    data = load_data()

    while True:
        banner()

        # Show quick summary if data exists
        if data['semesters']:
            cgpa = calculate_cgpa(data['semesters'])
            backlogs = get_backlogs(data['semesters'])
            print(Fore.GREEN + f"  👤 {data['student'].get('name', 'Student')}  |  "
                  f"CGPA: {cgpa}  |  Backlogs: {len(backlogs)}")
            divider()

        print(Fore.CYAN + "  1. Enter Student Information")
        print(Fore.CYAN + "  2. Add Semester Data")
        print(Fore.CYAN + "  3. View Full Results")
        print(Fore.CYAN + "  4. Show Visual Charts")
        print(Fore.CYAN + "  5. Export PDF Report")
        print(Fore.CYAN + "  6. Delete a Semester")
        print(Fore.RED  + "  7. Exit")
        divider()

        choice = input(Fore.WHITE + "  Choose an option (1-7): ")

        if choice == '1':
            enter_student_info(data)
        elif choice == '2':
            add_semester(data)
        elif choice == '3':
            view_results(data)
        elif choice == '4':
            show_graphs(data)
        elif choice == '5':
            export_result_pdf(data)
        elif choice == '6':
            delete_semester(data)
        elif choice == '7':
            print(Fore.GREEN + "\n👋 Goodbye! Study hard raa! 💪")
            break
        else:
            print(Fore.RED + "❌ Invalid choice!")
            input("Press Enter to continue...")

main()