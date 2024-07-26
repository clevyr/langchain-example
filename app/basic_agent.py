from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from . import config

# define tool that the llm can use
# the doctring for each function will be used as a tool description for the llm
@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together."""
    print(f'multiply: {first_int} * {second_int}')
    return first_int * second_int


@tool
def add(first_int: int, second_int: int) -> int:
    "Add two integers."
    print(f'add: {first_int} * {second_int}')
    return first_int + second_int


@tool
def exponentiate(base: int, exponent: int) -> int:
    "Exponentiate the base to the exponent power."
    print(f'exponentiate: {base} * {exponent}')
    return base**exponent


tools = [multiply, add, exponentiate]

def basic_agent():
    # We pull a promt from the langchain hub
    prompt = hub.pull("hwchase17/openai-tools-agent")
    prompt.pretty_print()

    # use our local ollama as the llm
    llm = ChatOpenAI(
        api_key=config.openai_api_key,
        model=config.openai_model,
        temperature=0,
        base_url=config.openai_base_url,
        # other params...
    )

    # Construct the tool calling agent
    # This just decides which tools to call
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Create an agent executor by passing in the agent and tools
    # This actually calls the tool and continues the agentic loop
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    print(agent_executor.invoke(
        {
            "input": "Take 3 to the fifth power and multiply that by the sum of twelve and three, then square the whole result"
        }
    ))
