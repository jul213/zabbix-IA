#!/bin/bash
echo "--- VERIFICACIÓN DE SISTEMA IA-ZABBIX ---"
[ -f /var/log/ia_monitor.log ] && echo "✅ Archivo de log: EXISTE" || echo "❌ Archivo de log: NO EXISTE"
ls -l /var/log/ia_monitor.log | grep -q "rw-rw-rw-" && echo "✅ Permisos log: CORRECTOS" || echo "❌ Permisos log: INCORRECTOS (ejecuta chmod 666)"
systemctl is-active --quiet ia-zabbix && echo "✅ Servicio Systemd: CORRIENDO" || echo "❌ Servicio Systemd: CAÍDO"
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:11434/api/tags | grep -q "200" && echo "✅ Ollama API: RESPONDIDENDO" || echo "❌ Ollama API: NO RESPONDE"
echo "----------------------------------------"
