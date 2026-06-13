# Руководство по маршрутизации Podkop

## Содержание

- Секции
- Proxy, VLESS и Reality
- VPN и DNS
- Списки и устройства
- Проверка
- Сценарии
- Ошибки
- Источники

## Секции

Имена: латиница, цифры, `_`. Каждая секция связывает домены/IP/источники с действием.

```text
config section 'main'
    option connection_type 'proxy'
    option proxy_config_type 'urltest'
    list community_lists 'geoblock'

config section 'wg'
    option connection_type 'vpn'
    option interface 'wg0'
    list community_lists 'youtube'
```

## Proxy, VLESS и Reality

Для одной ссылки выбрать Connection URL. Для нескольких:

- Selector: вручную.
- URLTest: автоматический выбор.
- Dashboard/YACD: временное закрепление. При RAM cache после reboot вернется автоматический режим.

```json
{
  "type": "vless",
  "server": "files.example.com",
  "server_port": 443,
  "uuid": "REDACTED-UUID",
  "flow": "xtls-rprx-vision",
  "tls": {
    "enabled": true,
    "server_name": "cover.example.com",
    "utls": {"enabled": true, "fingerprint": "chrome"},
    "reality": {
      "enabled": true,
      "public_key": "REDACTED-PUBLIC-KEY",
      "short_id": "REDACTED-SHORT-ID"
    }
  }
}
```

Проверить DNS server, порт, UUID/flow, SNI, public key, short ID и совместимость полей с sing-box. При плохом импорте экспортировать только outbound из клиента на базе sing-box.

## VPN и Domain Resolver

Сначала проверить интерфейс:

```sh
curl -v --interface wg0 ifconfig.me
```

Выбрать `Connection Type: VPN`. Для split routing:

- WG/AWG: `Route Allowed IPs` выключен при `0.0.0.0/0`.
- OpenVPN: при необходимости `pull-filter ignore redirect-gateway`.

Domain Resolver отправляет DNS этой секции через туннель.

## Списки и устройства

Поддерживаются community, user, local и remote lists, а также Fully Routed IPs.

```text
example.com
sub.example.com
103.21.244.0/22
103.21.244.89
```

```sh
sing-box rule-set compile --output rules.srs rules.json
```

Для Fully Routed IP назначить static lease. Глобальная отправка всей LAN не является основным назначением Podkop.

## Проверка

1. FakeIP работает.
2. Dashboard показывает outbound.
3. YACD `Conns` показывает правило.
4. nftables counters растут.
5. URLTest latency test успешен.
6. Проверен реальный сервис, не только главная страница.

## Сценарии

### Geoblock через VLESS/Reality

Proxy section, URL/outbound, список Geoblock, проверка FakeIP и YACD.

### Несколько VLESS

URLTest, несколько ссылок, check interval/tolerance/testing URL, режим Fastest, тест отказа.

### YouTube через WG, остальное через VLESS

Отдельная VPN section YouTube с Domain Resolver; Proxy section без списка, поглощающего YouTube.

### Исключить домен

Создать Exclusion и добавить домен; проверить YACD.

### Корпоративный VPN

Поднять interface без default route, VPN section для корпоративных доменов, split DNS. Альтернатива: Mixed Proxy.

### Гостевая сеть

Для включения добавить bridge в Source Network Interface и разрешить инфраструктурный/DNS access. Для исключения не добавлять bridge.

## Ошибки

| Симптом | Причина | Исправление |
|---|---|---|
| весь интернет в WG | default route | Route Allowed IPs off |
| не та секция | overlap lists | сузить, Exclusion |
| VLESS не импортируется | формат | outbound JSON |
| Reality handshake | SNI/key/SID/time | сверить параметры |
| URLTest не переключается | manual selector/test URL | Fastest, test URL |
| remote list не скачан | источник недоступен | download via section |
| FakeIP есть, соединения нет | tproxy/outbound | counters, порт 1602 |
| VPN section падает | interface | `curl --interface` |

## Источники

Podkop Wiki, коммит `34872e963af4c99116665a202ea83616fd6017ad`:

- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/sections
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/own-outbound
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/tunnels
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/workvpn
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/yacd
