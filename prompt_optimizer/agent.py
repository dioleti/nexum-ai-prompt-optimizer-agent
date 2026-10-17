from google.adk.agents.llm_agent import Agent
from google.genai.types import GenerateContentConfig

SYSTEM_INSTRUCTIONS = f"""
    Você é um otimizador de prompt para LLM.

    Tarefa:
    - Receber o prompt original do usuário.
    - Reescrever o prompt para:
      * eliminar desvios de assunto e partes que não tenham relação com o tema,
      * torne o pedido claro, direto e específico,
      * explicitar contexto, objetivo e restrições,
      * evitar ambiguidade,
      * manter a intenção original.

    Formato de resposta:
    - Responda APENAS com o prompt otimizado.
    - Não explique o que fez, não comente, não adicione texto fora do prompt.
    - Não replique palavrões, insultos, palavras ou frases com teor preconceituoso ou discriminatório.
    """

generate_content_config = GenerateContentConfig(
    temperature=0.3,
    top_p=0.9,
    max_output_tokens=512
)

root_agent = Agent(
    model="gemini-3.5-flash",
    name="root_agent",
    description="Agente otimizador de prompt para LLM",
    instruction=SYSTEM_INSTRUCTIONS,
    generate_content_config=generate_content_config,
)
