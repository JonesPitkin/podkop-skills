# Podkop Skills

Набор Skills для установки, настройки и сопровождения Podkop на OpenWrt.

Материалы основаны на [Podkop Wiki](https://github.com/itdoginfo/podkop-wiki) на коммите `34872e963af4c99116665a202ea83616fd6017ad` от 29 мая 2026 года.

## Навыки

| Skill | Назначение |
|---|---|
| `podkop-install` | Установка, обновление, удаление и восстановление Podkop |
| `podkop-dns` | Проектирование и настройка DNS, FakeIP, dnsmasq и AdGuard Home |
| `podkop-routing` | Секции, списки, VLESS/Reality, URLTest и VPN-маршрутизация |
| `podkop-diagnostics` | Read-only сбор фактов и локализация первого сломанного слоя |
| `podkop-troubleshooting` | Минимальные исправления после подтвержденной диагностики |

## Разделение ответственности

Три смежных навыка намеренно не дублируют друг друга:

1. `podkop-dns` создает или изменяет DNS-конфигурацию.
2. `podkop-diagnostics` только собирает данные и формирует отчет.
3. `podkop-troubleshooting` применяет исправление к уже подтвержденной причине.

## Структура

Каждый каталог навыка содержит:

- `SKILL.md` с trigger description и основным workflow;
- `agents/openai.yaml` с UI-метаданными;
- `references/` с подробными процедурами и сценариями.

## Установка

Скопировать нужные каталоги в директорию Skills Codex:

```sh
cp -R podkop-* "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Навыки можно устанавливать независимо, но полный набор обеспечивает переходы между настройкой, диагностикой и исправлением.

## Проверка

```sh
python3 -m pip install pyyaml
python3 scripts/validate_skills.py
```

GitHub Actions выполняет ту же проверку для pull request и push.

## Безопасность

Не публикуйте VLESS URL, UUID, пароли, токены, Reality keys, short ID и конфигурации с секретами. Примеры используют только фиктивные или скрытые значения.

