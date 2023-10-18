FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-runtime

RUN pip3 install pandas jupyterlab docker datasets transformers

RUN python3 -c 'from transformers import RagRetriever; RagRetriever.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base", dataset="wiki_dpr", index_name="exact")'

RUN python3 -c 'from transformers import RagRetriever; retriever = RagRetriever.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base", dataset="wiki_dpr", index_name="exact"); RagSequenceForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever);

