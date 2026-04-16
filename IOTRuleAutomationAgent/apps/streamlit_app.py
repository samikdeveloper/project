import streamlit as st

from rule_automation.agent_graph import build_graph


graph = build_graph()

st.title("Agentic AI Rule Management")

user_input = st.text_area("Enter your natural language rule:", height=150)

if st.button("Generate Rule"):
    if not user_input.strip():
        st.warning("Please enter a natural language rule description.")
    else:
        final_state = graph.invoke({"user_input": user_input})

        st.subheader("Generated Rule JSON")
        st.json(final_state.get("rule_json", {}))

        st.subheader("HITL Approval")
        approve = st.radio("Do you approve this rule?", ("Yes", "No"))

        if approve == "Yes":
            result = final_state.get("result", {})
            st.success(result.get("message", "Rule approved and started!"))
        else:
            st.error("Rule was rejected by human validator.")
