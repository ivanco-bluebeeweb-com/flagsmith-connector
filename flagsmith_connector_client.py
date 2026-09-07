"""HTTP client for Flagsmith API."""
from __future__ import annotations
import httpx
from typing import Any, Optional

DEFAULT_BASE = "https://edge.api.flagsmith.com/api/v1"

class FlagsmithClient:
    def __init__(self, environment_key: str, base_url: str = ""):
        self.environment_key = environment_key.strip()
        self.base_url = (base_url.strip() if base_url else DEFAULT_BASE).rstrip("/")
        self.headers = {
            "X-Environment-Key": self.environment_key,
            "Content-Type": "application/json",
            "User-Agent": "Imperal-Flagsmith-Connector/1.0.0"
        }
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def verify_auth(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/flags/", headers=self.headers)
                if resp.status_code in (200, 201, 204):
                    data = resp.json() if resp.content else []
                    return {"status": "ok", "data": data}
                return {"status": "error", "error": f"HTTP {resp.status_code}: {resp.text}"}
            except Exception as e:
                return {"status": "error", "error": str(e)}

    async def list_flags(self, limit: int = 20) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/flags/", headers=self.headers)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list):
                    return data[:limit]
                for k in ["data", "flags", "items", "results"]:
                    if k in data and isinstance(data[k], list):
                        return data[k][:limit]
                return []
            return []

    async def get_flag(self, flag_id: str) -> dict[str, Any]:
        flags = await self.list_flags(limit=100)
        for f in flags:
            feat = f.get("feature", {})
            feat_id = str(feat.get("id") or "")
            feat_name = str(feat.get("name") or "")
            if feat_id == flag_id or feat_name == flag_id:
                return f
        raise ValueError(f"Flag '{flag_id}' not found in environment.")
