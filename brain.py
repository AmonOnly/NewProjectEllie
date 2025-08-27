# brain.py
import json
import re
from llm import ask_llm, ask_llm_chat
from tts import speak
from tools import apps, control, screen
from memory import add_entry, get_last_commands, load_memory

ASSISTANT_NAME = "ELLIE"

TOOLS = {
    "apps.open_app": apps.open_app,
    "control.type_text": control.type_text,
    "control.click_text": control.click_text,
    "screen.read_screen": screen.read_screen
}

def summarize_old_memory(max_lines=10):
    """Gera um resumo das memórias antigas."""
    memory = load_memory()
    if not memory:
        return "Nenhuma memória antiga."
    old_entries = memory[:-50] if len(memory) > 50 else []
    summary_lines = []
    for e in old_entries[-max_lines:]:
        feedback = e['feedback'] if e['feedback'] else "sem feedback"
        summary_lines.append(f"{e['command']} -> {e['tool']} ({feedback})")
    if not summary_lines:
        return "Nenhuma memória antiga relevante."
    return "\n".join(summary_lines)

def answer_question(text):
    """Responde perguntas gerais usando LLM e contexto de memória."""
    try:
        summary = summarize_old_memory()
        recent_history = get_last_commands(50)
        history_text = "\n".join(
            [f"{h['command']} -> {h['tool']} ({h['feedback']})" for h in recent_history]
        )
        prompt = f"""
Resumo antigo:
{summary}

Histórico recente:
{history_text}

Usuário disse: '{text}'
Responda de forma completa e clara.
"""
        answer = ask_llm_chat(prompt)
        speak(answer)
        print(f"[{ASSISTANT_NAME}]: {answer}")
    except Exception as e:
        print("[ERROR CHAT]", e)
        speak("Desculpe, não consegui responder a isso.")

def route_command(text):
    """Roteia comandos para ferramentas ou LLM."""
    try:
        lower_text = text.lower().strip()

        # Abrir aplicativos
        if lower_text.startswith(("abrir ", "iniciar ", "executar ")):
            app_name = lower_text.replace("abrir ", "").replace("iniciar ", "").replace("executar ", "").strip()
            tool_name = "apps.open_app"
            args = {"app_name": app_name}
            if tool_name in TOOLS:
                result = TOOLS[tool_name](**args)
                speak(result)
                print(f"[{ASSISTANT_NAME}]", result)
                add_entry(command=text, tool=tool_name, args=args, result=result, feedback=None)
                return

        # Digitar texto
        if lower_text.startswith(("digitar ", "escrever ")):
            msg = lower_text.replace("digitar ", "").replace("escrever ", "").strip()
            tool_name = "control.type_text"
            args = {"text": msg}
            if tool_name in TOOLS:
                result = TOOLS[tool_name](**args)
                speak("Texto digitado.")
                print(f"[{ASSISTANT_NAME}]", result)
                add_entry(command=text, tool=tool_name, args=args, result=result, feedback=None)
                return

        # Clicar texto
        if lower_text.startswith(("clicar em ", "click ")):
            target = lower_text.replace("clicar em ", "").replace("click ", "").strip()
            tool_name = "control.click_text"
            args = {"target": target}
            if tool_name in TOOLS:
                result = TOOLS[tool_name](**args)
                speak(f"Clique realizado em {target}.")
                print(f"[{ASSISTANT_NAME}]", result)
                add_entry(command=text, tool=tool_name, args=args, result=result, feedback=None)
                return

        # Ler tela
        if lower_text in ("ler tela", "ler o que está na tela"):
            tool_name = "screen.read_screen"
            args = {}
            if tool_name in TOOLS:
                result = TOOLS[tool_name](**args)
                speak("Conteúdo da tela:")
                speak(result)
                print(f"[{ASSISTANT_NAME}]", result)
                add_entry(command=text, tool=tool_name, args=args, result=result, feedback=None)
                return

        # Se não for comando explícito, LLM tenta interpretar
        recent_history = get_last_commands(50)
        history_text = "\n".join(
            [f"{h['command']} -> {h['tool']} ({h['feedback']})" for h in recent_history]
        )
        old_summary = summarize_old_memory()

        prompt = f"""
Resumo antigo:
{old_summary}

Histórico recente:
{history_text}

Usuário disse: '{text}'
Retorne SOMENTE um JSON válido com os campos:
{{
 "tool": "<nome da ferramenta>",
 "args": {{}}
}}
Não escreva nada fora do JSON.
"""
        llm_response = ask_llm(prompt)
        if not llm_response.strip():
            answer_question(text)
            return

        match = re.search(r"\{.*\}", llm_response, re.DOTALL)
        if match:
            llm_response = match.group(0)
        else:
            answer_question(text)
            return

        try:
            cmd = json.loads(llm_response)
        except json.JSONDecodeError:
            answer_question(text)
            return

        tool_name = cmd.get("tool")
        args = cmd.get("args", {})

        if tool_name in TOOLS:
            result = TOOLS[tool_name](**args)
            speak(f"Executado: {tool_name}")
            print(f"[{ASSISTANT_NAME}]", result)

            feedback = input("Foi útil? (sim/não): ").strip().lower()
            if feedback not in ["sim", "não"]:
                feedback = None
            add_entry(command=text, tool=tool_name, args=args, result=result, feedback=feedback)
        else:
            answer_question(text)

    except Exception as e:
        print("[ERROR]", e)
        speak("Erro ao processar o comando.")
