# =============================================================
# SCHEMAS.PY
# =============================================================
# Handles all data validation and input structure for the system.
# =============================================================

import re
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, field_validator, StringConstraints


# =============================================================
# 1) TYPE ALIASES
# =============================================================

NameType = Annotated[str, StringConstraints(strip_whitespace=True)]
PasswordType = Annotated[str, StringConstraints(min_length=6, max_length=20)]
TeamType = Annotated[int, Field(gt=0)]


# =============================================================
# 2) ENUMS (Gender & Role)
# =============================================================

class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"
    prefer = "Prefer not to say"


class RoleEnum(str, Enum):
    admin = "Admin"
    teamleader = "Team_leader"
    developer = "Developer"


# =============================================================
# 3) USER CREATE MODEL
# =============================================================

class UserCreate(BaseModel):
    firstname: NameType
    lastname: NameType
    password: PasswordType
    team: TeamType
    email: EmailStr
    gender: GenderEnum
    role: RoleEnum

    # ============================================
    # FIELD VALIDATORS
    # ============================================

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

    @field_validator('firstname')
    @classmethod
    def validate_firstname(cls, value):
        if len(value) < 2:
            raise ValueError('Firstname is too short (min 2 characters)')
        if len(value) > 30:
            raise ValueError('Firstname is too long (max 30 characters)')
        return value

    @field_validator('lastname')
    @classmethod
    def validate_lastname(cls, value):
        if len(value) < 2:
            raise ValueError('Lastname is too short (min 2 characters)')
        if len(value) > 30:
            raise ValueError('Lastname is too long (max 30 characters)')
        return value

    @field_validator('gender')
    @classmethod
    def validate_gender(cls, value):
        if value in ["Select Gender", "None", ""]:
            raise ValueError("Please select a valid gender option before continuing.")
        return value

    @field_validator('role')
    @classmethod
    def validate_role(cls, value):
        if value in ["Select Role", "None", ""]:
            raise ValueError("Please select a valid role option before continuing.")
        return value

    @field_validator('team')
    @classmethod
    def validate_team(cls, value):
        if value <= 0:
            raise ValueError("Please select a valid team number before continuing.")
        return value


# =============================================================
# 4) PASSWORD RESET MODEL
# =============================================================

class PasswordReset(BaseModel):
    email: EmailStr
    password: PasswordType

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
