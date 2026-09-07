"""Connection management for Flagsmith Connector."""
from __future__ import annotations
import uuid
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import NoParams, ConnectParams, ConnectionIdParams, ConnectionRecord, ConnectionList, DeleteResult
from flagsmith_connector_client import FlagsmithClient

def _mask(v: str) -> str:
    if len(v) > 8:
        return v[:4] + "*" * (len(v) - 8) + v[-4:]
    return "***"

async def get_connections_list(ctx) -> list[dict]:
    page = await ctx.store.query("connections")
    docs = page.data if hasattr(page, "data") else []
    conns = []
    for d in docs:
        data = d.data if hasattr(d, "data") else d
        doc_id = d.id if hasattr(d, "id") else data.get("id")
        data["_store_id"] = doc_id
        conns.append(data)
    return conns

async def resolve_client(ctx, connection_id: str = "") -> FlagsmithClient:
    conns = await get_connections_list(ctx)
    if not conns:
        raise ValueError("No Flagsmith connections configured. Use connect_flagsmith_connector first.")
    conn = None
    if connection_id:
        for c in conns:
            if c.get("id") == connection_id:
                conn = c
                break
        if not conn:
            raise ValueError(f"Connection {connection_id} not found.")
    else:
        conn = conns[0]
    return FlagsmithClient(environment_key=conn["environment_key"], base_url=conn.get("base_url", ""))

@chat.function("connect_flagsmith_connector", "Connect Flagsmith account via credentials.", action_type="write", chain_callable=True, event="flagsmith-connector.connect_flagsmith_connector", effects=["create:connection"], data_model=ConnectionRecord)
async def connect_flagsmith_connector(params: ConnectParams, ctx) -> ActionResult:
    client = FlagsmithClient(environment_key=params.environment_key, base_url=params.base_url)
    res = await client.verify_auth()
    if res.get("status") == "error":
        return ActionResult.error(f"Failed to connect to Flagsmith: {res.get('error')}")

    cid = f"conn_{uuid.uuid4().hex[:8]}"
    rec = {
        "id": cid,
        "label": params.label or "Primary Flagsmith",
        "environment_key": params.environment_key,
        "masked_key": _mask(params.environment_key),
        "base_url": params.base_url,
        "is_active": True
    }
    await ctx.store.create("connections", rec)
    return ActionResult.success(ConnectionRecord(**rec), summary=f"Connected Flagsmith ({rec['label']}).")

@chat.function("list_connections", "List configured Flagsmith connections.", action_type="read", chain_callable=True, event="flagsmith-connector.list_connections", effects=["read:connections"], data_model=ConnectionList)
async def list_connections(params: NoParams, ctx) -> ActionResult:
    conns = await get_connections_list(ctx)
    items = [ConnectionRecord(
        id=c["id"],
        label=c["label"],
        masked_key=c.get("masked_key", "***"),
        base_url=c.get("base_url", "https://edge.api.flagsmith.com/api/v1"),
        is_active=c.get("is_active", False)
    ) for c in conns]
    return ActionResult.success(ConnectionList(connections=items, total=len(items)), summary=f"Found {len(items)} connection(s).")

@chat.function("disconnect_flagsmith_connector", "Disconnect Flagsmith account and delete stored credentials.", action_type="destructive", chain_callable=True, event="flagsmith-connector.disconnect_flagsmith_connector", effects=["delete:connection"], data_model=DeleteResult)
async def disconnect_flagsmith_connector(params: ConnectionIdParams, ctx) -> ActionResult:
    conns = await get_connections_list(ctx)
    if not conns:
        return ActionResult.error("No connections to disconnect.")
    deleted = 0
    for c in conns:
        if not params.connection_id or c.get("id") == params.connection_id:
            store_id = c.get("_store_id") or c.get("id")
            await ctx.store.delete("connections", store_id)
            deleted += 1
    return ActionResult.success(DeleteResult(success=deleted > 0, message=f"Disconnected {deleted} connection(s)."), summary="Disconnected Flagsmith connection.")
