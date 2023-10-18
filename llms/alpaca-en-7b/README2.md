# To reproduce, first set up your environment:
Note that you have to use latest transformer version, otherwise LLAMA not included
```
 conda create -n alpaca python=3.10
 conda activate alpaca
 pip3 install -r requirements.txt
 git clone https://github.com/huggingface/transformers.git
 cd transformers
 pip3 install -e .
```
To download your model, please fill the form at Meta, 
Or I have downloaded for you


Note that if you want to run reproduction on other models, you should firstly run the following code to convert your downlaoded LLAMA model

```
cd transformers
python3 src/transformers/models/llama/convert_llama_weights_to_hf.py \
    --input_dir ./Llama \
    --model_size 30b \ # this is the model size you want to specify
    --output_dir ./Llama/converted/ # this is the output converted model
```

# Then run the script on Bunya:
Note: the path of model is ./llama/converted/llama-7b/
```
 sbatch run_reproduce.sh
 
```

# To inference on Bunya, run the following:


```
 python3 run_inference.py --input_model ./output/llama-7b/ 
```




