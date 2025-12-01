from pydantic import BaseModel, constr, validator
from typing import Optional

SEVERITY_CHOICES = {"Low", "Medium", "High", "Critical"}
STATUS_CHOICES = {"Open", "Fixed", "Accepted", "False Positive"}

class Vulnerability(BaseModel):
    id: Optional[int] = None
    title: constr(strip_whitespace=True, min_length=1)
    severity: str = "Low"
    asset: constr(strip_whitespace=True, min_length=1)
    description: str = ""
    status: str = "Open"


