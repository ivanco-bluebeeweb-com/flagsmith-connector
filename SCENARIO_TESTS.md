# Flagsmith Connector Scenario Tests

## Target & Authentication
- Vendor: Flagsmith
- Category: Feature Flagging & Remote Configuration
- Auth Method: Server-side Environment Key (`ser.*`)
- Target Environment: Live Production / Edge API (`https://edge.api.flagsmith.com/api/v1`)
- Tested User: `vlad@bluebeeweb.com` (Google Chrome Profile 2)

## Automated Live Verification Summary
1. **Account Creation & Environment Provisioning**:
   - Automated via Google Chrome (`Profile 2`) under `vlad@bluebeeweb.com`.
   - Created Organisation `Bluebeeweb` and Project `My first project`.
   - Generated Server-side Environment Key (`Imperal OS Server Key`).
2. **Step 1: Connect (`connect_flagsmith_connector`)**:
   - Authenticated against live Flagsmith Edge API `GET /api/v1/flags/`.
   - Credential saved in Document store, masked with standard asterisks format (`ser.******************U6PN`).
3. **Step 2: List Connections (`list_connections`)**:
   - Verified active connection enumeration with secret protection.
4. **Step 3: List Flags (`list_flags`)**:
   - Queried live feature flags (`show_demo_button`, ID: `254162`).
5. **Step 4: Get Flag (`get_flag`)**:
   - Retrieved exact feature record by ID with status.
6. **Step 5: Audit Health (`audit_flag_health`)**:
   - Verified automated connectivity and feature count telemetry.
7. **Step 6: Disconnect (`disconnect_flagsmith_connector`)**:
   - Clean teardown from storage verified.
