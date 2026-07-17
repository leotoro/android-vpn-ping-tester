import os
import platform
import subprocess
import time

class AndroidVpnTester:
    def __init__(self):
        # Servidores optimizados y comunes en configuraciones Android
        self.targets = {
            "Cloudflare DNS (1.1.1.1)": "1.1.1.1",
            "Google Public DNS (8.8.8.8)": "8.8.8.8",
            "Quad9 Security DNS (9.9.9.9)": "9.9.9.9",
            "NordVPN Shared Server": "103.86.96.100",
            "ExpressVPN Leak Test Server": "85.203.37.1"
        }
        self.system_os = platform.system().lower()

    def ping_server(self, hostname):
        """Ejecuta un comando de ping nativo según el sistema operativo."""
        # Configurar parámetros según si es Windows o Unix (Linux/Mac)
        param = '-n' if self.system_os == 'windows' else '-c'
        command = ['ping', param, '3', hostname]
        
        start_time = time.time()
        try:
            # Ejecutar comando ocultando la salida nativa de la consola
            response = subprocess.run(
                command, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL, 
                timeout=5
            )
            duration = (time.time() - start_time) * 1000 / 3 # Promedio estimado
            
            if response.returncode == 0:
                return round(duration, 2)
            return None
        except (subprocess.TimeoutExpired, Exception):
            return None

    def run_assessment(self):
        print("=" * 60)
        print("   ANDROID VPN & NETWORK PERFORMANCE BENCHMARK TOOL")
        print("=" * 60)
        print(r" Running network latency diagnostics...")
        print("-" * 60)
        
        for name, ip in self.targets.items():
            print(f"Testing connectivity to {name} [{ip}]...", end="", flush=True)
            latency = self.ping_server(ip)
            
            if latency:
                print(f" [SUCCESS] -> Latency: {latency} ms")
            else:
                print(" [FAILED] -> Host unreachable or packet loss 100%")
                
        print("-" * 60)
        print("Analysis completed successfully.")
        print("=" * 60)

if __name__ == "__main__":
    tester = AndroidVpnTester()
    tester.run_assessment()
  
