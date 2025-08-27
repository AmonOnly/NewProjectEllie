# tools/apps.py
import subprocess
import platform

def open_app(app_name):
    """
    Abre um aplicativo pelo nome.
    """
    system = platform.system()
    
    try:
        if system == "Linux":
            # Usando 'xdg-open' ou chamando direto o app
            if app_name.lower() == "firefox":
                subprocess.Popen(["firefox"])
            else:
                subprocess.Popen([app_name])
        
        elif system == "Windows":
            import os
            os.startfile(app_name)  # para apps do Windows
            
        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", app_name])
        
        return f"{app_name} aberto com sucesso!"
    
    except Exception as e:
        return f"Erro ao abrir {app_name}: {e}"
