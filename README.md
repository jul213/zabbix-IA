# 🛡️ AIOps Ecosystem: Real-Time Intelligence with Zabbix & Phi-3

Este proyecto implementa una solución de **AIOps**, diseñada para la interpretación semántica de logs mediante un modelo de lenguaje ligero y eficiente.

## 🧠 El Concepto
El sistema monitoriza el `syslog` en tiempo real. Al detectar un evento crítico, el middleware procesa el log y consulta a un modelo **Phi-3** local para obtener un diagnóstico inmediato, enviando la solución directamente al panel de Zabbix.

## 🛠️ Stack Tecnológico
* **Monitorización:** Zabbix 7.0 (Docker)
* **IA Local:** Ollama con **Phi-3** (Microsoft)
* **Lenguaje:** Python 3.10
* **Resiliencia:** Bash Watchdog Script

## 🏗️ Estructura del Repositorio
* `ia_monitor.py`: Middleware de comunicación entre Syslog, Ollama y Zabbix.
* `docker-compose.yml`: Infraestructura del servidor Zabbix y base de datos.
* `check_sistema.sh`: Sistema de auto-recuperación y limpieza de logs.

## 🚀 Despliegue Rápido
1. `docker-compose up -d`
2. `ollama run phi3`
3. `sudo python3 ia_monitor.py`
