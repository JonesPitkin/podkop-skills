---
name: podkop-routing
description: Проектировать и настраивать маршрутизацию Podkop на OpenWrt через секции Proxy, VPN, Block и Exclusion; работать с VLESS, Reality, sing-box outbound JSON, Selector, URLTest, WireGuard/AWG/OpenVPN/OpenConnect, доменными и IP-списками, Fully Routed IPs, Mixed Proxy и Source Network Interface. Использовать при раздельной маршрутизации сервисов и устройств, нескольких туннелях, автоматическом переключении VLESS, пользовательских правилах и проверке попадания трафика в нужный outbound.
---

# Podkop Routing

Сначала описать политику словами, затем переводить ее в минимальный набор секций. Не начинать с редактирования сгенерированного sing-box JSON.

## Рабочий процесс

1. Составить таблицу `источник -> домены/подсети -> действие -> outbound -> DNS`.
2. Проверить: клиент использует роутер как DNS и gateway, FakeIP работает, nftables активен.
3. Выбрать тип:
   - `Proxy`: VLESS, Shadowsocks, Trojan, Hysteria2, SOCKS.
   - `VPN`: WG/AWG/OpenVPN/OpenConnect interface.
   - `Block`: отбросить.
   - `Exclusion`: исключить из других секций.
4. Для Proxy выбрать Connection URL, Selector, URLTest или Outbound Config.
5. Назначить community, user, local или remote lists без лишних перекрытий.
6. Для VPN при необходимости включить Domain Resolver.
7. Для устройства целиком использовать static lease и Fully Routed IPs.
8. Применить и проверить Dashboard/YACD, FakeIP и nftables counters.

## VLESS и Reality

- Предпочитать штатную `vless://` ссылку, если Podkop ее принимает.
- Иначе использовать sing-box outbound JSON.
- Проверять server, port, UUID, flow, TLS `server_name`, fingerprint, Reality `public_key` и `short_id`.
- Для публичных hostnames не генерировать transport-labeled cover names вроде `vpn.*`, `proxy.*`, `ws.*`, `panel.*`, `admin.*` без явного предупреждения о риске.
- Когда схема опирается на HTTP/CDN publication, предпочитать нейтральные hostname вроде `assets.*`, `static.*`, `media.*`, `content.*`, `files.*`.
- Никогда не помещать Reality private key в клиентский outbound.
- Отделять ошибку JSON от сетевой доступности сервера.

## Контроль изменений

- Добавлять по одной секции.
- Не включать одновременно `Russia inside`, `Russia outside`, `Ukraine`.
- Для отдельного сервиса внутри широкого списка заменить его набором узких.
- Не включать `Route Allowed IPs` с `0.0.0.0/0`, если нужен split routing.

## Подробности

Открыть [references/routing-guide.md](references/routing-guide.md) для VLESS/Reality JSON, URLTest, списков, VPN и ошибок.
