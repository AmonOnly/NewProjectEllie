from asr import listen
from brain import route_command
from pynput import keyboard
from threading import Thread

def on_activate():
    """Função chamada quando hotkey é pressionada (voz)."""
    print("[MAIN] Hotkey ativada! Fale agora...")
    try:
        # Captura voz com duração opcional (ajuste se necessário)
        text = listen(duration=5)  # ou apenas listen() se sua função não usar duration
        if text.strip() == "":
            print("[MAIN] Nenhum texto detectado.")
            return
        print("[USUÁRIO (voz)]", text)
        route_command(text)
    except Exception as e:
        print("[ERROR VOZ]", e)

def text_loop():
    """Loop de entrada por texto."""
    while True:
        try:
            text = input("Digite um comando (ou 'sair' para encerrar): ")
            if text.lower() in ["sair", "exit"]:
                print("[MAIN] Encerrando assistente...")
                break
            if text.strip() == "":
                continue
            print("[USUÁRIO (texto)]", text)
            route_command(text)
        except KeyboardInterrupt:
            print("\n[MAIN] Interrupção detectada. Saindo...")
            break
        except Exception as e:
            print("[ERROR TEXTO]", e)

if __name__ == "__main__":
    from pynput.keyboard import GlobalHotKeys

    # Configura hotkey Ctrl+Space
    hotkey = GlobalHotKeys({
        '<ctrl>+<space>': on_activate
    })

    print("[MAIN] Assistente iniciado. Pressione Ctrl+Space para falar ou digite comandos.")

    # Hotkey roda em thread separada
    hotkey_thread = Thread(target=hotkey.start, daemon=True)
    hotkey_thread.start()

    # Loop principal de texto
    text_loop()

    # Para hotkey quando sai
    hotkey.stop()
    hotkey_thread.join()
    print("[MAIN] Assistente finalizado.")
