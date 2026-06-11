# Migration Guide

## From `nidox-vpn-skills/skills/podkop`

The legacy `skills/podkop/` directory in `nidox-vpn-skills` is a compatibility marker. The standalone source of truth is this repository.

## Recommended Migration

1. maintain the authoritative content in this repository
2. sync a full snapshot into `nidox-vpn-skills/podkop-skills/`
3. keep the legacy thin entrypoint until downstream tooling is migrated
