import langroid as lr
import langroid.language_models as lm
from langroid.agent.tools.recipient_tool import RecipientTool
from os import environ

ollama_model = environ.get("OLLAMA_MODEL")

# This example works best with chatGPT or llama3:70b
def startup():
    # set up LLM
    llm_cfg = lm.OpenAIGPTConfig(
        chat_model=f'ollama/{ollama_model}',  # use ollama. will use OLLAMA_HOST env for ollama location
        chat_context_length=32_000,
        timeout=120,
    )

    # use LLM in an Agent
    agent_cfg = lr.ChatAgentConfig(llm=llm_cfg)

    # Multi-Agent chat loop: Teacher Agent asks questions to Student Agent

    ceo_agent = lr.ChatAgent(agent_cfg)
    ceo_agent.enable_message(
        RecipientTool
    )  # because it is talking to more than one agent? Human client and PM
    ceo_task = lr.Task(
        ceo_agent,
        name="CEO",
        interactive=False,
        llm_delegate=True,  # because I want to LLM to decide when the task is done instead of some special meesage
        system_message="""
        You are the CEO of a software development company called AdvancedTech focused on understanding client needs,
        knowing your team strengths and delivering a product that solves the clients problems completely and thoroughly.

        You're job is to work with the project manager to proprose a solution for a client's needs.
        When the client is satisfied with the solution, simply respond with "DONE"

        You communicate ONLY with the Client or your ProjectManager.
        Use the `recipient_tool` to address one of these.

        YOU MUST ALWAYS START BY ASKING THE CLIENT WHAT THEY NEED.
        For example

        DONT WRITE ANY CODE.

        INSTEAD SEND THE TASK TO THE PROJECT MANAGER AS IS WITH A REASONABLE DEADLINE.

        IMPORTANT - Once you have client approval to start the project, simply respond with "DONE".

        ```Example Response 1:
            {
                "intended_recipient":"Client",
                "content":"...",
                "request":"recipient_message"
            }
        ```
        ```Example Response 2:
            {
                "intended_recipient":"ProjectManager",
                "content":"...",
                "request":"recipient_message"
            }
        ```
        ```Example Response 3:
            {
                "intended_recipient":"Cient",
                "content":"DONE",
                "request":"recipient_message"
            }
        ```
        """,
    )

    client_agent = lr.ChatAgent(agent_cfg)
    client_task = lr.Task(
        client_agent,
        name="Client",
        interactive=False,
        system_message='''You are the CLIENT for a software development company called AdvnacedTach.
        You have many needs invloving a wide range of industries.agent=

        Ask the CEO of AdvancedTech to solve a particular proplem you have. When the CEO responds with a solution,
        you may ask for futher details, clarification, or modifications.

        IMPORTANT - once you are satisfied with the CEO's solution, tell them they have you're approval to start
        development on the solution.
        ''',
        single_round=True

    )

    pm_agent = lr.ChatAgent(agent_cfg)
    pm_agent.enable_message(
        RecipientTool
    )  # because it is talking to more than one agent? Talking to CEO and developer
    pm_task = lr.Task(
        pm_agent,
        name="ProjectManager",
        llm_delegate=True,  # because I want to LLM to decide when the task is done instead of some special meesage
        interactive=False,
        system_message="""
        You are the lead project manager at a software development company
        called AdvancedTech.

        You communicate only with either with the "CEO" or "Developer".

        The CEO will ask you to solve a client problme. You will ask the Developer to develop a solution
        and respond back to the CEO with the Developer's solutions.

        You're job is to esimate timelines, allocate resources, and request code from the developer.
        Be sure to provide specific requirements for the developer.

        Use the `recipient_tool` to address one of these.

        DO NOT WRITE ANY CODE OR PROPROSE ANY SOLUTIONS. Instead, ask the developer to delevope code.

        As soon as you get code from the developer, address the CEO
        and show them the code.

        ```Example Response 1:
            {
                "intended_recipient":"Developer",
                "content":"...",
                "request":"recipient_message"
            }
        ```
        ```Example Response 2:
            {
                "intended_recipient":"CEO",
                "content":"...",
                "request":"recipient_message"
            }
        ```
        """,
    )

    dev_agent = lr.ChatAgent(agent_cfg)
    # dev_agent.enable_message(RecipientTool)  # because it is NOT talking to more than one agent? Talking to ONLY PM
    dev_task = lr.Task(
        dev_agent,
        name="Developer",
        interactive=False,
        system_message="""
        You are an expert python developer. Simply return code for the given task.
        DO NOT RESPOND WITH ANYTHING OTHER THAN CODE
        """,
        single_round=True,
    )


    ceo_task.add_sub_task([client_task,  pm_task])
    pm_task.add_sub_task(dev_task)

    ceo_task.run()
