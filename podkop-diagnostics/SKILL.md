---
name: podkop-diagnostics
description: "Собирать, интерпретировать и безопасно представлять диагностику Podkop на OpenWrt: LuCI Diagnostics, global_check, версии, DNS, dnsmasq, sing-box, FakeIP, nftables/tproxy counters, outbounds, VPN-интерфейсы, Dashboard, YACD и логи. Использовать для read-only обследования, проверки после установки или изменения, подготовки отчета и локализации первого сломанного слоя. Не изменять конфигурацию; передавать подтвержденную причину в podkop-troubleshooting."
---

# Podkop Diagnostics

Диагностика собирает доказательства; исправления выполнять после локализации слоя:

```text
клиент DNS/gateway -> dnsmasq -> sing-box DNS/FakeIP -> nftables/tproxy -> outbound -> интернет
```

## Быстрый протокол

1. Уточнить, выполняется ли тест из LAN. Browser Diagnostics недостоверна при удаленном доступе к LuCI.
2. Зафиксировать систему и версии.
3. Запустить LuCI Diagnostics и читать блоки сверху вниз.
4. Получить:
   ```sh
   /usr/bin/podkop global_check
   ```
5. Проверить клиента:
   ```sh
   nslookup fakeip.podkop.fyi
   curl -v https://fakeip.podkop.fyi/check
   ```
6. Проверить порты, dnsmasq и nftables.
7. Проверить outbound отдельно:
   - VPN: `curl --interface`.
   - VLESS/Reality: checks, логи, тестовая ссылка.
8. Сформулировать первый сломанный этап.

## Сбор данных

Использовать [references/diagnostic-runbook.md](references/diagnostic-runbook.md). Скрывать VLESS URL, UUID, токены, Reality keys, пароли и лишние публичные IP.

## Результат диагностики

- Нет FakeIP: DNS.
- FakeIP есть, `curl` зависает: gateway/nftables/tproxy.
- Counters растут, outbound падает: прокси/VPN.
- Работает на других клиентах: локальный DNS/VPN/gateway.
- Терминал работает, браузер нет: Secure DNS.

Выдать краткий отчет:

```text
Симптом:
Первый сломанный слой:
Подтверждающие наблюдения:
Не проверено:
Рекомендуемая ветка podkop-troubleshooting:
```

## Граница

Не менять UCI, службы, packages, nftables, DNS клиентов или outbounds. Исправления передавать `podkop-troubleshooting`.
