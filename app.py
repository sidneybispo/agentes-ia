import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from Tools.search_tools import SearchTools  # Importando a classe SearchTools
from langchain_openai import ChatOpenAI  # Importando a classe ChatOpenAI

# Carregar variáveis de ambiente do .env
load_dotenv()

# Pegar a chave da API do Serper
serper_api_key = os.getenv('SERPER_API_KEY')

# Verificar se a chave da API do Serper foi carregada corretamente
if not serper_api_key:
    raise ValueError("A chave da API do Serper não foi encontrada. Verifique o arquivo .env")

# Instanciar a ferramenta de busca usando a classe SearchTools
search_tool = SearchTools()

# 1. Agente de Pesquisa (Researcher) - usando Serper para pesquisas
researcher = Agent(
    role="Researcher",
    goal="""Explique o que são agentes de IA, como eles funcionam, e identifique as principais bibliotecas, como LangChain, 
    que são usadas para criá-los.""",
    backstory="""Pesquise como bibliotecas como LangChain permitem a criação de agentes e identifique os componentes básicos, como ambientes,
    ferramentas e funções.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool.search_internet]  # Usando o método de busca da classe
)

# 2. Agente Escritor (Writer)
writer = Agent(
    role="Writer",
    goal="Desenvolva um tutorial completo explicando como criar agentes utilizando a LangChain.",
    backstory="""Estruture a explicação de forma didática, com uma introdução sobre agentes, os principais componentes da LangChain,
    e exemplos de implementação.""",
    verbose=True,
    allow_delegation=False
)

# 3. Agente Desenvolvedor (Developer)
developer = Agent(
    role="Developer",
    goal="Forneça exemplos práticos de código para a criação de agentes com LangChain.",
    backstory="""Implemente um agente simples usando LangChain que possa responder perguntas usando uma base de conhecimento ou uma API.""",
    verbose=True,
    allow_delegation=False
)

# 4. Agente Revisor (Reviewer)
reviewer = Agent(
    role="Reviewer",
    goal="Revisar o tutorial criado e garantir que ele esteja claro, preciso e fácil de entender.",
    backstory="""Verifique se o tutorial cobre todos os aspectos essenciais, se o código está correto, e se o leitor consegue
    seguir as instruções sem dificuldades.""",
    verbose=True,
    allow_delegation=False
)

# Instanciar o modelo GPT-4 Mini
OpenAIGPT4Mini = ChatOpenAI(
    model="gpt-4-mini"  # Especifica o modelo como GPT-4 Mini
)

# Definir tarefas para cada agente
task1 = Task(
    description="""Pesquise sobre agentes de IA e como criá-los usando a LangChain, descrevendo os principais componentes.""",
    agent=researcher,
    expected_output="Lista de componentes principais da LangChain e explicações sobre agentes de IA."
)

task2 = Task(
    description="""Crie uma estrutura de tutorial explicando como criar agentes com LangChain, cobrindo desde a introdução até exemplos práticos.""",
    agent=writer,
    expected_output="Estrutura completa do tutorial sobre criação de agentes com LangChain."
)

task3 = Task(
    description="""Implemente um exemplo prático de um agente de IA básico usando LangChain e forneça o código comentado.""",
    agent=developer,
    expected_output="Código-fonte de um agente básico utilizando LangChain, com comentários e explicações."
)

task4 = Task(
    description="""Revise o tutorial e o código, garantindo que o conteúdo seja compreensível e que os exemplos estejam corretos.""",
    agent=reviewer,
    expected_output="Revisão completa do tutorial e código, garantindo clareza e precisão."
)

# Instanciar a equipe (Crew) e adicionar as tarefas
crew = Crew(
    agents=[researcher, writer, developer, reviewer],
    tasks=[task1, task2, task3, task4],
    verbose=True,
    process=Process.sequential,  # As tarefas serão executadas uma após a outra
    manager_llm=OpenAIGPT4Mini  # Adiciona o modelo GPT-4 Mini como gerente
)

# Iniciar o processo de execução dos agentes
result = crew.kickoff()

# Exibir resultados
print("######################")
print(result)
