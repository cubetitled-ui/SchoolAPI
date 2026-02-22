import asyncio
from SchoolAPI.student.student import Student
from SchoolAPI.utils.utils import *
from SchoolAPI.schedule.schedule import Schedule
from SchoolAPI.marks.marks import Marks
from SchoolAPI.homeworks.homeworks import Homeworks
from SchoolAPI.notification.notification import Notification
from SchoolAPI.school.school import School
from SchoolAPI.materials.materials import Materials


async def test():
    token = "eyJhbGciOiJIUzI1..."
    student = Student(token)

    day1 = Utils.getNormalDate(2024, 2, 4)
    day2 = Utils.getNormalDate(2025, 6, 1)
    
if __name__ == '__main__':
    asyncio.run(test())
