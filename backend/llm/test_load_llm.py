from .loadllm import llm_call


user_input = "Help me with 3 plus 2 then divide by 5\n"
#user_input ="tell me about the latest research paper on ai/ml"
#user_input = "what is the capital of France?"
#user_input = "what is the largest planet in our solar system?"

system_instruction = (
    """ You are an AI assistant. If the user's question can be answered by searching arXiv or doing thrugh a math formular, follow these two rules.
    Otherwise, reply with a normal text answer NOT JSON OBJECT.
    Rule1: For example user asked '3 multiply 7', then <MATH EXPRESSION> is 3*7.
    Rule2: User's answer can be searching arXiv, for example: 'quantum entanglement', then <arxiv_query> is 'quantum entanglement'.
    Here is the JSON object you should return:
    {"function": "calculate", "arguments": {"expression": "<MATH EXPRESSION>"}
    or
    {"function": "search_arxiv", "arguments": {"query": "<arxiv_query>"}
    Respond ONLY with a JSON object in the following format, do NOT add any explanations or code
    """
)
prompt = f"{system_instruction}\nuser: {user_input}\nassistant: "

# 调用 LLM
response = llm_call(prompt, max_new_tokens=100)
print("RAW LLM response:", response)
print(isinstance(response, str))

