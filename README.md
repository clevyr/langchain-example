A basic langchain example running in a docker conatiner using ollama running a local llm.

Ollama inside a docker container cannot access the GPU/NPU on Apple Silicon, so Ollama should be running outside a container on the host machine.

Ollama should bind to `0.0.0.0:11434` rather than `127.0.0.1:11434` to allow access from within a docker container.
- Bind to `0.0.0.0:11434` once - will not persist after the server is stopped
```
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```
- Configure Ollama to always bind to `0.0.0.0:11434` - will require Ollama restart.
```
launchctl setenv OLLAMA_HOST "0.0.0.0:11434"
```

Once bound to `0.0.0.0:11434`, Ollama can be accessed at `<computer-name>.local:11434`. To find and edit your Mac's local hostname, search "local hostname" (and maybe scroll to the bottom) in System Settings.
