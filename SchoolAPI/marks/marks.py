import aiohttp
import asyncio
import json
from datetime import datetime
from SchoolAPI.utils.classCreater import JsonToClassConverter
from SchoolAPI.errors.errors import TokenError, DnevnikError
from SchoolAPI.student.student import Student

class Marks:
    def __init__(self, student: Student) -> None:
        self.student = student

    async def getMarksByDate(self, from_date: str, to_date: str):
        if not self.student.isActivate:
            await self.student.activate()

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        url = f"https://school.mos.ru/api/ej/core/family/v1/marks?student_id={self.student.id}&from={from_date}&to={to_date}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get marks by date: HTTP {response.status}")
                response = await response.json()
                MarksObject = JsonToClassConverter.convert("MarksObject", response)
                MarksObject.json = response
                return MarksObject

    async def getMarksByDates(self, date_from: str, date_to: str):
        if not self.student.isActivate:
            await self.student.activate()

        def convert_date_format(date_str: str) -> str:
            try:
                dt = datetime.strptime(date_str, '%Y-%m-%d')
                return dt.strftime('%d.%m.%Y')
            except ValueError:
                raise ValueError(f"Неверный формат даты: {date_str}. Ожидается YYYY-MM-DD")

        date_from_converted = convert_date_format(date_from)
        date_to_converted = convert_date_format(date_to)
        profile_id = self.student.profiles[0]['id'] if self.student.profiles else self.student.id

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
            "Profile-Id": str(profile_id),
        }
        url = f"https://school.mos.ru/api/ej/core/family/v1/marks?created_at_from={date_from_converted}&created_at_to={date_to_converted}&student_profile_id={profile_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get marks by dates: HTTP {response.status}")
                response = {"data": await response.json()}
                MarksObject = JsonToClassConverter.convert("MarksObject", response)
                MarksObject.json = response
                return MarksObject

    async def getSubjectsMarks(self):
        if not self.student.isActivate:
            await self.student.activate()

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        profile_id = self.student.profiles[0]['id'] if self.student.profiles else self.student.id
        url = f"https://school.mos.ru/api/ej/core/family/v1/subject_marks?student_id={profile_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get subjects marks: HTTP {response.status}")
                response = await response.json()
                MarksObject = JsonToClassConverter.convert("MarksObject", response)
                MarksObject.json = response
                return MarksObject

    async def getFinalMarks(self, academic_year_id: int = 13):
        if not self.student.isActivate:
            await self.student.activate()

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        url = f"https://school.mos.ru/api/ej/core/family/v1/final_marks/v2?person_id={self.student.person_id}&academic_year_id={academic_year_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get final marks: HTTP {response.status}")
                response = await response.json()
                if isinstance(response, list):
                    MarksObject = JsonToClassConverter.convert("MarksObject", {"payload": response})
                else:
                    MarksObject = JsonToClassConverter.convert("MarksObject", response)
                MarksObject.json = response
                return MarksObject

    async def getAcademicYears(self):
        if not self.student.isActivate:
            await self.student.activate()

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        url = "https://school.mos.ru/api/ej/core/family/v1/academic_years"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get academic years: HTTP {response.status}")
                response = await response.json()
                if isinstance(response, list):
                    ScheduleObject = JsonToClassConverter.convert("ScheduleObject", {"payload": response})
                else:
                    ScheduleObject = JsonToClassConverter.convert("ScheduleObject", response)
                ScheduleObject.json = response
                return ScheduleObject