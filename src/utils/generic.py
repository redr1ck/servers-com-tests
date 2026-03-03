from faker import Faker

from src.models.contact_contact_payload import Contact, ContactTokens
from src.models.contac_form import ContactFormData

fake = Faker()

def phone_9_15_digits():
    n = fake.random_int(min=9, max=15)
    # первая цифра не 0, остальные любые
    first = str(fake.random_int(min=1, max=9))
    rest = ''.join(str(fake.random_int(0, 9)) for _ in range(n - 1))
    return first + rest

def generate_contact_request_data() -> Contact:
    """Generate unique contact data for test using faker."""
    return Contact(
        fname=fake.first_name(),
        lname=fake.last_name(),
        email=fake.email(),
        email2=fake.email(),
        phone_number=phone_9_15_digits(),
        role=142,
        tokens=ContactTokens(
            title=fake.catch_phrase(),
            note=fake.text(max_nb_chars=1000)
        )
    )

def generate_contact_form_data() -> ContactFormData:
    """Generate unique contact form data for test using faker."""
    return ContactFormData(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        secondary_email=fake.email(),
        phone=phone_9_15_digits(),
        company=fake.company(),
        job_title=fake.job(),
        comment=fake.sentence(),
        is_primary=True,
        is_emergency=True,
        is_billing=True,
        is_technical=True,
        is_abuse=True,
    )
# Technical, Billing, Emergency, Abuse - role ID 142 (all roles)

