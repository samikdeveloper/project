from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI(title="Rule Management Service")

rules_store = {}
rule_id_counter = 1


class Rule(BaseModel):
    rule_name: str
    description: str
    input_topic: str
    condition: str
    action_message: str
    output_topic: str


@app.get("/")
def root():
    return {"message": "Backend service is running!"}


@app.get("/rules/list")
def list_all_rules():
    return list(rules_store.values())


@app.post("/rules/create")
def create_rule(rule: Rule):
    global rule_id_counter

    rule_id = str(rule_id_counter)
    rule_id_counter += 1

    rule_data = rule.dict()
    rule_data["status"] = "Created"
    rule_data["id"] = rule_id

    rules_store[rule_id] = rule_data

    return JSONResponse(
        content={
            "rule_id": rule_id,
            "message": "Rule created successfully"
        },
        status_code=201
    )


@app.get("/rules/{rule_id}")
def describe_rule(rule_id: int):
    rule_id_str = str(rule_id)
    if rule_id_str not in rules_store:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rules_store[rule_id_str]


@app.post("/rules/{rule_id}/start")
def start_rule(rule_id: int):
    rule_id_str = str(rule_id)
    if rule_id_str not in rules_store:
        raise HTTPException(status_code=404, detail="Rule not found")

    rules_store[rule_id_str]["status"] = "Running"
    return {"message": f"Rule id: {rule_id} started successfully!"}


@app.post("/rules/{rule_id}/stop")
def stop_rule(rule_id: int):
    rule_id_str = str(rule_id)
    if rule_id_str not in rules_store:
        raise HTTPException(status_code=404, detail="Rule not found")

    rules_store[rule_id_str]["status"] = "Stopped"
    return {"message": f"Rule {rule_id} stopped successfully!"}


@app.delete("/rules/{rule_id}/delete")
def delete_rule(rule_id: int):
    rule_id_str = str(rule_id)
    if rule_id_str not in rules_store:
        raise HTTPException(status_code=404, detail="Rule not found")

    del rules_store[rule_id_str]
    return {"message": f"Rule {rule_id} deleted successfully!"}
