# podkop-skills

Comprehensive AI Skill Repository for `Podkop`.

Official-source-oriented skill collection for `Podkop` on OpenWrt: installation, DNS and FakeIP, routing, diagnostics, and minimal-change troubleshooting.

## Skill Tree

- [`podkop`](podkop/SKILL.md)
- [`podkop-install`](podkop-install/SKILL.md)
- [`podkop-dns`](podkop-dns/SKILL.md)
- [`podkop-routing`](podkop-routing/SKILL.md)
- [`podkop-diagnostics`](podkop-diagnostics/SKILL.md)
- [`podkop-troubleshooting`](podkop-troubleshooting/SKILL.md)

## Dependency Map

- `podkop` is the repository entrypoint for request classification.
- `podkop-install` owns package lifecycle and platform fit.
- `podkop-dns` owns dnsmasq, sing-box DNS, FakeIP, and client DNS behavior.
- `podkop-routing` owns proxy/VPN sections, outbounds, selectors, and traffic policy.
- `podkop-diagnostics` is read-only and identifies the first broken layer.
- `podkop-troubleshooting` applies the smallest safe fix after confirmed diagnosis.

## Quick Start

1. Start with [`podkop/SKILL.md`](podkop/SKILL.md) for broad tasks.
2. Use `podkop-install` before changing packages or OpenWrt integration.
3. Use `podkop-diagnostics` before making assumptions about a broken router.
4. Use `podkop-troubleshooting` only after the failing layer is proven.

## Repository Structure

```text
podkop-skills/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SKILL_INDEX.md
├── VERSION_MATRIX.md
├── MIGRATION_GUIDE.md
├── GITHUB_REPOSITORY.md
├── RELEASE_v1.0.0.md
├── podkop/
├── podkop-install/
├── podkop-dns/
├── podkop-routing/
├── podkop-diagnostics/
└── podkop-troubleshooting/
```

## Official Sources

- official `Podkop` repository
- official `Podkop` wiki
- official OpenWrt package and platform documentation

See [`podkop/references/official-links.md`](podkop/references/official-links.md).

## Version Policy

Treat `Podkop`, `sing-box`, `dnsmasq`, OpenWrt package flows, and LuCI behavior as changeable across releases. Validate current upstream state before production mutations.

## License

Released under the MIT License. See [`LICENSE`](LICENSE).

## Contribution Guide

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Changelog

Repository-level release notes are tracked in [`CHANGELOG.md`](CHANGELOG.md).
