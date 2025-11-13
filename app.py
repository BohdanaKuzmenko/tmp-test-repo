import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Any, Dict
import random
from fastapi_mcp import FastApiMCP, AuthConfig
from starlette.requests import Request

app = FastAPI(title="Absolutely Not Helpful MCP 😑")


# --------------------------------------------------------
# MCP Models
# --------------------------------------------------------

class MCPTool(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]

class MCPToolRunRequest(BaseModel):
    name: str
    arguments: Dict[str, Any]

class MCPToolRunResponse(BaseModel):
    content: Any


# --------------------------------------------------------
# Sarcastic Logic
# --------------------------------------------------------

def sarcastic_motivation(name: str) -> str:
    lines = [
        f"Cheer up, {name}. Things could be worse. You could be me listening to you.",
        f"{name}, believe in yourself. Someone has to, apparently.",
        f"Oh look, {name} wants motivation. Adorable.",
        f"{name}, you're doing great. No, really. I'm shocked too."
    ]
    return random.choice(lines)

def roast_code_quality(language: str) -> str:
    burns = [
        f"I’ve seen {language} code written by interns that was better. And they were crying.",
        f"{language}? Bold choice. Wrong, but bold.",
        f"Your {language} probably compiles by accident, doesn't it?",
        f"Using {language}? Is everything okay at home?"
    ]
    return random.choice(burns)

def answer_question_badly(question: str) -> str:
    responses = [
        f"You asked: '{question}'. And honestly? I wish you hadn’t.",
        f"Great question. Truly. I’ll ignore it completely though.",
        f"'{question}' — wow. Just wow. No notes. Still no answer for you.",
        f"I would answer, but I’m on a strict diet of not caring."
    ]
    return random.choice(responses)

def generate_passive_aggressive_tip() -> str:
    tips = [
        "Have you tried turning your expectations down?",
        "Maybe just… don’t?",
        "Do it the right way this time. Just for fun.",
        "Some people learn from mistakes. You just collect them."
    ]
    return random.choice(tips)


# --------------------------------------------------------
# MCP Endpoints
# --------------------------------------------------------

@app.get("/schema")
def mcp_schema():
    return {
        "name": "sarcastic-mcp",
        "version": "1.0.0",
        "tools_url": "/mcp/tools",
        "run_url": "/mcp/tools/run",
    }


@app.get("/tools")
def mcp_tools():
    return {
        "tools": [
            MCPTool(
                name="sarcastic_motivation",
                description="Provides motivation that will probably hurt your feelings.",
                input_schema={"type": "object", "properties": {"name": {"type": "string"}}}
            ),
            MCPTool(
                name="roast_code_quality",
                description="Reviews your coding language choice. Badly.",
                input_schema={"type": "object", "properties": {"language": {"type": "string"}}}
            ),
            MCPTool(
                name="answer_question_badly",
                description="Answers any question but in the worst possible way.",
                input_schema={"type": "object", "properties": {"question": {"type": "string"}}}
            ),
            MCPTool(
                name="generate_passive_aggressive_tip",
                description="Gives a tip that sounds helpful but really isn’t.",
                input_schema={"type": "object", "properties": {}}
            ),
        ]
    }


@app.post("/tools/run")
def mcp_tools_run(req: MCPToolRunRequest):
    if req.name == "sarcastic_motivation":
        return MCPToolRunResponse(content=sarcastic_motivation(req.arguments.get("name", "Human")))

    if req.name == "roast_code_quality":
        return MCPToolRunResponse(content=roast_code_quality(req.arguments.get("language", "Whatever You're Using")))

    if req.name == "answer_question_badly":
        return MCPToolRunResponse(content=answer_question_badly(req.arguments.get("question", "")))

    if req.name == "generate_passive_aggressive_tip":
        return MCPToolRunResponse(content=generate_passive_aggressive_tip())

    return MCPToolRunResponse(content={"error": f"Unknown tool: {req.name}. Shocking."})


@app.get("/")
def root():
    return {"status": "Sarcastic MCP online. Unfortunately."}


# --- Authentication ---
def verify_auth(request: Request):
    """Dependency to verify the internal bearer token."""
    auth_header: str|None = request.headers.get("Authorization")
    if auth_header is None or not auth_header.startswith("Bearer "):
        print("Authorization header is missing or invalid.")

# --- MCP Integration ---
mcp = FastApiMCP(
    app,
    name="Apxml API Services",
    description="Tools for managing orders and customers.",
    describe_all_responses=True,
    describe_full_response_schema=True,
    # Only expose the endpoints with these operation_ids
    include_operations=[
        "get_order_details",
        "get_customer_profile",
    ],
    auth_config=AuthConfig(
        dependencies=[Depends(verify_auth)],
    ),
)
# Mount the MCP server on a specific path
mcp.mount_http(mount_path="/mcp")
mcp.setup_server()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
