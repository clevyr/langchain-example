from langchain_openai import ChatOpenAI
from langchain_core.tools import tool, BaseTool
from langchain_core.utils.utils import convert_to_secret_str
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from os import environ
from typing import Sequence

openai_model = environ.get("OPENAI_MODEL", "")
openai_base_url = environ.get("OPENAI_BASE_URL", "")
openai_api_key = convert_to_secret_str(environ.get("OPENAI_API_KEY", ""))


# define tool that the llm can use
# the doctring for each function will be used as a tool description for the llm
@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together.

    Args:
        first_int: The first int to multiply.
        second_int: The second int to multiply.
    """
    return first_int * second_int


@tool
def add(first_int: int, second_int: int) -> int:
    """Add two integers together.

    Args:
        first_int: The first int to add.
        second_int: The second int to add.
    """

    return first_int + second_int


@tool
def exponentiate(base: int, exponent: int) -> int:
    """Add two integers together.

    Args:
        base: The int that will exponentiated.
        exponent: The power that the base is rased to.
    """

    return base**exponent


tools = [multiply, add, exponentiate]


def basic_agent():
    # We pull a promt from the langchain hub
    prompt = hub.pull("hwchase17/openai-tools-agent")
    prompt.pretty_print()

    # use our local ollama as the llm
    llm = ChatOpenAI(
        api_key=openai_api_key,
        model=openai_model,
        temperature=0,
        base_url=openai_base_url,
        # other params...
    )

    # Construct the tool calling agent
    # This just decides which tools to call
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Create an agent executor by passing in the agent and tools
    # This actually calls the tool and continues the agentic loop
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    print(
        agent_executor.invoke(
            {
                "input": "Take three to the fifth power and multiply that by the sum of twelve and three, then square the whole result"
            }
        )
    )
