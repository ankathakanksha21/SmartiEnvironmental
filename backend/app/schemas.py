"""What the API accepts and returns, and the rules for valid input.

FastAPI checks every request against these classes before the route runs.
main.py turns any failure into {field: message} for the frontend forms.
"""

import re
from datetime import datetime
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, BeforeValidator, ConfigDict, ValidationInfo

OnboardingStatus = Literal["New Enquiry", "In Progress", "Active"]
StaffRole = Literal["Fitter", "Maintenance Engineer"]
JobStatus = Literal["Pending", "In Progress", "Completed"]

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


def chosen_from_list(value, info: ValidationInfo):
    """A dropdown with nothing selected sends an empty string."""
    if value == "":
        names = {"customer_id": "a customer", "staff_id": "a staff member"}
        raise ValueError(f"Choose {names[info.field_name]}.")
    return value


def booking_time(value) -> datetime:
    """Read the date input's text, with our own messages for anything unreadable."""
    if value == "":
        raise ValueError("Date and time is required.")
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError("Enter a valid date and time.") from None
    # Times are local with no offset. An offset would crash the comparison with datetime.now().
    if parsed.tzinfo is not None:
        raise ValueError("Enter a valid date and time.")
    # Drop the seconds, so two bookings for 09:30 count as the same time.
    return parsed.replace(second=0, microsecond=0)


RequiredText = Annotated[str, AfterValidator(required)]
Phone = Annotated[str, AfterValidator(valid_phone)]
OptionalEmail = Annotated[str, AfterValidator(valid_email_or_blank)]
ChosenId = Annotated[int, BeforeValidator(chosen_from_list)]
BookingTime = Annotated[datetime, BeforeValidator(booking_time)]


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


class StaffCreate(RequestBody):
    name: RequiredText
    role: StaffRole
    phone: Phone


class StaffDetails(StaffCreate):
    is_active: bool


class StaffOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    role: StaffRole
    phone: str
    is_active: bool


class JobDetails(RequestBody):
    customer_id: ChosenId
    staff_id: ChosenId
    description: RequiredText
    scheduled_at: BookingTime


class JobStatusUpdate(BaseModel):
    status: JobStatus


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer: CustomerOut
    staff: StaffOut
    description: str
    scheduled_at: datetime
    status: JobStatus
    is_overdue: bool
