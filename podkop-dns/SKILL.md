---
name: podkop-dns
description: "Проектировать и настраивать DNS в Podkop: dnsmasq, sing-box на 127.0.0.42:53, FakeIP 198.18.0.0/15, DoH/DoT/UDP, bootstrap DNS, Domain Resolver, клиентский Secure DNS/Private DNS, перехват DNS и интеграцию с AdGuard Home. Использовать при выборе DNS-схемы, изменении конфигурации, split DNS, Dont Touch My DHCP, DNS-утечках и настройке DNS для VLESS, Reality или VPN-секций. Для сбора доказательств использовать podkop-diagnostics, для исправления подтвержденных сбоев — podkop-troubleshooting."
---

# Podkop DNS

Рассматривать DNS как обязательную часть маршрутизации.

## Модель

```text
клиент -> dnsmasq на роутере:53 -> sing-box 127.0.0.42:53 -> upstream DNS
```

Для доменов из списков клиент получает FakeIP из `198.18.0.0/15`; трафик к нему перехватывается nftables/tproxy и передается sing-box.

## Рабочий процесс

1. Выбрать топологию: Podkop как основной DNS, AdGuard Home до/после Podkop либо ручной dnsmasq.
2. Выбрать upstream protocol и server. Для hostname DoH/DoT задать bootstrap UDP DNS.
3. Сохранить стандартную цепочку `dnsmasq -> 127.0.0.42:53`, если нет осознанной альтернативы.
4. Настроить клиентов на DNS роутера; для hardcoded DNS при необходимости добавить interception.
5. Для VPN section при необходимости включить Domain Resolver.
6. Для VLESS/Reality учитывать, что преобразование FakeIP выполняет прокси; отдельный DNS через Domain Resolver для Proxy section не выбирается.
7. Применить [references/dns-guide.md](references/dns-guide.md).
8. Перед завершением вызвать `podkop-diagnostics` для проверки результата.

## Ограничения

- Не включать `Dont Touch My DHCP` без ручной настройки dnsmasq.
- Не использовать `127.0.0.42` или `127.0.0.53` для AdGuard Home.
- Клиент должен использовать DNS-цепочку Podkop для FakeIP.
- Не превращать этот навык в общий runbook диагностики: проверки портов, counters и логов выполняет `podkop-diagnostics`.
- Не отключать IPv6 глобально без подтвержденного обхода через IPv6.

## Подробности

Открыть [references/dns-guide.md](references/dns-guide.md) для DoH/DoT/UDP, Domain Resolver, AdGuard Home, DNS interception, клиентских ОС и матрицы ошибок.
