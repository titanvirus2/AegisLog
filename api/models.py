from pydantic import BaseModel, constr

SEVERITY_CHOICES = {"Low", "Medium", "High", "Critical"}
STATUS_CHOICES = {"Open", "Fixed", "Accepted", "False Positive"}

class Vulnerability(BaseModel):
    id: int
    title: constr(strip_whitespace=True, min_length=1)
    severity: str = "Low"
    asset: constr(strip_whitespace=True, min_length=1)
    description: str = ""
    status: str = "Open"


