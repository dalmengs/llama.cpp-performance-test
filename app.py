from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import uvicorn

app = FastAPI()
llm = Llama(
    model_path="./Phi-3-mini-4k-instruct-q4.gguf",  # path to GGUF file
    n_ctx=4096,  # The max sequence length to use - note that longer sequence lengths require much more resources
    n_threads=8, # The number of CPU threads to use, tailor to your system and the resulting performance
    n_gpu_layers=35, # The number of layers to offload to GPU, if you have GPU acceleration available. Set to 0 if no GPU acceleration is available on your system.
)

class RequestModel(BaseModel):
    prompt: str

@app.post("/v1/generate")
async def generate(request: RequestModel):
    prompt = request.prompt
    output = llm(
        f"<|user|>\n{prompt}<|end|>\n<|assistant|>",
        max_tokens=256,  # Generate up to 256 tokens
        stop=["<|end|>"], 
        echo=False,  # Whether to echo the prompt
    )
    res = (output['choices'][0]['text'])
    print(res)
    return res

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )