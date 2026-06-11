---
name: podkop
description: Route Podkop requests to the correct skill for installation, DNS, routing, diagnostics, or troubleshooting.
---

# Podkop Repository Router

Use this skill when the task mentions `Podkop` broadly and the owning specialist skill is not yet clear.

## Routing Rules

- Use `podkop-install` for installation, update, removal, and restore.
- Use `podkop-dns` for DNS, FakeIP, dnsmasq, bootstrap DNS, and client DNS behavior.
- Use `podkop-routing` for sections, selectors, outbounds, VPN tunnels, and traffic policy.
- Use `podkop-diagnostics` for read-only data collection and first-broken-layer analysis.
- Use `podkop-troubleshooting` only after a diagnostic path confirms the failing layer.
