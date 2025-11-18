# AI Voice Chat Agent Enhancement



## 🎯 Technical Objectives

1. Function Calling with LLM: Using function/tool calling by prompting OpenAI to output structured JSON calls for external functions



2. Intent Parsing and Tool Mapping: Parsing user queries to determine the intent(e.g., perform a mathematical calculation or perform an API query). 



## 🚀 Technical Design

**Tool Functions：** Implement two helper functions:



 * `search_arxiv(query: str) -> str`: Simulates or performs an arXiv search and returns a relevant passage or summary for the query.

  * `calculate(expression: str) -> str`: Evaluates a mathematical expression (using `sympy` or `eval`) and returns the result as text.



* **Prompt Engineering:** Modify the Llama 3 system/user prompts so the model knows to generate structured function-call outputs when appropriate. For example, instruct it that if the user’s question can be answered by searching arXiv or doing math, it should output a JSON-like call, such as:



  ```json

  {"function": "calculate", "arguments": {"expression": "2+2"}}

  ```



  or



  ```json

  {"function": "search_arxiv", "arguments": {"query": "quantum entanglement"}}

  ```



  Otherwise, it should respond normally in text.



  * **Detecting and Calling Tools:** After the LLM generates a response, check if it is a function call. Parse the JSON output from the LLM to extract the function name and arguments. If it is a call, invoke the corresponding Python function (`search_arxiv` or `calculate`) with those arguments and capture its result. Use this result as the assistant’s reply (to be spoken by TTS). If the LLM output is normal text, just use it as the assistant’s response without calling any function.



  * **Fallback Behavior:** Ensure the voice agent handles all cases. If the LLM’s output cannot be parsed as a function call (or if the named function is unknown), fall back to replying with a standard text response or an error message as appropriate.



  * **Logging:** Logging the backend user/system prompts and the assistant’s respopnse 

  

  * **Enhancing API:** Endpoint /voice-query and /chathist support these technical changes

## Demo

https://github.com/user-attachments/assets/76839271-e3c7-4cbe-9695-11f49a273e44


**Frontend UI：**


<img width="1494" height="614" alt="ChatBot" src="https://github.com/user-attachments/assets/c3e10890-023f-4717-99c9-e92c1b64d467" />
  
## Deployment

To deploy this project: git clone it first, then:

```bash
  pip install -r reqirement.txt
```
Create and config .env file in the root path. Then, add your OPENAI_API_KEY or Hugging Face Token by following the below template:

```bash
HF_Token=<your token>
OPENAI_API_KEY=<your key>
```
For model you would like to use, you can specify in .env or in config.py

Startup the backend service:
```bash
cd backend
python main.py
```

Startup the frontend:
```bash
cd frontend 
gradio voice_chat_app.py
```
- Frontend will be available at: `http://localhost:7860`
- Backend API should be running at: `http://localhost:8002`




