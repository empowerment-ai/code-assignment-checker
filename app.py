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
        st.markdown("""
        # AI-based Programming Assignment Reviewer

        Welcome to this AI-powered tool designed to assist educators in evaluating general programming assignments. This application utilizes the capabilities of [LangChain](https://github.com/LangChain/langchain) and [OpenAI](https://openai.com) to automate the review process of student submissions, helping to ensure consistency and efficiency in assessment. This tool currently requires a OpenAI API Key, which can be obtained using the provided link.   While it is not free, the OpenAI models provide the best results and overall the [cost](https://openai.com/pricing#language-models) per check is minimal.  Rever to the OpenAI website for details.

        ## How it Works
        The tool parses the student submissions and uses AI to run tests and evaluate the code quality against specified criteria. By integrating LangChain and OpenAI, we can leverage advanced natural language processing to interpret the code's intent and provide detailed feedback.

        ## Features
        - **Automated Code Execution**: Run student programs safely in an isolated environment.
        - **Code Quality Analysis**: Evaluate code for best practices and adherence to programming standards.
        - **Feedback Generation**: Automatically generate constructive feedback based on the code analysis.

        ## Get Started
        To begin, simply review or tweak the AI instructions, copy/paste your assignment instructions, and an individual student's coding submission. Once you are done, you can click the Check button to match the submission against the instructions.

        ## Caveats
        This does not replace the need to review the student's work.  While the plan is to improve this tool, AI will generate hallucination. You may need to tweak the AI instructions to improve the generated feedback.        

        ## Useful Links
        - [Streamlit Documentation](https://docs.streamlit.io)
        - [OpenAI API Documentation](https://beta.openai.com/docs/)
        - [LangChain API Documentation](https://python.langchain.com/docs/get_started/introduction)
        - [Source Code](https://github.com/empowerment-ai/code-assignment-checker)
        
        Feel free to explore the code and contribute to the project. Your feedback and contributions are most welcome!

        ---
    """)


if __name__ == '__main__':
    st.set_page_config(page_title="Coding Assignment Checker")
    st.header('🦜🔗 Coding Assignment Checker')
    tab0, tab1, tab2, tab3 = st.tabs(["Introduction", "AI Instructions", "Assignment Instructions", "Submission Details"])
    app_intro()

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

public class HelloWorld {
    public static void main(String[] args) {
        // Print "Hello, World!" to the console
        System.out.println("Hello, World!");
    }
}

    """



    with st.form('my_form'):

        with tab1:
            ai_review_instructions =st.text_area("AI Instructions", ai, height=500)
        with tab2:
            instructions=st.text_area("Assignment Instructions", sample_instruction, height=500)
        with tab3:
            submission = st.text_area("Student Submission:", sample_submission, height=500)

        if not (openai_api_key or openai_api_key.startswith('sk-')):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
            st.session_state.disabled = True
        submitted = st.form_submit_button('Check', disabled=st.session_state.disabled)
        
        if submitted and openai_api_key.startswith('sk-'):
            with get_openai_callback() as cb:

                model = st.sidebar.selectbox('Select Model:', ['gpt-3.5-turbo', 'gpt-4'])
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

