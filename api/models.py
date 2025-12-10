from pydantic import BaseModel, constr
from typing import Optional

class Vulnerability(BaseModel):
    id: Optional[int] = None
    title: constr(strip_whitespace=True, min_length=1)
    severity: str = "Low"
    asset: constr(strip_whitespace=True, min_length=1)
    description: str = ""
    status: str = "Open"

class Asset(BaseModel):
    id: Optional[int] = None
    operating_system: constr(strip_whitespace=True, min_length=1)
    ip_address: str = ""
