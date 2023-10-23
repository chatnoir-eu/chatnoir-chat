#a python script for inference on a single example using LlAMA model
import argparse
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM

device = "cuda:0" if torch.cuda.is_available() else "cpu"


falcon_prompt = "User: {input_sentence}\nAssistant:"


def run_inference(input_sentence, tokenizer, pipeline):
    # get output of the LlaMa from input sentence

    sequences = pipeline(
        falcon_prompt.format(input_sentence=input_sentence),
        max_length=200,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
    )

    return sequences[0]["generated_text"]

def load_model(model_path):

    print(f'Load model using Device "{device}" from path "{model_path}".')

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    pipeline = transformers.pipeline(
        "text-generation",
        model=model_path,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map=device,
    )
    return tokenizer, pipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_model", type=str, required=True)
    arg = parser.parse_args()
    tokenizer, pipeline = load_model(arg.input_model)

    print("Enter a sentence to generate your response. Enter 'exit' to exit.")
    previouses = []
    while True:
        input_sentence = input("Enter a sentence: ")
        if input_sentence == "exit":
            break
        run_inference(input_sentence,tokenizer,pipeline)






