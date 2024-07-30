import langroid as lr
import langroid.language_models as lm
from langroid.mytypes import Entity
from os import environ

ollama_model = environ.get('OLLAMA_MODEL')

def langroid_example() -> None:
    # set up LLM
    llm_cfg = lm.OpenAIGPTConfig( # or OpenAIAssistant to use Assistant API
    # any model served via an OpenAI-compatible API
    chat_model=f'ollama/{ollama_model}',
    chat_context_length=32_768,  # adjust based on model
    timeout=120,

    )

    # use LLM in an Agent
    agent_cfg = lr.ChatAgentConfig(llm=llm_cfg)
    agent = lr.ChatAgent(agent_cfg)

    # 2-Agent chat loop: Teacher Agent asks questions to Student Agent
    teacher_agent = lr.ChatAgent(agent_cfg)
    teacher_task = lr.Task(
    teacher_agent, name="Teacher",
    system_message="""
        Ask your student concise numbers questions.
        Use a variaty of operations and functions.
        If there is a student response, give consise feedback on their answer to your previous question.
        After giving feedback, ask another question.
        Makes these exchanges quick and don't add any extra words or content.
        Do not give feedback to the first message.

        All responses should be in the following form:
            Feedback: <your feedback on the student's answer>
            Question: <the nest question>
        """,
        user_message="Ask a single question - do not give feedback in the response to this message",
        interactive=False,
    )
    student_agent = lr.ChatAgent(agent_cfg)
    student_task = lr.Task(
    student_agent, name="Student",
    system_message="You are a students. A teacher will ask you questions. Concisely answer the teacher's questions.",
    single_round=True,
    interactive=False,

    )

    teacher_task.add_sub_task(student_task)

    # only 4 turns will be taken. Each agents' response counts as one turn.
    # With 4 turns, the teacher will ask 2 question and each will be ansered by the student
    teacher_task.run(turns=4)
