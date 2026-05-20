import httpx
import logging
from typing import List, Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class BodogwuClient:
    BASE_URL = "https://bodogwu.customs.gov.ng/back/api/SgdDocument"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    async def get_models(self, page: int = 1, page_size: int = 50) -> List[Dict[str, Any]]:
        """Fetch list of SGD document summaries."""
        url = f"{self.BASE_URL}/GetModels"
        params = {"page": page, "pageSize": page_size}
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching models from Bodogwu: {e}")
            return []

    async def get_model(self, sgd_id: str) -> Optional[Dict[str, Any]]:
        """Fetch full details of a specific SGD document."""
        url = f"{self.BASE_URL}/GetModel"
        params = {"sgdId": sgd_id}
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching model {sgd_id} from Bodogwu: {e}")
            return None
