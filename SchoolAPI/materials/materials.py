import aiohttp  # type: ignore
import asyncio
import json
from SchoolAPI.utils.classCreater import JsonToClassConverter
from SchoolAPI.errors.errors import TokenError, DnevnikError
from SchoolAPI.student.student import Student


class Materials:
    def __init__(self, student: Student) -> None:
        self.student = student
        
    async def getAllMaterials(self):
        async with aiohttp.ClientSession() as session:
            payload = {
                "query": {"filter": {"sorting": {"field": "published_at", "direction": "desc"}}}, 
                'sort': {'field': 'published_at', 'order': 'desc'}, 
                'page': 1,
                'per_page': 100000,
            }

            response = await session.post(
                f"https://uchebnik.mos.ru/search/api/v3/materials",
                 headers={
                     'Authorization': f'Bearer {self.student.token}',
                     'User-Id': str(self.student.id),
                  }, json=payload)

            if response.status != 200:
                pass
            
            response = await response.json()
            
            MaterialsObj = JsonToClassConverter.convert("Materials", response)
            MaterialsObj.json = response
            
            return MaterialsObj
        
        
# Let's continue editing other files now - notification.py next!
