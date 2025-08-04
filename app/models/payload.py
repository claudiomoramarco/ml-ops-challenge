#"è il contratto per l api"
from pydantic import BaseModel
from typing import List

class IrisPayload(BaseModel):
    features: List[List[float]]
    # {"features": [[5.1, 3.5, 1.4, 0.2]]} 