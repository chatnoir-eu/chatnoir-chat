# Chatnoir-Chat


Run it locally (alpaca-7b) via:

```
docker run --rm -ti --entrypoint python3 registry.webis.de/code-lib/public-images/chatnoir-chat:0.0.1 alpaca-en-7b/run_inference.py --input_model /workspace/llama/alpaca-7b
```

Run it locally (gpt2-base) via:

```
docker run --rm -ti --entrypoint python3 registry.webis.de/code-lib/public-images/chatnoir-chat-gpt2-base:0.0.1 GPT-2-models/run_inference.py --input_model /workspace/gpt2_models/gpt2
```
Run it locally (gpt2-base) via:

```
docker run --rm -ti --entrypoint python3 registry.webis.de/code-lib/public-images/chatnoir-chat-gpt2-base:0.0.1 GPT-2-models/run_inference.py --input_model /workspace/gpt2_models/gpt2-large
```


Run it locally (gpt2-xl) via:

```
docker run --rm -ti --entrypoint python3 registry.webis.de/code-lib/public-images/chatnoir-chat-gpt2-xl:0.0.1 GPT-2-models/run_inference.py --input_model /workspace/gpt2_models/gpt2-xl
```

Run it locally (Falcon-7b-instruct) via:

```
docker run --rm -ti --entrypoint python3 registry.webis.de/code-lib/public-images/chatnoir-chat-gpt2-xl:0.0.1 Falcon-models/run_inference.py --input_model /workspace/falcon/falcon-7b-instruct
```


Run it locally (Guanaco-7b) via:
```
docker run --rm -ti --entrypoint python3 registry.webis.de/code-lib/public-images/chatnoir-chat-gpt2-xl:0.0.1 Guanaco/run_inference.py --input_model /workspace/llama/llama-7b --lora_adapter /workspace/llama/guanaco/
```


Run it locally (llama-2-7b-chat) via:
```
docker run --rm -ti --entrypoint python3 registry.webis.de/code-lib/public-images/chatnoir-chat-gpt2-xl:0.0.1 llama-2-models/run_inference.py --input_model /workspace/llama/llama-2-7b-chat
```


Run it locally (Bool2NLQ-alpaca) via:

```
docker run --rm -ti --entrypoint python3 registry.webis.de/code-lib/public-images/chatnoir-chat-gpt2-xl:0.0.1 alpaca-en-7b/run_inference.py --input_model /workspace/Bool2NLQ-alpaca
```
