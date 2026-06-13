---
name: podkop-troubleshooting
description: "Пошагово устранять подтвержденные неисправности Podkop на OpenWrt: неработающий DNS/FakeIP, sing-box, nftables/tproxy, VLESS/Reality, VPN-интерфейсы, конфликтующие пакеты, отдельные клиенты, LuCI, нестабильный WAN, установка и обновление. Использовать после podkop-diagnostics, когда первый сломанный слой уже локализован и требуется выбрать минимальное исправление, применить его, проверить результат или подготовить эскалацию."
---

# Podkop Troubleshooting

Исправлять первый сломанный этап цепочки, затем повторять тесты с начала. Не компенсировать DNS-ошибку routing rules и не переустанавливать Podkop до проверки логов.

## Алгоритм

1. Получить отчет `podkop-diagnostics` с первым сломанным слоем.
2. Если доказательств недостаточно, вернуться в `podkop-diagnostics`, а не угадывать.
3. Выбрать ветку: client/browser, LAN DNS, FakeIP без traffic, VLESS/Reality, VPN, install/LuCI или WAN.
4. Выполнить минимальное исправление из [references/troubleshooting-playbook.md](references/troubleshooting-playbook.md).
5. Перезапустить только нужную службу.
6. Повторить исходный тест и проверить обычный трафик.
7. Если гипотеза не подтверждена, вернуть временные изменения.

## Приоритет причин

1. Клиентский DNS/DoH/VPN/gateway.
2. dnsmasq.
3. sing-box.
4. nftables/tproxy.
5. outbound.
6. lists/sections.

## VLESS/Reality

- Не запрашивать полную публичную ссылку.
- Проверять время, DNS сервера, порт, UUID, flow, SNI, fingerprint, public key и short ID.
- Отличать импорт Podkop, handshake sing-box и недоступность сервера.
- Сравнивать с тестовой ссылкой и при необходимости использовать outbound JSON.
- Не заменять рабочие cover hostnames на шаблонные `vpn.*`, `proxy.*`, `ws.*`, `panel.*`, `admin.*` или transport paths вроде `/ws`, `/vpn`, `/proxy`, `/vless`, `/xray` как "быстрый фикс".

## Завершение

После исправления вызвать `podkop-diagnostics` повторно и проверить реальный сервис. Для эскалации приложить его отчет и артефакты.
