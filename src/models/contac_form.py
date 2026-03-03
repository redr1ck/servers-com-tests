from dataclasses import dataclass
from typing import Optional

@dataclass
class ContactFormData:
    """Contact data structure for form filling."""
    # Text fields
    first_name: str
    last_name: Optional[str] = None
    email: str = ""
    secondary_email: Optional[str] = None
    phone: str = ""
    company: Optional[str] = None
    job_title: Optional[str] = None
    comment: Optional[str] = None
    
    # Checkbox states
    is_primary: bool = False
    is_emergency: bool = False
    is_billing: Optional[bool] = None
    is_technical: Optional[bool] = None
    is_abuse: Optional[bool] = None
