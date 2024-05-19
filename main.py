import os
import asyncio
from AsyncHttpRequest import Request
from ExecutionTime import AsyncExecutionTime
from dotenv import load_dotenv

load_dotenv()

iteration = 1
request_url = "http://{domain}{endpoint}".format(
    domain=os.environ.get("DOMAIN"),
    endpoint=os.environ.get("ENDPOINT")
)
prompt_file = open("./prompt.md", "r")

# Classification Task (500 Tokens)
prompt = prompt_file.read()

@AsyncExecutionTime("Inference Processing")
async def request():
    response = await Request.post(
        url=request_url,
        headers={
            "Content-type": "application/json"
        },
        data={
            "prompt": prompt
        }
    )
    return response.json()["choices"][0]["text"]

@AsyncExecutionTime("Total Inference Execution Time")
async def main():
    task = []
    for _ in range(iteration):
        task.append(asyncio.create_task(request()))
    response = await asyncio.gather(*task)
    print(response)

prompt_file.close()

asyncio.run(main())