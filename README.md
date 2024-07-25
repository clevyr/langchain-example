A basic langchain example running in a docker conatiner using ollama running a local llm.

Ollama inside a docker container cannot access GPU/NPU on
Apple Silicon, so Ollama should be running outside a container on the host machine.

`localhost` on the host machine can be accessed from inside the container using `host.docker.internal`.
