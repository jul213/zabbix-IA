import subprocess
import requests
import json
import os
import sys
import logging

# === CONFIGURACIÓN SENIOR OPTIMIZADA ===
LOG_FILE = "/var/log/syslog"
ZABBIX_SERVER = "127.0.0.1"
ZABBIX_PORT = 10052
ZABBIX_HOST = "IA-LOCAL"
ZABBIX_KEY = "ia.veredicto"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "phi3"

# Configuración de logs del script
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analizar_con_ia(log_line):
    """
    Motor de inferencia compacto: Máxima velocidad, misma inteligencia.
    """
    # PROMPT COMPRIMIDO (Menos tokens = Más velocidad)
    prompt_sistema = (
        f"Analiza técnicamente: '{log_line}'.\n"
        "Respuesta breve (1 frase por punto):\n"
        "🚨 DIAGNÓSTICO: <qué_pasa>\n"
        "🛠️ SOLUCIÓN: <acción_técnica>\n"
        "💻 COMANDOS: <comandos_linux>\n"
        "⚠️ RIESGO: <Bajo/Medio/Crítico>"
    )

    try:
        payload = {
            "model": MODELO,
            "prompt": prompt_sistema,
            "stream": False,
            "options": {
                "temperature": 0.1,   # Menos "creatividad", más velocidad técnica
                "num_predict": 150    # Límite de palabras para evitar respuestas largas
            }
        }
        # Timeout extendido a 120 para evitar el error de Read Timeout
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get('response', 'Error: IA no generó respuesta.')
    except Exception as e:
        logging.error(f"Fallo en conexión con Ollama: {e}")
        return f"Error de Middleware: Tiempo de espera agotado o motor offline."

def enviar_a_zabbix(veredicto):
    """
    Inyecta el veredicto en el ecosistema de Zabbix.
    """
    # Escapar comillas para evitar errores en el shell
    veredicto_esc = veredicto.replace('"', '\\"')
    
    comando = [
        "zabbix_sender",
        "-z", ZABBIX_SERVER,
        "-p", str(ZABBIX_PORT),
        "-s", ZABBIX_HOST,
        "-k", ZABBIX_KEY,
        "-o", veredicto_esc
    ]
    
    try:
        res = subprocess.run(comando, capture_output=True, text=True, check=True)
        logging.info(f"Zabbix Update: {res.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Fallo al enviar a Zabbix: {e.stderr}")

def monitor_main():
    """
    Bucle principal de monitoreo reactivo.
    """
    logging.info(f"🚀 Engine IA Online en {LOG_FILE}...")
    
    # Comando tail -F para lectura en tiempo real
    process = subprocess.Popen(['tail', '-F', LOG_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue
            
            # Filtro de criticidad para no saturar la CPU con logs informativos
            if any(word in line.upper() for word in ["CRITICAL", "ERROR", "FAIL", "WARNING"]):
                logging.warning(f"🎯 Evento crítico detectado. Procesando...")
                
                # 1. Analizar con el nuevo prompt compacto
                veredicto = analizar_con_ia(line)
                print(f"\n{veredicto}\n")
                
                # 2. Notificar a Zabbix
                enviar_a_zabbix(veredicto)
                
    except KeyboardInterrupt:
        logging.info("Terminando monitor de forma segura...")
        process.terminate()
    except Exception as e:
        logging.critical(f"Error fatal: {e}")
        process.terminate()

if __name__ == "__main__":
    # Verificación de requisitos
    if subprocess.run(["which", "zabbix_sender"], capture_output=True).returncode != 0:
        print("❌ ERROR: Falta 'zabbix_sender'. Instálalo con: sudo apt install zabbix-sender")
        sys.exit(1)
        
    monitor_main()
