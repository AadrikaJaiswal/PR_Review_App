import streamlit as st
from PR_Review_langraph import graph

st.title("PR Review App")

pr_url = st.text_input("Enter GitHub PR Link:")

if st.button("Analyze PR"):
    if pr_url:
        with st.spinner("Analyzing PR... Please wait."):
            result = graph.invoke({"pr_url": pr_url})

        #error handling
        if "error" in result.get("pr_details", {}):
            st.error(f"{result['pr_details']['error']}")
        else:
            #PR_Summary
            st.subheader("PR Summary")
            st.write(result["summary"])

            #Issues_Detected
            st.subheader("Issues Detected")
            st.write(result["issues"] if result["issues"] else "No issues found.")

            #PR_Comments
            st.subheader("Suggested PR Comments")
            st.code(result["comments"], language="markdown")
    else:
        st.warning("Please enter a valid PR link.")