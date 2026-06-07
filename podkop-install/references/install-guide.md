# Руководство по установке Podkop

## Содержание

- Поддерживаемая среда
- Автоматическая и ручная установка
- Обновление Podkop и sing-box
- Sysupgrade и удаление
- Типовые сценарии
- Ошибки и диагностика
- Источники

## Поддерживаемая среда

Базовая рекомендация wiki: ванильная OpenWrt 24.10 и не менее 20 МБ свободного места на NAND. Пакеты `podkop_*.ipk` и `luci-app-podkop_*.ipk` архитектурно независимы, но `sing-box` и другие зависимости зависят от репозитория OpenWrt.

Перед установкой:

```sh
cat /etc/openwrt_release
opkg print-architecture 2>/dev/null
df -h /overlay
date
nslookup github.com
```

## Автоматическая установка и обновление

Для OpenWrt 24.10 использовать официальный скрипт:

```sh
sh <(wget -O - https://raw.githubusercontent.com/itdoginfo/podkop/refs/heads/main/install.sh)
```

Если Podkop установлен, скрипт выполняет обновление. Сохранить полный вывод терминала при ошибке.

Перед запуском:

1. Удалить GetDomains его официальным uninstall script, если он установлен.
2. Разрешить скрипту удалить `https-dns-proxy` либо удалить вручную:
   ```sh
   opkg remove --force-depends luci-app-https-dns-proxy https-dns-proxy luci-i18n-https-dns-proxy*
   ```
3. Проверить `iptables-mod-extra`; legacy iptables может конфликтовать с nftables tproxy.
4. Убедиться, что системное время корректно.

## Ручная установка

Для OpenWrt с `opkg`:

```sh
opkg update
opkg install /tmp/podkop_*.ipk
opkg install /tmp/luci-app-podkop_*.ipk
```

Всегда устанавливать сначала `podkop`, затем LuCI-приложение. Для OpenWrt 25.12 использовать соответствующие `.apk` и синтаксис установленного пакетного менеджера; не смешивать `.ipk` и `.apk`.

## Обновление sing-box

Install script обновляет sing-box, если версия ниже минимальной. Для ручного обновления:

```sh
service podkop stop
opkg update
opkg upgrade sing-box
service podkop start
```

Диагностика wiki ожидает sing-box не ниже 1.12.4:

```sh
sing-box version
ls -l /etc/init.d/sing-box
```

Автостарт отдельной службы sing-box должен быть отключен: ею управляет Podkop.

## Нехватка места

```sh
df -h /overlay
du -h -d 1 /overlay 2>/dev/null | sort -h
```

Варианты:

1. Удалить ненужные пакеты и кэш.
2. Использовать `sing-box-tiny`, если подходит отсутствие встроенного Tailscale:
   ```sh
   service podkop stop
   opkg update
   opkg remove sing-box --force-depends
   opkg install sing-box-tiny
   service podkop start
   ```
3. Применять `--force-space` только когда расчет opkg явно неверен.
4. Для малой flash собрать образ OpenWrt со встроенными `libc`, `ca-bundle`, `kmod-inet-diag`, `kmod-tun`, `sing-box` или `sing-box-tiny`.

## Sysupgrade

Перед обновлением:

```sh
service podkop stop
```

После sysupgrade переустановить Podkop. Если обновление сделано без остановки и DNS пропал:

```sh
service podkop stop
uci -q delete dhcp.@dnsmasq[0].server
uci add_list dhcp.@dnsmasq[0].server="8.8.8.8"
uci commit dhcp
service dnsmasq restart
ntpd -q -p ptbtime1.ptb.de
service podkop start
```

## Удаление

```sh
opkg remove luci-i18n-podkop-ru luci-app-podkop podkop
```

После удаления проверить рабочий upstream dnsmasq.

## Типовые сценарии

### Чистая OpenWrt 24.10

Проверить 20+ МБ, время и DNS; запустить install script; очистить кэш LuCI; настроить секцию; запустить Diagnostics.

### Переход с GetDomains

Сохранить VPN-интерфейсы; удалить только GetDomains; проверить остаточные mark rules; установить Podkop; не восстанавливать старые nftables-правила.

### Кастомная прошивка

Проверить nftables/tproxy, репозитории и встроенные DNS/VPN-службы. На GL.iNet проверить конфликт `vpn-client`; на сборках без nftables Podkop работать не будет.

### VLESS + Reality после установки

Добавить VLESS URL в Proxy section. Если URL не импортируется, использовать sing-box outbound JSON. Проверить `server`, порт, UUID, flow, TLS `server_name`, fingerprint, Reality `public_key` и `short_id`; private key остается на сервере.

## Ошибки и диагностика

| Симптом | Вероятная причина | Проверка | Действие |
|---|---|---|---|
| `Operation not permitted` | неверное время, DNS или IPv6 | `date`, `nslookup` | NTP, восстановить DNS, проверить IPv6 |
| `Only have ... available` | flash или расчет opkg | `df -h /overlay` | освободить место, tiny; force только после проверки |
| sing-box не запускается | версия или конфиг | version, логи | обновить, проверить outbound |
| После остановки нет интернета | нет upstream dnsmasq | `uci show dhcp` | peer DNS WAN или DNS forward |
| LuCI показывает старое | browser cache | инкогнито | hard reload |
| FakeIP не маршрутизируется | nftables conflict | `nft list ruleset` | удалить подтвержденный конфликт |

## Источники

Podkop Wiki, коммит `34872e963af4c99116665a202ea83616fd6017ad` от 2026-05-29:

- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/install
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/faq
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/diagnostics
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/clear-browser-cache

