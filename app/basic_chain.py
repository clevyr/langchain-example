from langchain_community.llms import Ollama
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from . import config

def basic_chain():
    llm = Ollama(
        model=config.ollama_model,
        temperature=0,
        base_url=config.ollama_base_url,
        # other params...
    )

    template = PromptTemplate.from_template("Tell me a joke about {topic}.")

    # chain some things together to make an llm chain
    chain = template | llm | CommaSeparatedListOutputParser()

    # the chain can be invoked multiple times with different parameters
    print(chain.invoke({"topic": "LangChain"}))
    print(chain.invoke({"topic": "Foxes"}))
