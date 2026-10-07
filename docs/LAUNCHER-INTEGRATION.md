# Integration contract with MOO2-SGC Launcher

This note preserves the separation established in the launcher requirements addendum and updated v0.4.7 guidance. **No integration has been implemented in this handoff.**

## Present boundary

- Launcher owns game discovery/import, selection, patch setup, sandboxed runtime at `C:\Games\MOO2-SGC`, profile/version management, networking commands, diagnostics, update and rollback.
- PRSL owns readiness policy, coordinator, optional game adapter and in-turn UI, distributed only as its own independently versioned package.
- New Chat is another optional independent extension; any UI tab in the launcher is NOT automatically an in-game PRSL hook.
- SCG Quickplay and Tournament gameplay mod projects are separate. PRSL should not require their rulesets.

## Integration gates

The launcher must never assume that a signed PRSL package is compatible with an arbitrary fan-patch engine; require a **certified exact-hash adapter + protocol version + platform/guest runtime tuple**. At first, PRSL cannot be selected for play (v0.4.7 lists it research-only). The game version 1.40b23 baseline is a separate environment and must not be mistaken for the tested 1.50.26 engine.

Modes for subsequent certification:

| Selection | PRSL | Chat | Expected behavior |
|---|---|---|---|
| Standard Community | Off | Off | Native game, no PRSL packets/hooks |
| PRSL only | On | Off | Ready barrier + essential status, only when certified |
| Chat only | Off | On | Messaging, no modification to native End Turn |
| Both | On | On | Optional status integration with distinct modules |

No PRSL/Chat source should be fused into the bootstrapper. The launcher should preserve requested vs resolved profiles and lockfiles, mod conflict checks, stable author/provenance, and explicit active/inactive state. A future shared hook dispatcher must have exclusive validated ownership of each patched instruction boundary.

## Networking

Launcher v0.4.7's Community network plan includes `ORION150.EXE`, `IPXNET CONNECT moo2.thedopefish.com 213` for Dopefish public IPX. That config command is not a PRSL coordinator endpoint; PRSL would require its own authenticated control transport. Live Dopefish/IPX acceptance was explicitly pending in the launcher report as of Oct 7.

## Proposed adapter manifest contract (NOT implemented)

```json
{
  "schema": 1,
  "id": "moo2-sgc.prsl",
  "version": "UNRELEASED",
  "status": "research-only",
  "installable": false,
  "engine_sha256": "2db296e052419250d21866f7c23ac2978a33b3c05b451a9516f06599b91c3f5c",
  "adapter_certified": false,
  "multiplayer_certified": false
}
```

This is **illustrative documentation**, never feed it directly into an installer, loader or signing pipeline. Never turn `installable` true merely to expose a checkbox. Production schema/version choice belongs to the launcher and future PRSL package contracts.
