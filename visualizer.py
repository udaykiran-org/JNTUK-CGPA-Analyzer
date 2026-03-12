import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def plot_semester_sgpa(semesters):
    """Bar chart of SGPA across all semesters"""
    from calculator import calculate_sgpa

    sem_labels = []
    sgpa_values = []

    for sem in semesters:
        sem_labels.append(f"Sem {sem['semester']}")
        sgpa_values.append(calculate_sgpa(sem['subjects']))

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#1e1e2e')
    ax.set_facecolor('#1e1e2e')

    colors = ['#89b4fa' if s >= 8 else '#fab387' if s >= 6 else '#f38ba8' for s in sgpa_values]
    bars = ax.bar(sem_labels, sgpa_values, color=colors, width=0.5, zorder=3)

    # Add value labels on bars
    for bar, val in zip(bars, sgpa_values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                str(val), ha='center', va='bottom', color='white', fontweight='bold')

    ax.set_ylim(0, 10.5)
    ax.set_xlabel('Semester', color='white', fontsize=12)
    ax.set_ylabel('SGPA', color='white', fontsize=12)
    ax.set_title('📊 Semester wise SGPA Performance', color='white', fontsize=14, fontweight='bold')
    ax.tick_params(colors='white')
    ax.grid(axis='y', color='gray', linestyle='--', alpha=0.4, zorder=0)

    for spine in ax.spines.values():
        spine.set_edgecolor('gray')

    # Legend
    high = mpatches.Patch(color='#89b4fa', label='SGPA ≥ 8 (Distinction)')
    mid = mpatches.Patch(color='#fab387', label='SGPA ≥ 6 (First Class)')
    low = mpatches.Patch(color='#f38ba8', label='SGPA < 6 (Pass/Fail)')
    ax.legend(handles=[high, mid, low], facecolor='#313244', labelcolor='white')

    plt.tight_layout()
    plt.savefig('sgpa_chart.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ SGPA Chart saved as sgpa_chart.png")

def plot_subject_grades(semester_data):
    """Horizontal bar chart for subject wise grades in a semester"""
    from calculator import get_grade

    subjects = [sub['name'] for sub in semester_data['subjects']]
    grade_points = [get_grade(sub['grade']) for sub in semester_data['subjects']]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#1e1e2e')
    ax.set_facecolor('#1e1e2e')

    colors = ['#a6e3a1' if g >= 8 else '#fab387' if g >= 5 else '#f38ba8' for g in grade_points]
    bars = ax.barh(subjects, grade_points, color=colors, zorder=3)

    for bar, val in zip(bars, grade_points):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                str(val), va='center', color='white', fontweight='bold')

    ax.set_xlim(0, 11)
    ax.set_xlabel('Grade Point', color='white', fontsize=12)
    ax.set_title(f"📚 Subject wise Grade Points — Sem {semester_data['semester']}",
                 color='white', fontsize=14, fontweight='bold')
    ax.tick_params(colors='white')
    ax.grid(axis='x', color='gray', linestyle='--', alpha=0.4, zorder=0)

    for spine in ax.spines.values():
        spine.set_edgecolor('gray')

    plt.tight_layout()
    plt.savefig(f"sem{semester_data['semester']}_subjects.png", dpi=150, bbox_inches='tight')
    plt.show()
    print(f"✅ Subject chart saved!")

def plot_cgpa_progress(semesters):
    """Line chart showing CGPA progress over semesters"""
    from calculator import calculate_sgpa

    sem_labels = [f"Sem {s['semester']}" for s in semesters]
    sgpa_list = [calculate_sgpa(s['subjects']) for s in semesters]

    # Running CGPA
    running_cgpa = []
    total_pts = 0
    total_creds = 0
    from calculator import get_grade
    for sem in semesters:
        for sub in sem['subjects']:
            total_pts += sub['credits'] * get_grade(sub['grade'])
            total_creds += sub['credits']
        running_cgpa.append(round(total_pts/total_creds, 2) if total_creds else 0)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#1e1e2e')
    ax.set_facecolor('#1e1e2e')

    ax.plot(sem_labels, running_cgpa, color='#89dceb', marker='o',
            linewidth=2.5, markersize=8, zorder=3)
    ax.fill_between(sem_labels, running_cgpa, alpha=0.2, color='#89dceb')

    for i, val in enumerate(running_cgpa):
        ax.text(i, val + 0.1, str(val), ha='center', color='white', fontweight='bold')

    ax.set_ylim(0, 10.5)
    ax.set_xlabel('Semester', color='white', fontsize=12)
    ax.set_ylabel('CGPA', color='white', fontsize=12)
    ax.set_title('📈 CGPA Progress Over Semesters', color='white', fontsize=14, fontweight='bold')
    ax.tick_params(colors='white')
    ax.grid(color='gray', linestyle='--', alpha=0.4, zorder=0)

    for spine in ax.spines.values():
        spine.set_edgecolor('gray')

    plt.tight_layout()
    plt.savefig('cgpa_progress.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ CGPA Progress chart saved!")