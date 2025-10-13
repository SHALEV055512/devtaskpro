import re
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field,field_validator, StringConstraints

NameType = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=30)]
PasswordType = Annotated[str, StringConstraints(min_length=6, max_length=20)]
TeamType = Annotated[int, Field(gt=0)]



class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"
    prefer = "Prefer not to say"

class RoleEnum(str, Enum):
    admin = "Admin"
    teamleader = "Team Leader"
    developer = "Developer"

class UserCreate(BaseModel):
    firstname: NameType
    lastname: NameType
    password: PasswordType
    team: TeamType
    email: EmailStr
    gender: GenderEnum
    role: RoleEnum

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if not re.search(r'[A-Z]', value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', value):
            raise ValueError('Password must contain at least one number')
        return value

    # ✅ בדיקות שם פרטי ושם משפחה (אורך)
    @field_validator('firstname', 'lastname')
    @classmethod
    def validate_names(cls, value):
        if len(value) < 2:
            raise ValueError('Name is too short (min 2 characters)')
        if len(value) > 30:
            raise ValueError('Name is too long (max 30 characters)')
        return value

    # ✅ בדיקות בחירה של Gender ו־Role
    @field_validator('gender', 'role')
    @classmethod
    def check_selected(cls, value):
        if value in ["Select Role", "Select Gender", "None", ""]:
            raise ValueError('You must select a valid option')
        return value
