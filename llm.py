from llama_cpp import Llama
import os

model_path = os.path.join("modelos", "llama2_7b_chat_uncensored-q4_0.gguf")
llm = Llama(model_path=model_path)

def ask_llm(prompt):
    response = llm(prompt, max_tokens=200)
    return response['choices'][0]['text'].strip()
def ask_llm_chat(question, context=""):
    """
    Função para perguntas gerais. Pode receber contexto (histórico).
    """
    full_prompt = f"{context}\nPergunta: {question}\nResposta:"
    response = llm(full_prompt, max_tokens=200)
    return response['choices'][0]['text'].strip()