<h1>Model Proformance / Latency Test</h1>
Tested performance of inference model to make additional inference layer by providing custom model using llama.cpp</br></br>
<h3>Test Environment</h3>
- Platform: Google Cloud Platform(GCP): VM Instance
- Instance:
-- Instance Type: n1-standard-4
-- CPU Platform: Intel Skylake
-- CPU & Mem. Resources: 4vCPU, 15GM Mem.
-- GPU: 1 x NVIDIA T4</br>
<h3>Hugging Face Model Repository</h3>
Model Name: microsoft/Phi-3-mini-4k-instruct-gguf </br>
https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf</br></br>
<h3>How to install model</h3>
1. Install Hugging Face CLI:
`pip install huggingface-hub>=0.17.1`
2. Login to Hugging Face:
`huggingface-cli login`
3. Download the GGUF model:
`huggingface-cli download microsoft/Phi-3-mini-4k-instruct-gguf Phi-3-mini-4k-instruct-q4.gguf --local-dir . --local-dir-use-symlinks False`
<h3>How to use model in Python</h3>
1. Install llama.cpp-python
`! CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python`
2. Run the model (Test model with below demo project code)
```python
from llama_cpp import Llama


llm = Llama(
  model_path="./Phi-3-mini-4k-instruct-q4.gguf",  # path to GGUF file
  n_ctx=4096,  # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=8, # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=35, # The number of layers to offload to GPU, if you have GPU acceleration available. Set to 0 if no GPU acceleration is available on your system.
)

prompt = "How to explain Internet to a medieval knight?"

# Simple inference example
output = llm(
  f"<|user|>\n{prompt}<|end|>\n<|assistant|>",
  max_tokens=256,  # Generate up to 256 tokens
  stop=["<|end|>"], 
  echo=True,  # Whether to echo the prompt
)

print(output['choices'][0]['text'])
```