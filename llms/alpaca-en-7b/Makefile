docker-build-basis:
	docker build -t registry.webis.de/code-lib/public-images/chatnoir-chat:0.0.1-basis docker/ -f docker/Dockerfile.basis
	docker push registry.webis.de/code-lib/public-images/chatnoir-chat:0.0.1-basis

docker-build-alpaca:
	docker build -t registry.webis.de/code-lib/public-images/chatnoir-chat:0.0.2-alpaca . -f docker/Dockerfile.alpaca
	docker push registry.webis.de/code-lib/public-images/chatnoir-chat:0.0.2-alpaca

docker-build-chatnoir:
	cp run_inference.py docker/run_inference.py
	cp flask_api.py docker/flask_api.py
	docker build -t registry.webis.de/code-lib/public-images/chatnoir-chat:0.0.8 docker -f docker/Dockerfile.chatnoir
	docker push registry.webis.de/code-lib/public-images/chatnoir-chat:0.0.8

docker-build-gpt2-xl:
	docker build -t registry.webis.de/code-lib/public-images/chatnoir-chat:0.0.1-gpt2-xl -f docker/Dockerfile.gpt2-xl .
	docker push registry.webis.de/code-lib/public-images/chatnoir-chat:0.0.1-gpt2-xl

docker-build-gpt2-large:
	docker build -t registry.webis.de/code-lib/public-images/chatnoir-chat:0.0.1-gpt2-large -f docker/Dockerfile.gpt2-large .
	docker push registry.webis.de/code-lib/public-images/chatnoir-chat:0.0.1-gpt2-large

docker-build-gpt2-base:
	docker build -t registry.webis.de/code-lib/public-images/chatnoir-chat:0.0.1-gpt2-base -f docker/Dockerfile.gpt2-base .
	docker push registry.webis.de/code-lib/public-images/chatnoir-chat:0.0.1-gpt2-base

docker-build-chatnoir-gpt:
	cp run_inference.py docker/run_inference.py
	cp flask_api.py docker/flask_api.py
	docker build -t registry.webis.de/code-lib/public-images/chatnoir-chat-gpt2-base:0.0.1 docker -f docker/Dockerfile.chatnoir-gpt2-base
	docker build -t registry.webis.de/code-lib/public-images/chatnoir-chat-gpt2-large:0.0.1 docker -f docker/Dockerfile.chatnoir-gpt2-large
	docker build -t registry.webis.de/code-lib/public-images/chatnoir-chat-gpt2-xl:0.0.1 docker -f docker/Dockerfile.chatnoir-gpt2-xl
	docker push registry.webis.de/code-lib/public-images/chatnoir-chat-gpt2-base:0.0.1
	docker push registry.webis.de/code-lib/public-images/chatnoir-chat-gpt2-large:0.0.1
	docker push registry.webis.de/code-lib/public-images/chatnoir-chat-gpt2-xl:0.0.1

docker-build-sentence-retrieval:
	cd sentence-retrieval \
	&& docker build -t registry.webis.de/code-lib/public-images/chatnoir-chat-sentence-retrieval:0.0.5 .

docker-build-sentence-retrieval-basis:
	docker build -t registry.webis.de/code-lib/public-images/chatnoir-chat-sentence-retrieval:0.0.1-basis -f sentence-retrieval/Dockerfile.basis .
	docker push registry.webis.de/code-lib/public-images/chatnoir-chat-sentence-retrieval:0.0.1-basis

local-sentence-retrieval:
	docker run --rm -ti -p 8888:8888  -w /workspace \
		-v $${PWD}:/workspace/ \
		-v /mnt/ceph/tira/state/ir_datasets:/root/.ir_datasets \
		-v /mnt/ceph/storage/corpora/corpora-thirdparty/corpus-clueweb22/:/mnt/ceph/storage/corpora/corpora-thirdparty/corpus-clueweb22/:ro \
		--entrypoint jupyter \
		registry.webis.de/code-lib/public-images/chatnoir-chat-sentence-retrieval:0.0.4 \
		notebook --allow-root --ip 0.0.0.0

