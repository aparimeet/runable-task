import json
import os

CONTEXT_FILE = "context.json"

def get_context():
    if not os.path.exists(CONTEXT_FILE):
        return {"summary": "", "plan": "", "history": []}
    with open(CONTEXT_FILE, "r") as f:
        return json.load(f)

def save_context(context):
    with open(CONTEXT_FILE, "w") as f:
        json.dump(context, f, indent=2)

def update_history(action, result):
    context = get_context()
    context["history"].append({"action": action, "result": result})
    # Simple pruning: keep the last 10 interactions
    if len(context["history"]) > 10:
        context["history"] = context["history"][-10:]
    save_context(context)

def set_plan(plan):
    context = get_context()
    context["plan"] = plan
    save_context(context)

def set_summary(summary):
    context = get_context()
    context["summary"] = summary
    save_context(context) 