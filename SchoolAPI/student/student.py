import aiohttp  # type: ignore
import asyncio
import json
from SchoolAPI.utils.classCreater import JsonToClassConverter
from SchoolAPI.errors.errors import TokenError, DnevnikError, LibError

class Student:
    def __init__(self, token: str) -> None:
        self.token = token
        self.isActivate = False
        self.session = None

    def __str__(self):
        if self.isActivate:
            return f"Student Object: {self.session.last_name} {self.session.first_name} {self.session.middle_name} [{self.session.id}]\nID: {self.session.person_id}\nDate of birth: {self.session.date_of_birth}"
        else:
            return f"Student Object: not activate!"


    def __getattribute__(self, name):
        allowed_attrs = ["__str__", 'token', 'isActivate', "activate", "getSession", "getPassport", "getPerson", "getStudentProfiles", "getUserInfo", "refresh", "session"]
        if name not in allowed_attrs and not super().__getattribute__('isActivate'):
            raise LibError("The object is not activated! Call `await Student.activate()` before use.")
        return super().__getattribute__(name)


# Let's continue editing other files now - marks.py next!
