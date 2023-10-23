#a python script for inference on a single example using LlAMA model
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
from peft import PeftModel

device = "cuda:0" if torch.cuda.is_available() else "cpu"

formatted_prompt = (
    f"A chat between a curious human and an artificial intelligence assistant."
    f"The assistant gives helpful, detailed, and polite answers to the user's questions.\n"
    "### Human: {prompt} ### Assistant:"
)


def run_inference(input_sentence, tokenizer, model, device):
    # get output of the LlaMa from input sentence

    input_sentence = formatted_prompt.format(prompt=input_sentence)

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

def load_model(model_path, lora_adapter_path):
    print(f'Load model using Device "{device}" from path "{model_path}".')

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        load_in_4bit=True,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        max_memory={i: '24000MB' for i in range(torch.cuda.device_count())},
        quantization_config=BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type='nf4'
        ),
    )
    model = PeftModel.from_pretrained(model, lora_adapter_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    return tokenizer, model

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_model", type=str, required=True)
    parser.add_argument("--lora_adapter", type=str, required=True)
    arg = parser.parse_args()
    tokenizer, model = load_model(arg.input_model, arg.lora_adapter)

    print("Enter a sentence to generate your response. Enter 'exit' to exit.")
    previouses = []
    while True:
        input_sentence = input("Enter a sentence: ")
        if input_sentence == "exit":
            break
        run_inference(input_sentence,  tokenizer, model, device)






