import aiohttp
import asyncio
import json
from typing import Union
from SchoolAPI.utils.classCreater import JsonToClassConverter
from SchoolAPI.errors.errors import TokenError, DnevnikError
from SchoolAPI.student.student import Student

class Homeworks:
    def __init__(self, student: Student):
        self.student = student

    async def getHomeworkByDate(self, from_date: str, to_date: str):
        if not self.student.isActivate:
            await self.student.activate()

        profile = await self.student.getStudentProfiles()
        profile_id = profile[0]['id'] if profile else self.student.id

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        url = f"https://school.mos.ru/api/ej/core/family/v1/homeworks?from={from_date}&to={to_date}&student_id={profile_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get homework by date: HTTP {response.status}")
                response = await response.json()
                HomeworkObject = JsonToClassConverter.convert("HomeworkObject", response)
                HomeworkObject.json = response
                return HomeworkObject

    async def additionalMaterials(self, uuid: Union[list[str], str], homework_entry_student_id: int):
        if not self.student.isActivate:
            await self.student.activate()

        payload = {"materials": []}

        if isinstance(uuid, list):
            for id in uuid:
                payload["materials"].append({
                    "uuid": id,
                    "purpose": "for_home",
                    "selected_mode": "execute",
                    "homework_entry_student_id": homework_entry_student_id
                })
        elif isinstance(uuid, str):
            payload["materials"].append({
                "uuid": uuid,
                "purpose": "for_home",
                "selected_mode": "execute",
                "homework_entry_student_id": homework_entry_student_id
            })

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
            "Content-Type": "application/json",
        }
        url = "https://school.mos.ru/api/family/materials/v1/additional_materials"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.post(url, headers=headers, json=payload) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get additional materials: HTTP {response.status}")
                response = await response.json()
                MaterialsObject = JsonToClassConverter.convert("MaterialsObject", response)
                MaterialsObject.json = response
                return MaterialsObject

    async def getShortHomeworkByDates(self, dates: Union[list[str], str]):
        if not self.student.isActivate:
            await self.student.activate()

        profile = await self.student.getStudentProfiles()
        profile_id = profile[0]['id'] if profile else self.student.id

        if isinstance(dates, str):
            dates_str = dates
        elif isinstance(dates, list):
            dates_str = "%2C".join(dates)

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        url = f"https://school.mos.ru/api/ej/core/family/v1/schedule/short?student_id={profile_id}&dates={dates_str}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get short homework by dates: HTTP {response.status}")
                response = await response.json()
                HomeworkObject = JsonToClassConverter.convert("HomeworkObject", response)
                HomeworkObject.json = response
                return HomeworkObject