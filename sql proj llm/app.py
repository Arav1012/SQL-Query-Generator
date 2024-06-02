import streamlit as st
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyAB194S5pGyP1-ZF5nKrQ52rhME_FbrdW4"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

def main():
    st.set_page_config(page_title="SQL Query Generator", page_icon=":robot:")
    st.markdown(
        """
        <div style="text-align:center;">
            <h1>SQL Query Generator</h1>
            <h3>I can generate SQL queries for you!</h3>
            <h4>With Explanation as well!!!</h4>
            <p>This tool is a simple tool that allows you to generate SQL Queries based on your prompts.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    text_input = st.text_area("Enter your Query here in Plain English:")

    submit = st.button('Generate SQL Query')

    if submit:
        with st.spinner("Generating SQL Query..."):
            template = """
                create a SQL query snippet using the below text:
                 
                
                    {text_input}

                
                I just want a SQL Query.
            """
            formatted_template = template.format(text_input=text_input)

            st.write(formatted_template)
            response = model.generate_content(formatted_template)
            sql_query=response.text

            sql_query=sql_query.strip().lstrip("sql").rstrip("")
            

            expected_output = """
                What would be the expected response of this SQL Query snippet:
                 
                
                    {sql_query}

                
                Provide sample tabular Response with no explanation:
            """

            expected_output_formatted = expected_output.format(sql_query=sql_query)
            eoutput=model.generate_content(expected_output_formatted)
            eoutput=eoutput.text
            

            explanation = """
                Explain this SQL Query:
                 
                
                    {sql_query}

                
                Please provide simplest of explanation.
            """
            explanation_formatted = explanation.format(sql_query=sql_query)
            explanation=model.generate_content(explanation_formatted)
            explanation=explanation.text

            with st.container():
                st.success("SQL Query Generated Successfully! Here is your Query:")
                st.code(sql_query,language="sql")
                st.success("Expected Output of this SQL Query will be:")
                st.markdown(eoutput)
                st.success("Explanation")
                st.markdown(explanation)

             
main()