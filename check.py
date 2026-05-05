import asyncio
import sys
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

# Добавляем путь к библиотеке
sys.path.insert(0, os.path.abspath("."))

from SchoolAPI import (
    Student,
    Schedule,
    Marks,
    Homeworks,
    Notification,
    School,
    Materials,
)

@dataclass
class TestResult:
    method_name: str
    class_name: str
    status: str  # "✅ Success", "❌ Failed", "⚠️ Error"
    error: Optional[str] = None
    data: Optional[Any] = None

class LibraryTester:
    def __init__(
        self,
        token: str,
        student_id: Optional[int] = None,
        student_person_id: Optional[str] = None,
    ):
        self.token = token
        self.student_id = student_id
        self.student_person_id = student_person_id
        self.results: List[TestResult] = []

    async def test_student(self) -> List[TestResult]:
        """Тестирует методы класса Student."""
        results = []
        try:
            student = Student(token=self.token)
            await student.activate()
            results.append(
                TestResult(
                    method_name="activate",
                    class_name="Student",
                    status="✅ Success",
                    data=str(student),
                )
            )
        except Exception as e:
            results.append(
                TestResult(
                    method_name="activate",
                    class_name="Student",
                    status="❌ Failed",
                    error=str(e),
                )
            )
        return results

    async def test_schedule(self, student: Student) -> List[TestResult]:
        """Тестирует методы класса Schedule."""
        results = []
        schedule = Schedule(student)
        today = datetime.now().strftime("%Y-%m-%d")

        # Проверяем getScheduleByDate
        try:
            data = await schedule.getScheduleByDate(today)
            results.append(
                TestResult(
                    method_name="getScheduleByDate",
                    class_name="Schedule",
                    status="✅ Success",
                    data=str(data)[:100] + "...",  # Обрезаем длинный вывод
                )
            )
        except Exception as e:
            results.append(
                TestResult(
                    method_name="getScheduleByDate",
                    class_name="Schedule",
                    status="❌ Failed",
                    error=str(e),
                )
            )

        # Проверяем getScheduleByDates
        try:
            data = await schedule.getScheduleByDates(today, today)
            results.append(
                TestResult(
                    method_name="getScheduleByDates",
                    class_name="Schedule",
                    status="✅ Success",
                    data=str(data)[:100] + "...",
                )
            )
        except Exception as e:
            results.append(
                TestResult(
                    method_name="getScheduleByDates",
                    class_name="Schedule",
                    status="❌ Failed",
                    error=str(e),
                )
            )

        # Проверяем getSchedulePeriods
        try:
            data = await schedule.getSchedulePeriods()
            results.append(
                TestResult(
                    method_name="getSchedulePeriods",
                    class_name="Schedule",
                    status="✅ Success",
                    data=str(data)[:100] + "...",
                )
            )
        except Exception as e:
            results.append(
                TestResult(
                    method_name="getSchedulePeriods",
                    class_name="Schedule",
                    status="❌ Failed",
                    error=str(e),
                )
            )

        return results

    async def test_marks(self, student: Student) -> List[TestResult]:
        """Тестирует методы класса Marks."""
        results = []
        marks = Marks(student)
        today = datetime.now().strftime("%Y-%m-%d")

        # Проверяем getMarksByDate
        try:
            data = await marks.getMarksByDate(today, today)
            results.append(
                TestResult(
                    method_name="getMarksByDate",
                    class_name="Marks",
                    status="✅ Success",
                    data=str(data)[:100] + "...",
                )
            )
        except Exception as e:
            results.append(
                TestResult(
                    method_name="getMarksByDate",
                    class_name="Marks",
                    status="❌ Failed",
                    error=str(e),
                )
            )

        # Проверяем getSubjectsMarks
        try:
            data = await marks.getSubjectsMarks()
            results.append(
                TestResult(
                    method_name="getSubjectsMarks",
                    class_name="Marks",
                    status="✅ Success",
                    data=str(data)[:100] + "...",
                )
            )
        except Exception as e:
            results.append(
                TestResult(
                    method_name="getSubjectsMarks",
                    class_name="Marks",
                    status="❌ Failed",
                    error=str(e),
                )
            )

        return results

    async def test_homeworks(self, student: Student) -> List[TestResult]:
        """Тестирует методы класса Homeworks."""
        results = []
        homeworks = Homeworks(student)
        today = datetime.now().strftime("%Y-%m-%d")

        # Проверяем getHomeworkByDate
        try:
            data = await homeworks.getHomeworkByDate(today, today)
            results.append(
                TestResult(
                    method_name="getHomeworkByDate",
                    class_name="Homeworks",
                    status="✅ Success",
                    data=str(data)[:100] + "...",
                )
            )
        except Exception as e:
            results.append(
                TestResult(
                    method_name="getHomeworkByDate",
                    class_name="Homeworks",
                    status="❌ Failed",
                    error=str(e),
                )
            )

        return results

    async def test_notification(self, student: Student) -> List[TestResult]:
        """Тестирует методы класса Notification."""
        results = []
        notification = Notification(student)

        # Проверяем getNotifications
        try:
            data = await notification.getNotifications()
            results.append(
                TestResult(
                    method_name="getNotifications",
                    class_name="Notification",
                    status="✅ Success",
                    data=str(data)[:100] + "...",
                )
            )
        except Exception as e:
            results.append(
                TestResult(
                    method_name="getNotifications",
                    class_name="Notification",
                    status="❌ Failed",
                    error=str(e),
                )
            )

        return results

    async def test_school(self, student: Student) -> List[TestResult]:
        """Тестирует методы класса School."""
        results = []
        school = School(student)

        # Проверяем getSchoolInfo
        try:
            data = await school.getSchoolInfo()
            results.append(
                TestResult(
                    method_name="getSchoolInfo",
                    class_name="School",
                    status="✅ Success",
                    data=str(data)[:100] + "...",
                )
            )
        except Exception as e:
            results.append(
                TestResult(
                    method_name="getSchoolInfo",
                    class_name="School",
                    status="❌ Failed",
                    error=str(e),
                )
            )

        # Проверяем getSubjects
        try:
            data = await school.getSubjects()
            results.append(
                TestResult(
                    method_name="getSubjects",
                    class_name="School",
                    status="✅ Success",
                    data=str(data)[:100] + "...",
                )
            )
        except Exception as e:
            results.append(
                TestResult(
                    method_name="getSubjects",
                    class_name="School",
                    status="❌ Failed",
                    error=str(e),
                )
            )

        return results

    async def test_materials(self, student: Student) -> List[TestResult]:
        """Тестирует методы класса Materials."""
        results = []
        materials = Materials(student)

        # Проверяем getAllMaterials
        try:
            data = await materials.getAllMaterials()
            results.append(
                TestResult(
                    method_name="getAllMaterials",
                    class_name="Materials",
                    status="✅ Success",
                    data=str(data)[:100] + "...",
                )
            )
        except Exception as e:
            results.append(
                TestResult(
                    method_name="getAllMaterials",
                    class_name="Materials",
                    status="❌ Failed",
                    error=str(e),
                )
            )

        return results

    async def run_all_tests(self) -> List[TestResult]:
        """Запускает все тесты."""
        # Тестируем Student
        student_results = await self.test_student()
        self.results.extend(student_results)

        # Если Student не активировался, остальные тесты не имеют смысла
        if not any(
            result.method_name == "activate" and result.status == "✅ Success"
            for result in student_results
        ):
            self.results.append(
                TestResult(
                    method_name="ALL_OTHER_TESTS",
                    class_name="ALL",
                    status="⚠️ Skipped (Student not activated)",
                    error="Student.activate() failed, so other tests were skipped.",
                )
            )
            return self.results

        # Создаём объект Student для остальных тестов
        student = Student(token=self.token)
        await student.activate()

        # Тестируем остальные классы
        self.results.extend(await self.test_schedule(student))
        self.results.extend(await self.test_marks(student))
        self.results.extend(await self.test_homeworks(student))
        self.results.extend(await self.test_notification(student))
        self.results.extend(await self.test_school(student))
        self.results.extend(await self.test_materials(student))

        return self.results

    def print_report(self) -> None:
        """Печатает отчёт о тестировании."""
        print("\n" + "=" * 100)
        print("ОТЧЁТ О ТЕСТИРОВАНИИ БИБЛИОТЕКИ SchoolAPI")
        print("=" * 100 + "\n")

        success_count = 0
        fail_count = 0
        error_count = 0

        for result in self.results:
            if result.status == "✅ Success":
                success_count += 1
            elif result.status == "❌ Failed":
                fail_count += 1
            else:
                error_count += 1

            print(
                f"[{result.class_name}.{result.method_name}] -> {result.status}"
                + (f" | Data: {result.data}" if result.data else "")
                + (f" | Error: {result.error}" if result.error else "")
            )

        print("\n" + "=" * 100)
        print(f"ИТОГО: {success_count} ✅ | {fail_count} ❌ | {error_count} ⚠️")
        print("=" * 100 + "\n")

async def main():
    # Подставь свои значения
    TOKEN = "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxOTU0NzQzIiwic2NwIjoib3BlbmlkIHByb2ZpbGUiLCJuYmYiOjE3Nzc3MTk3OTQsIm1zaCI6IjY2M2FjMGQ5LTkzNDctNGQzYy04OGMyLTQ4MGJlNzJjYmU2OCIsImF0aCI6InN1ZGlyIiwiaXNzIjoiaHR0cHM6XC9cL3NjaG9vbC5tb3MucnUiLCJybHMiOiJ7MTpbMjA6MjpbXSwzMDo0OltdLDQwOjE6W10sMTgzOjE2OltdLDIxMToxOTpbXSw1MjU6NDQ6W10sNTMzOjQ4OltdXX0iLCJleHAiOjE3NzgzMjQ1OTQsImlhdCI6MTc3NzcxOTc5NCwianRpIjoiMjk4NjI4NDctMDRhMy00YmFjLTg2MjgtNDcwNGEzYWJhYzllIiwic3NvIjoiOGY5NTA0ZGYtODcwOS00MDNmLTllZmItY2ViZDIzZDU3NTQzIn0.a-rSlB2ULjFyD7k2vMIpQ7ochsQ6zGv8ALJ-kOBV_eI8P3YwjBdlLGyYx9Fq-jy3yfheBQLUeH86rdTsr2bSWVAkfePbCjDEkgkyJadre9d3eI9vdNJEYqCEBVNSpuOYTeOpUGrxDAlD0-BQsme2SFTDqYQAjrd0SK3KTthkbjFXXuKedCf8r7kjVqp4hDDmvDz4rKZcHdOJpcvR9IKayoxKdvWmx26D3MNvn4sm9sI502Bw9br7qvcEl937iaEVknua2a0GCQ3FNhq80gM0fnWDI83VS2MJOBHc9W5IcH10uIoyViW0s2msN_5OOMgTjaNlgg70eCnXX0Ep-fO9gw"
    STUDENT_ID = 15071555
    STUDENT_PERSON_ID = "663ac0d9-9347-4d3c-88c2-480be72cbe68"

    tester = LibraryTester(
        token=TOKEN,
        student_id=STUDENT_ID,
        student_person_id=STUDENT_PERSON_ID,
    )
    results = await tester.run_all_tests()
    tester.print_report()

if __name__ == "__main__":
    asyncio.run(main())