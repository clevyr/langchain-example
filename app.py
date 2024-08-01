from dotenv import load_dotenv

# have to load env before importing the app
load_dotenv()

from app import basic_chain, basic_agent, langroid_example, startup


if __name__ == "__main__":
    basic_chain()
    basic_agent()
    langroid_example()
    startup()
