import os

# If running inside a docker container,
# this default url will not work
ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434/')
ollama_model = os.getenv('OLLAMA_MODEL','mistral')

openai_model = os.getenv('OPENAI_MODEL')
openai_base_url = os.getenv('OPENAI_BASE_URL')
openai_api_key = os.getenv('OPENAI_API_KEY')
