@echo off
"C:\Program Files\ZAP\Zed Attack Proxy\ZAP.exe" -daemon -config api.key=je5nmou3u45vahn9lkfk5rhsoq -config api.addrs.addr.name=127.0.0.1 -config api.addrs.addr.enabled=true -config proxy.port=8090
echo ZAP launched. Press any key to close.
pause
