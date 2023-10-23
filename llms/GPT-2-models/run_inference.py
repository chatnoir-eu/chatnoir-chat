#a python script for inference on a single example using LlAMA model
import argparse
from transformers import LlamaForCausalLM, LlamaTokenizer, AutoModelForCausalLM, AutoTokenizer
import torch

PROMPT_DICT = {
    "prompt_input": (
        "Below is an instruction that describes a task, paired with an input that provides further context. "
        "Write a response that appropriately completes the request.\n\n"
        "### Instruction:\n{instruction}\n\n### Input:\n{input}\n\n### Response:"
    ),
    "prompt_no_input": (
        "Below is an instruction that describes a task. "
        "Write a response that appropriately completes the request.\n\n"
        "### Instruction:\n{instruction}\n\n### Response:"
    ),
}


def run_inference(input_sentence, tokenizer, model, device):
    # get output of the LlaMa from input sentence
    input_sentence = PROMPT_DICT["prompt_no_input"].format(instruction=input_sentence)

    input_ids = tokenizer.encode(input_sentence, return_tensors="pt").to(device)
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=device)
    output_ids = model.generate(
        inputs=input_ids,
        attention_mask=attention_mask,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        num_beams=1,
        max_new_tokens=600,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
    )
    output_sentence = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    output_sentence = output_sentence.split("### Response:")[1]
    print(output_sentence)
    return output_sentence

def load_model(model_path):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f'Load model using Device "{device}" from path "{model_path}".')

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path).to(device)

    return tokenizer, model, device

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_model", type=str, required=True)
    arg = parser.parse_args()
    tokenizer, model, device = load_model(arg.input_model)

    print("Enter a sentence to generate your response. Enter 'exit' to exit.")
    previouses = []
    while True:
        input_sentence = input("Enter a sentence: ")
        if input_sentence == "exit":
            break
        run_inference(input_sentence,  tokenizer, model, device)






