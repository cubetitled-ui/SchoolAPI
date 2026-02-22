# SchoolAPI - Библиотека для работы с МЭШ API
from .student.student import Student
from .schedule.schedule import Schedule
from .marks.marks import Marks
from .homeworks.homeworks import Homeworks
from .notification.notification import Notification
from .school.school import School
from .materials.materials import Materials

__all__ = [
    "Student",
    "Schedule", 
    "Marks",
    "Homeworks",
    "Notification",
    "School",
    "Materials"
]
