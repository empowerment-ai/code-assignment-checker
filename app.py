import streamlit as st
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback


load_dotenv()

# Streamlit block with Markdown for program introduction
def app_intro():
    with tab0:
        with open("README.md", "r") as readme_file:
            readme_contents = readme_file.read()
            st.markdown(readme_contents)

if __name__ == '__main__':
    st.set_page_config(page_title="Coding Assignment Checker")
    st.header('🦜🔗 Coding Assignment Checker')
    tab0, tab1, tab2, tab3 = st.tabs(["Introduction", "AI Instructions", "Assignment Instructions", "Submission Details"])
    app_intro()
    model = st.sidebar.selectbox('Select Model:', ['gpt-3.5-turbo', 'gpt-4'])

    if 'submit_button_state' not in st.session_state: 
        st.session_state.disabled = False

    openai_api_key_env = os.getenv('OPENAI_API_KEY')
    openai_api_key = st.sidebar.text_input('OpenAI API Key', placeholder='sk-', value=openai_api_key_env)
    url = "https://platform.openai.com/account/api-keys"
    st.sidebar.markdown("Get an Open AI Access Key [here](%s). " % url)



    review_template = """{ai}

    Assignment Instructions:
    --------------
    {instructions}
    --------------

    Determine if this submission: 
    --------------
    {submission}
    --------------
                
    """

    ai="""You are an AI Assistant who is an expert in all modern programming languages.  You are helping to grade programming assignments for a course teaching programming to college students. I want you to review the submission against the given assignment instructions to determine if the student's submission matches the assignment instructions.  You will also act as  either a compiler or intepreter for whatever language the assignment is using.  You should confirm that the program is free of syntax errors and will actually run.  I also want you to point out any logic errors and differences from what was specifically asked in the assignment instructions.  Respond back with personalized, friendly, conversational feedback to the student.  If provided, be sure to address the student by name.   If there is a rubric provided, be sure to adhere to it.   
     
    """

    sample_instruction="""Write a Java Hello World program.   Be sure to name the class HelloWorld.   The program should also include proper summary comments that include your name, course section,  instructor name, and a brief description of your program.  

Rubric: 
Summary Comments
    Name : 5 Points
    Course Section: 5 Points
    Instructor:  5 Points
    Description: 5 Points 
If Logic is correct, student gets 30 points.  But Deduct 2 Points Per Logic Error
Class name:  If the Class name is correct, student gets 20 points, but Deduct 20 points if its incorrect
Deduct 2 points per Syntax Error 
   """

    sample_submission="""
/**
 * HelloWorld.java
 * Author: Bob Smith
 * Date: October 1st, 2023
 * Course Section: ABC
 * Instructor: Professor Tom Jones
 * Description: This program demonstrates a basic "Hello, World!" program written in Java. 
 *              It simply prints the message "Hello, World!" to the console.
 */

public class HelloWorldProgram {
    public static void main(String[] args) {
        // Print "Hello, World!" to the console
        System.out.println("World!");
    }
}
"""

    with tab1:
        ai_review_instructions =st.text_area("AI Instructions", ai, height=500)
    with tab2:
        instructions=st.text_area("Assignment Instructions", sample_instruction, height=500)
    with tab3:
        submission = st.text_area("Student Submission:", sample_submission, height=500)

        with st.form('my_form'):
            if (openai_api_key == None or not openai_api_key.startswith('sk-')):
                st.warning('Please enter your OpenAI API key!', icon='⚠')
                st.session_state.disabled = True
            submitted = st.form_submit_button('Check', disabled=st.session_state.disabled)
            
            if submitted and openai_api_key.startswith('sk-'):
                with get_openai_callback() as cb:

                    with st.spinner('Working on it...'):

                        llm = ChatOpenAI(model_name=model, temperature=0.0, openai_api_key=openai_api_key)

                        review_prompt_template = PromptTemplate(
                        input_variables=["ai", "instructions", "submission", "sample_output_format"], template=review_template
                        )
                        synopsis_chain = LLMChain(
                            llm=llm, prompt=review_prompt_template, output_key="review"
                        )
                        review = synopsis_chain.run({'ai': ai_review_instructions, 'instructions': instructions,'submission': submission })
                        print(cb)
                        st.write("Assignment Feedback:")
                        st.write(review)
                        st.markdown(f"""
                                    ### Total Cost:
                                    ${cb.total_cost:,.3f}
                        """)


