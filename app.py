from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import uvicorn

app = FastAPI()
llm = Llama(
    model_path="./Phi-3-mini-4k-instruct-q4.gguf",  # path to GGUF file
    n_gpu_layers=-1, # The number of layers to offload to GPU, if you have GPU acceleration available. Set to 0 if no GPU acceleration is available on your system.
    n_threads=5,
    n_threads_batch=5
)

class RequestModel(BaseModel):
    prompt: str

@app.post("/v1/completions")
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