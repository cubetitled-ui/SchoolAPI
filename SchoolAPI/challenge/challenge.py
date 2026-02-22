import aiohttp  # type: ignore
import asyncio
import json
from SchoolAPI.utils.classCreater import JsonToClassConverter
from SchoolAPI.errors.errors import TokenError, DnevnikError, LibError
from SchoolAPI.student.student import Student
from typing import Union


class Challenge:
    def __init__(self, student: Student = None) -> None:
        self.student = student

    async def getChallengeUuid(self, link):
        pass
