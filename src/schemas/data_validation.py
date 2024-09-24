from pydantic import BaseModel
from typing import Optional

class SelectionData(BaseModel):
    selected_column: str
    selected_fmn: Optional[str] = None
    selected_branch: Optional[str] = None
    selected_sub_branch: Optional[str] = None
