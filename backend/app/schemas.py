"""What the API accepts and returns, and the rules for valid input.

FastAPI checks every request against these classes before the route runs.
main.py turns any failure into {field: message} for the frontend forms.
"""

import re
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, ConfigDict, ValidationInfo

OnboardingStatus = Literal["New Enquiry", "In Progress", "Active"]
StaffRole = Literal["Fitter", "Maintenance Engineer"]

PHONE_PATTERN = re.compile(r"\+?[\d\s()-]+")
EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def required(value: str, info: ValidationInfo) -> str:
    if not value:
        raise ValueError(f"{info.field_name.capitalize()} is required.")
    return value


def valid_phone(value: str, info: ValidationInfo) -> str:
    required(value, info)
    digit_count = sum(character.isdigit() for character in value)
    if not PHONE_PATTERN.fullmatch(value) or not 7 <= digit_count <= 15:
        raise ValueError("Enter a valid phone number.")
    return value


def valid_email_or_blank(value: str) -> str:
    if value and not EMAIL_PATTERN.fullmatch(value):
        raise ValueError("Enter a valid email address.")
    return value


RequiredText = Annotated[str, AfterValidator(required)]
Phone = Annotated[str, AfterValidator(valid_phone)]
OptionalEmail = Annotated[str, AfterValidator(valid_email_or_blank)]


class RequestBody(BaseModel):
    # Strip spaces first, so a field holding only spaces counts as blank.
    model_config = ConfigDict(str_strip_whitespace=True)


class CustomerDetails(RequestBody):
    name: RequiredText
    phone: Phone
    email: OptionalEmail = ""
    address: RequiredText


class CustomerCreate(CustomerDetails):
    onboarding_status: OnboardingStatus = "New Enquiry"


class CustomerStatusUpdate(BaseModel):
    onboarding_status: OnboardingStatus


class CustomerOut(BaseModel):
    # Lets FastAPI read the values from a SQLAlchemy object.
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    email: str
    address: str
    onboarding_status: OnboardingStatus


class StaffDetails(RequestBody):
    name: RequiredText
    role: StaffRole
    phone: Phone
    is_active: bool = True


class StaffOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    role: StaffRole
    phone: str
    is_active: bool
