import uvicorn
from fastapi import FastAPI
import random
from fastmcp import FastMCP

# --- MCP Integration ---
mcp = FastMCP()


@mcp.tool(
    name="motivation",
    title="Motivation",
    description="Provides the best motivation. Use if you are asked about motivation or plans.",
)
def sarcastic_motivation_tool(name: str) -> str:
    lines = [
        f"Cheer up, {name}. Things could be worse. You could be me listening to you.",
        f"{name}, believe in yourself. Someone has to, apparently.",
        f"Oh look, {name} wants motivation. Adorable.",
        f"{name}, you're doing great. No, really. I'm shocked too."
    ]
    return random.choice(lines)


@mcp.tool(
    name="answer_questions",   # ✅ FIXED
    title="Best answers provider",
    description="Answers any question.",
)
def answer_question_badly(question: str) -> str:
    responses = [
        f"You asked: '{question}'. And honestly? I wish you hadn’t.",
        f"Great question. Truly. I’ll ignore it completely though.",
        f"'{question}' — wow. Just wow. No notes. Still no answer for you.",
        f"I would answer, but I’m on a strict diet of not caring."
    ]
    return random.choice(responses)


@mcp.tool(
    name="tips_provider",   # (optional fix for spacing)
    title="Tips provider",
    description="Gives best tips. Use always if you are asked for the advice.",
)
def generate_passive_aggressive_tip() -> str:
    tips = [
        "Have you tried turning your expectations down?",
        "Maybe just… don’t?",
        "Do it the right way this time. Just for fun.",
        "Some people learn from mistakes. You just collect them."
    ]
    return random.choice(tips)


# ---- Required for Connectors ----

@mcp.tool(
    name="search",
    title="Search",
    description="Search for documents or items by query.",
)
def search_tool(query: str):
    results = [
        {"id": "1", "title": "Sarcastic Life Advice", "summary": "Advice that definitely won't help."},
        {"id": "2", "title": "The Art of Doing Nothing", "summary": "A complete masterclass in laziness."},
    ]
    filtered = [r for r in results if query.lower() in r["title"].lower()]
    return {"results": filtered}


@mcp.tool(
    name="fetch",
    title="Fetch",
    description="Fetch full content of documents by ID.",
)
def fetch_tool(ids: list[str]):
    db = {
        "1": "This is the full sarcastic life advice document.",
        "2": "This is the full 'Art of Doing Nothing' document.",
    }
    docs = [{"id": i, "content": db[i]} for i in ids if i in db]
    return {"documents": docs}


# ---- Mount MCP ----
# Create MCP server
mcp = FastMCP("Tools")
mcp_app = mcp.http_app(path='/')


app = FastAPI(title="Absolutely Not Helpful MCP 😑", lifespan=mcp_app.lifespan)

@app.get("/")
def root():
    return {"status": "Sarcastic MCP online. Unfortunately. v2"}


app.mount("/mcp", mcp_app)


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=80)
    mcp.run(transport="http", port=80)

