{
    "name": "Education Lesson",
    "version": "19.0.1.0.0",
    "category": "Education",
    "summary": "Manage lesson plans",
    "author": "Muslim Foda",
    "website": "https://github.com/muslim-foda/Education",
    "license": "LGPL-3",
    "depends": [
        "base",
        "mail",
        "education_base",
        "education_core",
        "education_grade",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/lesson_plans_views.xml",
        "views/education_lesson_menu_views.xml",
        "views/grade_subject_views.xml",
    ],
    "installable": True,
    "application": True,
}
