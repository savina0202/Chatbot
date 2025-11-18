import json
#from tools.tools import call_tool, tool_list


def search_arxiv(query: str) -> str:
    """
    Simulate an arXiv search or return a dummy passage for the given query.
    In a real system, this might query the arXiv API and extract a summary.
    """
    # Example placeholder implementation:
    return f"[arXiv snippet related to '{query}']"

def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression and return the result as a string.
    """
    print(expression)
    try:
        from sympy import sympify
        result = sympify(expression)  # use sympy for safe evaluation
        return str(result)
    except Exception as e:
        return f"Error: {e}"
    
tool_list={"search_arxiv":search_arxiv,
           "calculate":calculate
           }

def call_tool(tool_name, args):
    if tool_name in tool_list:
        try:
            return tool_list[tool_name](args)
        except Exception as e:
            return f"Error calling '{tool_name}': {e}"
    else:
        return f"Error: Unknown tool '{tool_name}'"

def is_valid_json(txt):
    try:
        return json.loads(txt.strip())

    except Exception:
        return None

def route_llm_output(llm_text):
    try:
        print(f"LLM Output: {llm_text}\n")
        data = is_valid_json(llm_text)
        if not data:
            return f"{llm_text}", None
        func = data.get("function")
        args = data.get("arguments", {})
        if func not in tool_list:
            return f"Function '{func}' is not available.", None
        result = call_tool(func, args)
        return result, func
    except Exception as e:
        return f"Error: {e}", None


# llm_text='{"function": "calculate", "arguments": {"expression": "1/2"}}'
#llm_text='{"function": "search_arxiv", "arguments": {"query": "artificial intelligence machine learning"}}'
#llm_text='Paris'
# print(route_llm_output(llm_text))

