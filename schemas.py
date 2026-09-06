"""Pydantic schemas for Flagsmith Connector."""
from __future__ import annotations
from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field

class NoParams(BaseModel):
    """Empty parameters model."""
    pass

class ConnectParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Primary Flagsmith.")
    environment_key: str = Field(description="Flagsmith Server-side Environment Key.")
    base_url: str = Field(default="https://edge.api.flagsmith.com/api/v1", description="Flagsmith API base URL.")

class ConnectionIdParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier (empty uses active connection).")

class ConnectionRecord(BaseModel):
    id: str
    label: str
    masked_key: str
    base_url: str
    is_active: bool

class ConnectionList(BaseModel):
    connections: list[ConnectionRecord]
    total: int

class DeleteResult(BaseModel):
    success: bool
    message: str

class FlagRecord(BaseModel):
    id: str
    name: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    raw: Dict[str, Any] = Field(default_factory=dict)

class FlagList(BaseModel):
    flags: list[FlagRecord]
    total: int

class ListFlagParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    limit: int = Field(default=20, ge=1, le=100, description="Max records to return.")

class GetFlagParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    flag_id: str = Field(description="Flagsmith Flag ID.")

class AuditHealthReport(BaseModel):
    healthy: bool
    total_flags: int
    details: Dict[str, Any] = Field(default_factory=dict)
    summary: str
