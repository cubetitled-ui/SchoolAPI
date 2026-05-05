import aiohttp
import asyncio
import json
from SchoolAPI.utils.classCreater import JsonToClassConverter
from SchoolAPI.errors.errors import TokenError, DnevnikError, LibError

class Student:
    def __init__(self, token: str) -> None:
        self.token = token
        self.isActivate = False
        self.session = None
        self.id = None
        self.person_id = None
        self.first_name = None
        self.last_name = None
        self.middle_name = None
        self.date_of_birth = None
        self.profiles = []

    def __str__(self):
        if self.isActivate:
            return (
                f"Student Object: {self.last_name} {self.first_name} {self.middle_name} [{self.id}]\n"
                f"ID: {self.person_id}\nDate of birth: {self.date_of_birth}"
            )
        else:
            return "Student Object: not activated!"

    def __getattribute__(self, name):
        allowed_attrs = [
            "__str__", "token", "isActivate", "activate", "getSession", "getPassport",
            "getPerson", "getStudentProfiles", "getUserInfo", "refresh", "session",
            "id", "person_id", "first_name", "last_name", "middle_name", "date_of_birth", "profiles"
        ]
        if name not in allowed_attrs and not super().__getattribute__('isActivate'):
            raise LibError("The object is not activated! Call `await Student.activate()` before use.")
        return super().__getattribute__(name)

    async def activate(self) -> None:
        """Активирует студента, получая данные сессии с эндпоинта /api/family/web/v1/session."""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        url = "https://school.mos.ru/api/family/web/v1/session"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.session = data
                        self.isActivate = True
                        # Извлекаем данные о студенте
                        self.id = data.get("id") or data.get("student_id")
                        self.person_id = data.get("person_id") or data.get("student_person_id")
                        self.first_name = data.get("first_name")
                        self.last_name = data.get("last_name")
                        self.middle_name = data.get("middle_name")
                        self.date_of_birth = data.get("date_of_birth")
                        self.profiles = data.get("profiles", [])
                    else:
                        raise TokenError(f"Failed to activate student: HTTP {response.status}")
        except aiohttp.ClientError as e:
            raise TokenError(f"Network error: {str(e)}")

    async def refresh(self) -> None:
        """Обновляет сессию студента."""
        await self.activate()

    async def getSession(self):
        """Возвращает данные сессии."""
        if not self.isActivate:
            await self.activate()
        return self.session

    async def getPassport(self):
        """Получает данные паспорта студента."""
        if not self.isActivate:
            await self.activate()
        # Реализуем запрос к /api/persondata/v1/passport
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        url = f"https://school.mos.ru/api/persondata/v1/passport?person_id={self.person_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise DnevnikError(f"Failed to get passport: HTTP {response.status}")

    async def getPerson(self):
        """Получает данные о личности студента."""
        if not self.isActivate:
            await self.activate()
        # Реализуем запрос к /api/persondata/v1/person
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Mes-Subsystem": "familyweb",
        }
        url = f"https://school.mos.ru/api/persondata/v1/person?person_id={self.person_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise DnevnikError(f"Failed to get person data: HTTP {response.status}")

    async def getStudentProfiles(self):
        """Получает профили студента."""
        if not self.isActivate:
            await self.activate()
        return self.profiles

    async def getUserInfo(self):
        """Получает информацию о пользователе."""
        if not self.isActivate:
            await self.activate()
        return self.session