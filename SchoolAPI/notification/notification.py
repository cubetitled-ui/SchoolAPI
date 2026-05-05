import aiohttp
import asyncio
import json
from SchoolAPI.utils.classCreater import JsonToClassConverter
from SchoolAPI.errors.errors import TokenError, DnevnikError
from SchoolAPI.student.student import Student

class Notification:
    def __init__(self, student: Student) -> None:
        self.student = student

    async def getNotifications(self):
        if not self.student.isActivate:
            await self.student.activate()

        profile = await self.student.getStudentProfiles()
        profile_id = profile[0]['id'] if profile else self.student.id

        headers = {
            "Authorization": f"Bearer {self.student.token}",
            "X-Mes-Subsystem": "familymp",
            "Profile-Id": str(profile_id),
        }
        url = f"https://school.mos.ru/api/family/mobile/v1/notifications/search?student_id={self.student.id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    await self.student.refresh()
                    async with session.get(url, headers=headers) as retry_response:
                        response = retry_response
                if response.status != 200:
                    raise DnevnikError(f"Failed to get notifications: HTTP {response.status}")
                response = await response.json()
                Notifications = JsonToClassConverter.convert("Notifications", response)
                Notifications.json = response
                return Notifications