"""Panel UI for Flagsmith Connector following UI_INTERFACE_STANDARD.md and AUTH_AND_CREDENTIALS_STANDARD.md."""
from __future__ import annotations
from imperal_sdk import ui
from app import ext

def _settings_button() -> ui.UINode:
    return ui.Button(
        "App settings",
        variant="secondary",
        size="sm",
        icon="settings",
        on_click=ui.Call("__panel__flagsmith_settings")
    )

def _help_modal() -> ui.UINode:
    return ui.Modal(
        trigger=ui.Button("How do I set this up?", variant="ghost", size="sm"),
        title="Connecting Flagsmith",
        children=[
            ui.Text(
                "1. Sign in to your Flagsmith account and navigate to API Keys or Integrations settings.\n2. Generate a secure API Key or Access Token (provider API does not offer direct OAuth SSO).\n3. Paste the key below and click Connect.",
                variant="body"
            )
        ]
    )

@ext.panel("flagsmith_sidebar", slot="left")
async def flagsmith_sidebar(ctx, **kwargs) -> ui.UINode:
    return ui.Stack(
        direction="v",
        gap=3,
        align="stretch",
        children=[
            ui.Text("Flagsmith", variant="heading"),
            ui.Stack(
                direction="v",
                gap=1,
                align="stretch",
                children=[
                    ui.Text("Manage your Flagsmith connections and integrations.", variant="caption"),
                ]
            ),
            ui.Divider(),
            ui.Stack(
                direction="v",
                gap=2,
                align="stretch",
                children=[
                    ui.Text("Connect via API Key / Access Token", variant="caption"),
                    ui.Form(
                        submit_label="Connect Flagsmith",
                        action=ui.Call("connect_flagsmith"),
                        children=[
                            ui.Stack(
                                direction="v",
                                gap=2,
                                align="stretch",
                                children=[
                                    ui.Stack(
                                        direction="v",
                                        gap=1,
                                        align="stretch",
                                        children=[
                                            ui.Text("Connection Label", variant="label"),
                                            ui.Input(param_name="label", placeholder="e.g. Production Flagsmith"),
                                        ]
                                    ),
                                    ui.Stack(
                                        direction="v",
                                        gap=1,
                                        align="stretch",
                                        children=[
                                            ui.Text("API Key / Access Token", variant="label"),
                                            ui.Input(param_name="api_key", placeholder="Paste API Key or Access Token"),
                                        ]
                                    ),
                                ]
                            )
                        ]
                    ),
                ]
            ),
            _help_modal(),
            ui.Spacer(),
            _settings_button(),
        ]
    )
