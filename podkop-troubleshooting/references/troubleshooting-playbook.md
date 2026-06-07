# Playbook устранения неисправностей Podkop

## Содержание

- Один клиент
- DNS LAN
- FakeIP без трафика
- sing-box
- VLESS/Reality
- VPN
- Routing
- Install/LuCI/WAN
- Эскалация
- Источники

## Один клиент

Применять, если диагностика показала, что другие клиенты исправны, а проблемный обходит DNS или gateway роутера.

1. Вернуть DNS и gateway к значениям DHCP роутера.
2. Отключить Secure DNS, Android Private DNS или сторонний VPN, подтвердивший обход.
3. Для hardcoded DNS добавить redirect TCP/UDP 53; DoT/DoH исправлять отдельной firewall/browser policy.
4. Повторно вызвать `podkop-diagnostics`.

## DNS LAN

Применять, если диагностика показала неверный dnsmasq forward, недоступный upstream или DNS-петлю.

Восстановить `noresolv='1'` и `server='127.0.0.42'`. При Dont Touch My DHCP настроить вручную по `podkop-dns`. Исправить upstream/Bootstrap, затем:

```sh
service dnsmasq restart
service podkop restart
```

Исключить `https-dns-proxy`, nextdns и AGH loop.

## FakeIP без трафика

Применять, если FakeIP подтвержден, но диагностика показала нулевые/расходящиеся counters или конфликт mark rules.

1. Исправить gateway клиента, если он не ведет через OpenWrt.
2. Отключить подтвержденный конфликт GetDomains/GL.iNet vpn-client/старого script.
3. Не очищать весь ruleset.
4. Перезапустить Podkop и повторить диагностику counters и `127.0.0.1:1602`.

## sing-box

Применять к конкретной ошибке из логов:

1. Обновить sing-box до совместимой версии, если диагностирована старая версия.
2. Отключить отдельный autostart sing-box, если он конкурирует с Podkop.
3. При invalid JSON/unsupported option исправить только последнюю секцию или outbound.
4. При bind error освободить только занятый обязательный порт.
5. Перезапустить Podkop и повторить `podkop-diagnostics`.

## VLESS/Reality

### Импорт

Если URL работает в NekoBox, экспортировать только sing-box outbound JSON.

### DNS/timeout

Если диагностика локализовала DNS имени сервера, исправить upstream/bootstrap через `podkop-dns`. Если локализован недоступный порт, исправлять server/firewall/provider.

### Handshake

Сверить время, `server_name`, fingerprint, Reality public key, short ID, UUID и `xtls-rprx-vision`. Private key не должен быть в клиенте.

### Сервер работает, сайт не идет

Проверить list, overlap, Exclusion и YACD `Conns`; убедиться в FakeIP браузера.

## VPN

Если interface test диагностики падает, чинить подтвержденный handshake/routes/MTU/credentials. Для split routing убрать default route через `Route Allowed IPs`; в OpenVPN использовать `pull-filter ignore redirect-gateway`.

## Routing

- Не сочетать взаимоисключающие country lists.
- Для отдельного сервиса декомпозировать широкий список.
- При блокировке GitHub скачивать lists через section.
- Для WARP + Cloudflare subnet wiki предлагает firewall mark `0x00200000`.
- При FakeIP loop локального сервиса включить Resolve real IP for routing.

## Install, LuCI и WAN

### LuCI

Закрыть другие вкладки, hard reload/удалить данные сайта или открыть инкогнито.

### После stop нет интернета

Восстановить upstream dnsmasq: peer DNS WAN или явный forward.

### Нестабильный WAN

Включить Interface Monitoring, выбрать WAN и выполнить:

```sh
service podkop restart
```

### После sysupgrade

Остановить Podkop, временно поставить рабочий DNS, синхронизировать время, переустановить и запустить Podkop.

## Эскалация

Одним сообщением приложить:

1. Что делали, ожидали, получили.
2. Шаги воспроизведения.
3. Скрин Diagnostics с проблемного устройства.
4. `/usr/bin/podkop global_check`.
5. Логи Podkop/sing-box.
6. Install/update log.
7. Версии OpenWrt, Podkop, LuCI app, sing-box.

Удалить секреты, обновить Podkop и очистить LuCI cache.

## Источники

Podkop Wiki, коммит `34872e963af4c99116665a202ea83616fd6017ad`:

- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/troubleshooting
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/diagnostics
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/faq
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/badwan
- https://github.com/itdoginfo/podkop-wiki/tree/main/content/docs/clear-browser-cache
