import streamlit as st
from main import Assistant

assistant = Assistant()

st.title("Expert Finder")

user_question = st.text_input("Enter your query (e.g., 'Find me Reinforcement Learning experts in Amsterdam'): ")
num_experts = st.slider("Number of experts:", 1, 10, 5)

if st.button("Search"):
    query = assistant.get_search_query(user_question)
    st.write(f"Generated Search Query: **{query}**")

    search_response = assistant.metaphor.search(query, use_autoprompt=True, num_results=num_experts)
    results = search_response.get_contents().contents

    for result in results:
        expert_info = assistant.get_expert_from_html(result.extract)
        if expert_info:
            with st.container():
                st.write(f"**Name:** {expert_info.name}")
                st.write(f"**Affiliation:** {expert_info.affiliation}")
                st.write(f"**Location:** {expert_info.location}")
                st.write(f"**URL:** {result.url}")
                st.write(f"**Summary:** {expert_info.summary}")

                if expert_info.socials:
                    socials = expert_info.socials
                    st.write("Socials:")
                    for key, value in socials.items():
                        if value:
                            st.write(f"  **{key.capitalize()}:** {value}")

            st.markdown("---")  # Horizontal line separator
