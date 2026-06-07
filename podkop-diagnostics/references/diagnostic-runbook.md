# Диагностический протокол Podkop

## Содержание

- Система
- Клиент
- DNS
- sing-box
- nftables
- Outbound
- Наблюдаемость
- Результаты
- Источники

## Система

```sh
ubus call system board
cat /etc/openwrt_release
df -h /overlay
date
opkg list-installed 2>/dev/null | grep -E 'podkop|sing-box|luci-app-podkop'
service podkop status
sing-box version
/usr/bin/podkop global_check
```

Global check и install log сохранять как артефакты; проверять секреты. Не исправлять найденные отклонения в рамках этого runbook.

## Клиент

```sh
nslookup fakeip.podkop.fyi
curl -v https://fakeip.podkop.fyi/check
```

Ожидать DNS server = роутер, `198.18.x.x`, подключение к FakeIP, `"fakeip": true`.

Собрать IP, gateway, DNS, VPN, Secure DNS и сравнение с рабочим клиентом.

## DNS

```sh
netstat -tanp | grep LISTEN
uci show dhcp.@dnsmasq[0]
logread -e dnsmasq | tail -n 100
```

Ожидать `127.0.0.42:53`, `127.0.0.1:1602`, LAN `:53`, `noresolv='1'`, `server='127.0.0.42'`.

```sh
logread -f -e dnsmasq
```

## sing-box

В Diagnostics проверить: установлен, версия >= 1.12.4, init script есть, autostart отключен, процесс и порты активны.

```sh
logread | grep -E 'podkop|sing-box'
```

Искать JSON, rule-set, DNS, dial, TLS, Reality handshake и bind errors.

## nftables

```sh
nft list ruleset | grep -B3 mark
```

Нужны `mangle`, `mangle_output`, `proxy`. Counters для `198.18.0.0/15` растут при запросе.

- `mangle=0`: трафик не приходит.
- `mangle` растет, `proxy` отстает: конфликт mark/sing-box.
- Другие mark rules: GetDomains, GL.iNet vpn-client, старые scripts.

## Outbound

### VPN

```sh
curl -v --interface wg0 ifconfig.me
```

### VLESS/Reality

Разделить DNS имени сервера, reachability порта, TLS/Reality handshake, VLESS auth/flow и routing rule. Зафиксировать, на каком этапе возникает первая ошибка; не менять ссылку или outbound.

## Наблюдаемость

- Dashboard: process, memory, connections, traffic, URLTest.
- YACD `Conns`: соединение и правило.
- YACD `Proxies`: selector и latency.
- Diagnostics: DNS, sing-box, nftables, outbounds, FakeIP.

## Результаты

| Наблюдение | Слой |
|---|---|
| публичный IP вместо FakeIP | client DNS/DoH |
| FakeIP без соединения | gateway/nftables |
| нет `.42:53` | sing-box config/start |
| нет `.1:1602` | tproxy inbound |
| все green, сайт не туда | lists overlap |
| outbound timeout | proxy/VPN |
| browser check red | browser DoH |
| ломается после WAN reconnect | interface monitoring |

## Формат отчета

```text
Контекст: LAN/remote, OpenWrt, Podkop, sing-box
Симптом: точное наблюдаемое поведение
Рабочая контрольная точка: последний успешный этап цепочки
Первый сбой: первый неуспешный этап
Доказательства: команды и ключевые строки вывода
Секреты удалены: да/нет
Следующая ветка: имя раздела podkop-troubleshooting
```

## Источники

Podkop Wiki, коммит `34872e963af4c99116665a202ea83616fd6017ad`:

- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/diagnostics
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/troubleshooting
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/dashboard
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/yacd
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/dnsmasqlogs
