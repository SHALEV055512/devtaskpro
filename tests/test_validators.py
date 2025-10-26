import pytest
from backend.schemas import UserCreate
from pydantic import ValidationError

VALID_USER = {
    "firstname": "Shalev",
    "lastname": "Harari",
    "password": "Password123",
    "team": 1,
    "email": "Shalev526@gmail.com",
    "gender": "Male",
    "role": "Developer"
}


# -------------------------
# POSITIVE TEST (VALID INPUT)
# -------------------------

def test_valid_user_passes():
     user = UserCreate(**VALID_USER)
     assert user.firstname == "Shalev"
     assert user.lastname == "Harari"
     assert user.team == 1
     assert user.email == "Shalev526@gmail.com"
     assert user.gender == "Male"
     assert user.role == "Developer"


# -------------------------
# PASSWORD VALIDATION TESTS
# -------------------------

def test_password_missing_uppercase():
    data = VALID_USER.copy()
    data["password"] = "password123"  
    with pytest.raises(ValueError) as exc:
        UserCreate(**data)
    assert "Password must contain at least one uppercase letter" in str(exc.value)

def test_password_missing_lowercase():
    data = VALID_USER.copy()
    data["password"] = "PASSWORD123"  
    with pytest.raises(ValueError) as exc:
        UserCreate(**data)
    assert "Password must contain at least one lowercase letter" in str(exc.value)

def test_password_missing_number():
    data = VALID_USER.copy()
    data["password"] = "Password"  
    with pytest.raises(ValueError) as exc:
        UserCreate(**data)
    assert "Password must contain at least one number" in str(exc.value)


# -------------------------
# FIRSTNAME VALIDATION TESTS
# -------------------------

def test_firstname_too_short():
    data = VALID_USER.copy()
    data["firstname"] = "A" 
    with pytest.raises(ValueError) as exc:
        UserCreate(**data)
    assert "Firstname is too short (min 2 characters)" in str(exc.value)

def test_firstname_too_long():
    data = VALID_USER.copy()
    data["firstname"] = "A" * 31  
    with pytest.raises(ValueError) as exc:
        UserCreate(**data)
    assert "Firstname is too long (max 30 characters)" in str(exc.value)


# -------------------------
# LASTNAME VALIDATION TESTS
# -------------------------

def test_lastname_too_short():
    data = VALID_USER.copy()
    data["lastname"] = "A"  
    with pytest.raises(ValueError) as exc:
        UserCreate(**data)
    assert "Lastname is too short (min 2 characters)" in str(exc.value)

def test_lastname_too_long():
    data = VALID_USER.copy()
    data["lastname"] = "A" * 31 
    with pytest.raises(ValueError) as exc:
        UserCreate(**data)
    assert "Lastname is too long (max 30 characters)" in str(exc.value)


# -------------------------
# GENDER VALIDATION TESTS
# -------------------------

@pytest.mark.parametrize("invalid_gender", ["Select Gender", "None", ""])
def test_invalid_gender_options(invalid_gender):
    data = VALID_USER.copy()
    data["gender"] = invalid_gender
    with pytest.raises(ValidationError) as exc:
        UserCreate(**data)
    assert "Male" in str(exc.value)
    assert "Female" in str(exc.value)
    assert "Other" in str(exc.value)
    assert "Prefer not to say" in str(exc.value)


# -------------------------
# ROLE VALIDATION TESTS
# -------------------------

@pytest.mark.parametrize("invalid_role", ["Select Role", "None", ""])
def test_invalid_role_options(invalid_role):
    data = VALID_USER.copy()
    data["role"] = invalid_role
    with pytest.raises(ValidationError) as exc:
        UserCreate(**data)
    assert "Admin" in str(exc.value)
    assert "Team leader" in str(exc.value)
    assert "Developer" in str(exc.value)


# -------------------------
# TEAM VALIDATION TESTS
# -------------------------

@pytest.mark.parametrize("invalid_team", [0, -1])
def test_invalid_team_number(invalid_team):
    data = VALID_USER.copy()
    data["team"] = invalid_team
    with pytest.raises(ValidationError) as exc:
        UserCreate(**data)
    assert "Input should be greater than 0" in str(exc.value)