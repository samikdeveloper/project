# Rule Automation Project

This project uses LangGraph and Groq to convert natural language rule requests into rule JSON for an IoT rule engine, then supports human approval before creating and optionally starting the rule through a backend API.

## Project Layout

```text
RuleAutomationProject/
|-- apps/
|   |-- backend_server.py
|   |-- cli.py
|   `-- streamlit_app.py
|-- scripts/
|   |-- list_models.py
|   `-- test_groq.py
|-- src/
|   `-- rule_automation/
|       |-- __init__.py
|       |-- agent_graph.py
|       |-- backend_server.py
|       |-- model_setup.py
|       `-- prompt_template.py
|-- pyproject.toml
`-- README.md
```

## Run

Install the package in editable mode:

```bash
pip install -e .
```

Create a local `.env` file from the example and set your Groq key:

```bash
copy .env.example .env
```

Start the backend:

```bash
uvicorn apps.backend_server:app --host 127.0.0.1 --port 5001 --reload
```

Run the CLI:

```bash
python apps/cli.py
```

Run the Streamlit app:

```bash
streamlit run apps/streamlit_app.py
```
