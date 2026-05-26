import json
from anthropic import Anthropic
from .models import Service, Booking, Availability
from datetime import date, timedelta
from django.core.mail import send_mail
from django.conf import settings

client = Anthropic()
SYSTEM_PROMPT = """
You are a friendly and professional booking assistant for Enhanced Beauty, a permanent makeup and paramedical tattoo studio.

You help customers with:
- Learning about available services and pricing
- Checking available appointment slots
- Booking appointments
- Cancelling or rescheduling appointments

Services offered include eyebrows, eye liner, lips, paramedical tattoo, fine line tattoo, and consultations.

Rules you must follow:
- Only discuss topics related to Enhanced Beauty and booking appointments.
- Always collect the customer's full name, email address, and phone number before creating a booking.
- Always confirm the full appointment details with the customer before finalizing a booking.
- Always give the customer their booking reference number after a successful booking.
- Be warm, patient, and professional at all times.
- Never use markdown tables or numbered/bulleted lists. When listing services, start each service name with a dash (-) on its own line. Do not put multiple services on the same line. Bold text is allowed for emphasis only.
- If the customer has already provided their name, email, phone, or booking reference earlier in the conversation, use that information without asking again. Only ask the customer to confirm if the details are correct.
"""

TOOLS = [
    {
        "name": "list_services",
        "description": "Get all available services with their name, "
        "price, "
        "duration, "
        "and description.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "check_availability",
        "description": "Check available appointment slots. "
        "Optionally filter by date range.",
        "input_schema": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start of date range in YYYY-MM-DD format. Defaults to today.",
                },
                "end_date": {
                    "type": "string",
                    "description": "End of date range in"
                    "YYYY-MM-DD format. "
                    "Defaults to 30 days from today.",
                },
            },
            "required": [],
        },
    },
    {
        "name": "create_booking",
        "description": "Create a booking for a customer. Requires an "
        "availability slot ID, service ID, "
        "and customer contact information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "availability_id": {
                    "type": "integer",
                    "description": "The ID of the availability slot to book.",
                },
                "service_id": {
                    "type": "integer",
                    "description": "The ID of the service being booked.",
                },
                "name": {"type": "string", "description": "Full name of the customer."},
                "email": {
                    "type": "string",
                    "description": "Email address of the customer.",
                },
                "phone": {
                    "type": "string",
                    "description": "Phone number of the customer.",
                },
            },
            "required": ["availability_id", "service_id", "name", "email", "phone"],
        },
    },
    {
        "name": "cancel_booking",
        "description": "Cancel a booking that was already created. "
        "Requires a reference.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reference": {
                    "type": "string",
                    "description": "Reference for the booking.",
                }
            },
            "required": ["reference"],
        },
    },
    {
        "name": "get_booking",
        "description": "Get booking that was scheduled.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reference": {
                    "type": "string",
                    "description": "Reference for the booking.",
                }
            },
            "required": ["reference"],
        },
    },
]


def list_services():
    services = Service.objects.all()
    result = []
    for service in services:
        result.append(
            {
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "price": str(service.price),
                "duration": service.duration,
            }
        )
    return result


def check_availability(start_date=None, end_date=None):
    if start_date is None:
        start_date = date.today()

    if end_date is None:
        end_date = date.today() + timedelta(days=30)

    slots = Availability.objects.filter(
        date__gte=start_date, date__lte=end_date, booked=False
    )

    result = []
    for slot in slots:
        result.append(
            {
                "id": slot.id,
                "date": slot.date.strftime("%A, %B %d, %Y"),
                "location": slot.location,
                "start_time": str(slot.start_time),
                "end_time": str(slot.end_time),
            }
        )
    return result

def send_confirmation_email(booking):
    subject = f"Appointment Confirmation - {booking.reference}"
    message = f"""
        Hello {booking.name},
            Thank you for booking an appointment with Enhanced Beauty. Your appointment status is {booking.status}, ref. number {booking.reference} on {booking.availability.date} at {booking.availability.start_time} for a {booking.service.name} at {booking.availability.location}. Please visit the site if you need to cancel or reschedule your appointment. Looking forward to serving you. Have a wonderful day.
        """
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(subject, message, from_email, [booking.email, settings.DEFAULT_FROM_EMAIL])
    except Exception:
        pass

def send_cancellation_email(booking):
    subject = f"Appointment Cancellation - {booking.reference}"
    message = f"""
        Hello {booking.name},
            Thank you for booking an appointment with Enhanced Beauty. Your appointment (ref. number {booking.reference}) on {booking.availability.date} at {booking.availability.start_time} for a {booking.service.name} has been cancelled. If you need to reschedule please visit the site. Thank you and have a wonderful day.
        """
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(subject, message, from_email, [booking.email, settings.DEFAULT_FROM_EMAIL])
    except Exception:
        pass

def send_reschedule_email(old_booking, new_booking):
    subject = f"Appointment Rescheduled - {old_booking.reference}"
    message = f"""
        Hello {old_booking.name},
            Thank you for booking an appointment with Enhanced Beauty. Your appointment (ref. number {old_booking.reference}) on {old_booking.availability.date} at {old_booking.availability.start_time} for a {old_booking.service.name} has been rescheduled to {new_booking.availability.date} at {new_booking.availability.start_time} for a {new_booking.service.name} and your new ref. number is {new_booking.reference}. If you need to cancel or reschedule please visit the site. I look forward to serving you. Have a wonderful day.
        """
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(subject, message, from_email, [old_booking.email, settings.DEFAULT_FROM_EMAIL])
    except Exception:
        pass

def create_booking(availability_id, service_id, name, email, phone):
    slot = Availability.objects.get(id=availability_id)
    service = Service.objects.get(id=service_id)

    if Booking.objects.filter(availability=slot, status='confirmed').exists():
        return {"error": "This slot is already booked."}
    name = name.title()
    digits = ''.join(c for c in phone if c.isdigit())
    phone = f"{digits[:3]}-{digits[3:6]}-{digits[6:10]}"
    booking = Booking.objects.create(
        availability=slot, service=service, name=name, email=email, phone=phone
    )

    slot.booked = True
    slot.save()
    send_confirmation_email(booking)

    return {
        "reference": booking.reference,
        "name": booking.name,
        "date": str(booking.availability.date),
        "location": str(booking.availability.location),
        "time": str(booking.availability.start_time),
        "service": booking.service.name,
        "status": booking.status,
    }


def cancel_booking(reference):
    booking = Booking.objects.get(reference=reference)

    booking.status = "cancelled"
    booking.availability.booked = False
    booking.save()
    booking.availability.save()
    send_cancellation_email(booking)

    return {
        "reference": booking.reference,
        "name": booking.name,
        "date": str(booking.availability.date),
        "time": str(booking.availability.start_time),
        "service": booking.service.name,
        "status": booking.status,
    }


def get_booking(reference):
    booking = Booking.objects.get(reference=reference)

    return {
        "reference": booking.reference,
        "name": booking.name,
        "date": str(booking.availability.date),
        "time": str(booking.availability.start_time),
        "service": booking.service.name,
        "status": booking.status,
    }

def run_agent(messages):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        tools=TOOLS,
        messages=messages,
    )

    while response.stop_reason == "tool_use":
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                if block.name == "list_services":
                    result = list_services()
                elif block.name == "check_availability":
                    result = check_availability(
                        block.input.get("start_date"), block.input.get("end_date")
                    )
                elif block.name == "create_booking":
                    result = create_booking(
                        block.input.get("availability_id"),
                        block.input.get("service_id"),
                        block.input.get("name"),
                        block.input.get("email"),
                        block.input.get("phone"),
                    )
                elif block.name == "cancel_booking":
                    result = cancel_booking(block.input.get("reference"))
                elif block.name == "get_booking":
                    result = get_booking(block.input.get("reference"))
                else:
                    result = {"error": "Unknown tool"}

                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result)}
                )

        messages = messages + [
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": tool_results},
        ]

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

    for block in response.content:
        if hasattr(block, "text"):
            return block.text

    return "I'm sorry, I was unable to process your request. Please try again."
