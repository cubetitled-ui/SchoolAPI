import aiohttp
import asyncio
import json
from SchoolAPI.utils.classCreater import JsonToClassConverter
from SchoolAPI.errors.errors import TokenError, DnevnikError
from SchoolAPI.student.student import Student

class Schedule:
    def __init__(self, student: Student) -> None:
        self.student = student

    async def getScheduleByDate(self, date: str):
        if not self.student.isActivate:
            await self.student.activate()

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        url = f"https://school.mos.ru/api/ej/core/family/v1/schedule?student_id={self.student.id}&date={date}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get schedule by date: HTTP {response.status}")
                response = await response.json()
                ScheduleDay = JsonToClassConverter.convert("ScheduleDay", response)
                ScheduleDay.json = response
                return ScheduleDay

    async def getScheduleByDates(self, begin_date: str, end_date: str):
        if not self.student.isActivate:
            await self.student.activate()

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
            "X-Mes-Role": "student",
        }
        url = f"https://school.mos.ru/api/eventcalendar/v1/api/events?person_ids={self.student.person_id}&begin_date={begin_date}&end_date={end_date}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get schedule by dates: HTTP {response.status}")
                response = await response.json()
                ScheduleDays = JsonToClassConverter.convert("ScheduleDays", response)
                ScheduleDays.json = response
                return ScheduleDays

    async def getSchedulePeriods(self, academic_year_id: int = 13):
        if not self.student.isActivate:
            await self.student.activate()

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        url = f"https://school.mos.ru/api/ej/core/family/v1/periods_schedules?academic_year_id={academic_year_id}&student_profile_id={self.student.id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get schedule periods: HTTP {response.status}")
                response = await response.json()
                if isinstance(response, list):
                    SchedulePeriods = JsonToClassConverter.convert("SchedulePeriods", {"payload": response})
                else:
                    SchedulePeriods = JsonToClassConverter.convert("SchedulePeriods", response)
                SchedulePeriods.json = response
                return SchedulePeriods

    async def getAllSchedulePeriods(self):
        if not self.student.isActivate:
            await self.student.activate()

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        url = "https://school.mos.ru/api/nsi/dictionaries/v1/academic_years"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get all schedule periods: HTTP {response.status}")
                response = await response.json()
                if isinstance(response, list):
                    SchedulePeriods = JsonToClassConverter.convert("SchedulePeriods", {"payload": response})
                else:
                    SchedulePeriods = JsonToClassConverter.convert("SchedulePeriods", response)
                SchedulePeriods.json = response
                return SchedulePeriods

    async def getCurrentPeriod(self):
        periods = (await self.getAllSchedulePeriods()).payload
        for period in periods:
            if period.get("current_year", False):
                return period
        return None

    async def getControlTestDays(self, from_day: str, to_day: str):
        if not self.student.isActivate:
            await self.student.activate()

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        profile_id = self.student.profiles[0]['id'] if self.student.profiles else self.student.id
        url = f"https://school.mos.ru/api/ej/plan/family/v1/test_lessons/period?student_profile_id={profile_id}&from={from_day}&to={to_day}&student_person_id={self.student.person_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get control test days: HTTP {response.status}")
                response = await response.json()
                if isinstance(response, list):
                    SchedulePeriods = JsonToClassConverter.convert("SchedulePeriods", {"payload": response})
                else:
                    SchedulePeriods = JsonToClassConverter.convert("SchedulePeriods", response)
                SchedulePeriods.json = response
                return SchedulePeriods