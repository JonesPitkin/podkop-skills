---
name: podkop-install
description: Устанавливать, обновлять, удалять и восстанавливать Podkop на OpenWrt с учетом версии ОС, пакетного менеджера opkg/apk, места во flash, зависимостей sing-box и jq, конфликтов GetDomains, https-dns-proxy и legacy iptables. Использовать при первичной установке Podkop, обновлении Podkop или sing-box, переносе через sysupgrade, ошибках установки, нехватке места и проверке совместимости прошивки.
---

# Podkop Install

Устанавливать Podkop только после инвентаризации роутера. Не переносить команды между версиями OpenWrt без проверки пакетного менеджера и репозиториев.

## Рабочий процесс

1. Определить версию и тип прошивки:
   ```sh
   cat /etc/openwrt_release
   ubus call system board
   command -v opkg || command -v apk
   ```
2. Проверить время, DNS, интернет и свободное место:
   ```sh
   date
   nslookup downloads.openwrt.org
   df -h /overlay
   ```
3. Проверить конфликтующие пакеты и остатки прежних решений:
   ```sh
   opkg list-installed 2>/dev/null | grep -E 'podkop|sing-box|https-dns-proxy|nextdns|iptables-mod-extra'
   ```
4. Выбрать поддерживаемую ветку:
   - OpenWrt 24.10: основной протестированный вариант.
   - OpenWrt 23.05: не рекомендовать; Podkop 0.5.0+ требует sing-box 1.12 и jq 1.7.1.
   - OpenWrt 25.12: использовать install script или `.apk`, но отметить статус как не протестированный в контрольной версии wiki.
5. Перед изменениями сохранить UCI-конфигурацию:
   ```sh
   uci export podkop > /tmp/podkop-backup.uci 2>/dev/null || true
   uci export dhcp > /tmp/dhcp-backup.uci
   ```
6. Выполнить установку или обновление по [references/install-guide.md](references/install-guide.md).
7. После установки очистить кэш LuCI и проверить Dashboard и Diagnostics.
8. Не считать установку успешной, пока не проверены версия sing-box, запуск Podkop, DNS и FakeIP.

## Правила безопасности

- Не применять `--force-space`, пока реальное свободное место не проверено.
- Не удалять VPN-интерфейсы, firewall zones и forwarding без отдельной причины.
- Останавливать Podkop перед обновлением sing-box и sysupgrade OpenWrt.
- Считать кастомные прошивки отдельным риском: GL.iNet `vpn-client`, отсутствие nftables, встроенные `https-dns-proxy`/`nextdns` и альтернативные репозитории могут ломать tproxy.
- Не публиковать VLESS URL, UUID, Reality keys, short ID и конфиги с секретами.

## Проверка результата

```sh
service podkop status
sing-box version
netstat -tanp | grep -E '127\.0\.0\.42:53|127\.0\.0\.1:1602'
/usr/bin/podkop global_check
```

На клиенте:

```sh
nslookup fakeip.podkop.fyi
curl -v https://fakeip.podkop.fyi/check
```

Ожидать FakeIP из `198.18.0.0/15` и JSON с `"fakeip": true`.

## Подробности

Открыть [references/install-guide.md](references/install-guide.md) для пошаговой установки, обновления, восстановления после sysupgrade, сценариев нехватки места и таблицы ошибок.

