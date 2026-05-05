import aiohttp
import asyncio
import json
from SchoolAPI.utils.classCreater import JsonToClassConverter
from SchoolAPI.errors.errors import TokenError, DnevnikError
from SchoolAPI.student.student import Student

class School:
    def __init__(self, student: Student) -> None:
        self.student = student

    async def getSchoolInfo(self):
        if not self.student.isActivate:
            await self.student.activate()

        profile = await self.student.getStudentProfiles()
        if not profile:
            raise DnevnikError("No student profiles found.")

        class_unit_id = profile[0].get('class_unit', {}).get('id', 1)
        school_id = profile[0].get('school_id', 1)
        student_id = profile[0].get('id', self.student.id)

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        url = f"https://school.mos.ru/api/family/web/v1/school_info?class_unit_id={class_unit_id}&school_id={school_id}&student_id={student_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get school info: HTTP {response.status}")
                response = await response.json()
                SchoolObject = JsonToClassConverter.convert("SchoolObject", response)
                SchoolObject.json = response
                return SchoolObject

    async def getSubjects(self):
        if not self.student.isActivate:
            await self.student.activate()

        profile = await self.student.getStudentProfiles()
        if not profile:
            raise DnevnikError("No student profiles found.")

        curricula_id = profile[0].get('curricula', {}).get('id', 1)
        student_id = profile[0].get('id', self.student.id)

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        url = f"https://school.mos.ru/api/family/web/v1/programs/parallel_curriculum/{curricula_id}?student_id={student_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get subjects: HTTP {response.status}")
                response = await response.json()
                SchoolObject = JsonToClassConverter.convert("SchoolObject", response)
                SchoolObject.json = response
                return SchoolObject

    async def getMoscowSchools(self):
        if not self.student.isActivate:
            await self.student.activate()

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        url = "https://school.mos.ru/api/nsi/dictionaries/v1/family_moscow_organizations"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get Moscow schools: HTTP {response.status}")
                response = await response.json()
                if isinstance(response, list):
                    SchoolObject = JsonToClassConverter.convert("SchoolObject", {"payload": response})
                else:
                    SchoolObject = JsonToClassConverter.convert("SchoolObject", response)
                SchoolObject.json = response
                return SchoolObject