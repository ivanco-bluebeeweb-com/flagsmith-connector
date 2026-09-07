"""Resource handlers for Flagsmith Connector."""
from __future__ import annotations
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ListFlagParams, GetFlagParams,
    FlagRecord, FlagList, AuditHealthReport, ConnectionIdParams
)
from handlers_connection import resolve_client

@chat.function("list_flags", "List flags in Flagsmith.", action_type="read", chain_callable=True, event="flagsmith-connector.list_flags", effects=["read:flags"], data_model=FlagList)
async def list_flags(ctx, params: ListFlagParams) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        raw_items = await client.list_flags(limit=params.limit)
        items = []
        for r in raw_items:
            feat = r.get("feature", {})
            rid = str(feat.get("id") or r.get("id") or "unknown")
            rname = feat.get("name") or r.get("name") or rid
            enabled = r.get("enabled", False)
            status = "enabled" if enabled else "disabled"
            items.append(FlagRecord(id=rid, name=rname, status=status, created_at=None, raw=r))
        return ActionResult.success(FlagList(flags=items, total=len(items)), summary=f"Found {len(items)} flags.")
    except Exception as e:
        return ActionResult.error(f"Error listing flags: {e}")

@chat.function("get_flag", "Get details of one Flag in Flagsmith.", action_type="read", chain_callable=True, event="flagsmith-connector.get_flag", effects=["read:flag"], data_model=FlagRecord)
async def get_flag(ctx, params: GetFlagParams) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        r = await client.get_flag(params.flag_id)
        feat = r.get("feature", {})
        rid = str(feat.get("id") or r.get("id") or params.flag_id)
        rname = feat.get("name") or r.get("name") or rid
        status = "enabled" if r.get("enabled", False) else "disabled"
        return ActionResult.success(FlagRecord(id=rid, name=rname, status=status, created_at=None, raw=r), summary=f"Retrieved Flag {rname} ({rid}).")
    except Exception as e:
        return ActionResult.error(f"Error retrieving Flag: {e}")

@chat.function("audit_flag_health", "Audit health of Flagsmith flags and connectivity.", action_type="read", chain_callable=True, event="flagsmith-connector.audit_flag_health", effects=["read:audit"], data_model=AuditHealthReport)
async def audit_flag_health(ctx, params: ConnectionIdParams) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_flags(limit=50)
        return ActionResult.success(AuditHealthReport(
            healthy=True,
            total_flags=len(items),
            details={"sample_count": len(items)},
            summary=f"Flagsmith healthy. Sampled {len(items)} flags."
        ), summary=f"Flagsmith health check passed with {len(items)} flags.")
    except Exception as e:
        return ActionResult.error(f"Error auditing Flagsmith health: {e}")
