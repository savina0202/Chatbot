
def search_arxiv(query: str) -> str:
    """
    Simulate an arXiv search or return a dummy passage for the given query.
    In a real system, this might query the arXiv API and extract a summary.
    """
    # Example placeholder implementation:
    print("Using search_arxiv function now ...")
    return f"[arXiv snippet related to '{query}']"

def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression and return the result as a string.
    """
    try:
        print("Using calculate function now...")
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


