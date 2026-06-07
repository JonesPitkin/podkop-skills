# Руководство по DNS Podkop

## Содержание

- Базовая настройка
- Клиентский DNS
- Dont Touch My DHCP
- Domain Resolver
- AdGuard Home
- Типовые сценарии
- Контроль конфигурации
- Источники

## Базовая настройка

Выбрать DoH, DoT или UDP. Если адрес DoH/DoT задан доменным именем, настроить bootstrap UDP DNS. TTL FakeIP около минуты уменьшает последствия перезагрузки при RAM cache.

Минимум:

```text
option noresolv '1'
option cachesize '0'
list server '127.0.0.42'
```

## Клиентский DNS

Если терминал работает, а браузер нет, отключить Secure DNS/DoH. На Android проверить Private DNS. На Windows использовать DHCP DNS и убедиться, что IPv4 DNS равен роутеру.

Для hardcoded DNS можно перехватить TCP/UDP 53:

```text
config redirect
    option name 'Intercept DNS LAN'
    option src 'lan'
    option proto 'tcp udp'
    option src_dport '53'
    option dest_port '53'
    option target 'DNAT'
```

```sh
service firewall restart
```

Это не перехватывает DoH. DoT 853 требует отдельной политики.

## Dont Touch My DHCP

Включать только для ручного управления:

```text
option noresolv '1'
option cachesize '0'
list server '127.0.0.42'
```

Selective forward:

```text
list server '/itdog.info/1.1.1.1'
list server '127.0.0.42'
```

## Domain Resolver

Доступен для VPN sections с WG/AWG/OpenVPN/OpenConnect. Выбранный DNS повторно разрешает домены из списков и по умолчанию идет через тот же туннель.

Для Proxy/VLESS/Reality преобразование FakeIP выполняет удаленный прокси; не обещать отдельный DNS per Proxy section.

## AdGuard Home

### AGH как upstream Podkop

На роутере дать AGH отдельный loopback, например `127.0.0.10:53`; не использовать `.42` или `.53`. В Podkop выбрать UDP и `127.0.0.10`.

На отдельном хосте указать LAN IP AGH.

### AGH перед Podkop

Клиенты получают AGH по DHCP; AGH использует роутер с Podkop как upstream. Не направлять upstream AGH обратно на самого себя.

## Типовые сценарии

### Подготовить DNS для Android и телевизоров

Раздавать DNS роутера по DHCP, отключить Android Private DNS. Для устройств с hardcoded DNS применить interception TCP/UDP 53 и отдельную политику DoT/DoH.

### Подготовить браузеры

Отключить browser Secure DNS, чтобы запросы доменов из списков доходили до FakeIP resolver Podkop.

### Иностранный DoH нестабилен

Выбрать надежный UDP DNS. Для VPN sections использовать Domain Resolver.

### Корпоративный VPN

Клиент может заменить DNS и gateway. Использовать split DNS, Mixed Proxy либо перенести VPN на OpenWrt.

### Подготовить DNS для VLESS + Reality

Обеспечить разрешение имени proxy server через основной upstream/bootstrap. DNS имени прокси и FakeIP целевого сайта являются разными потоками.

## Контроль конфигурации

После настройки передать проверку в `podkop-diagnostics`. Ожидаемые инварианты:

| Область | Инвариант |
|---|---|---|
| dnsmasq | `noresolv='1'`, общий upstream `127.0.0.42` |
| sing-box DNS | слушает `127.0.0.42:53` |
| клиент | получает DNS роутера или AGH, ведущий в Podkop |
| FakeIP | домены из списков получают `198.18.0.0/15` |
| AGH | нет self-upstream и конфликтов `.42`/`.53` |
| VPN section | Domain Resolver настроен только там, где нужен |

## Источники

Podkop Wiki, коммит `34872e963af4c99116665a202ea83616fd6017ad`:

- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/dns
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/client-dns
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/dont-touch-my-dhcp
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/adguard
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/dnsmasqlogs
