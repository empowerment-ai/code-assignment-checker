# AI-based Programming Assignment Reviewer

Welcome to this AI-powered tool designed to assist educators in evaluating general programming assignments. This application utilizes the capabilities of [LangChain](https://github.com/LangChain/langchain) and [OpenAI](https://openai.com) to automate the review process of student submissions, helping to ensure consistency and efficiency in assessment. This tool currently requires a OpenAI API Key, which can be obtained using the provided link.   While it is not free, the OpenAI models provide the best results and overall the [cost](https://openai.com/pricing#language-models) per check is minimal.  Rever to the OpenAI website for details.

## How it Works
The tool parses the student submissions and uses AI to run tests and evaluate the code quality against specified criteria. By integrating LangChain and OpenAI, we can leverage advanced natural language processing to interpret the code's intent and provide detailed feedback.

## Features
- **Matching Assignment Requirements**:  Evaluate code to confirm if it matched the assignment instructions.
- **Syntax Check**: Will attempt to review the code for syntax errors. (Because this is not an actual compiler or linter, syntax checking is not always accurate. Double check the feedback)
- **Logic Check**: Will attempt to review the code for logic errors. (Watch for hallucinations)
- **Feedback Generation**: Automatically generate constructive feedback based on the code analysis.

## Get Started
To begin, simply review or tweak the AI instructions, copy/paste your assignment instructions, and an individual student's coding submission. Once you are done, you can click the Check button to match the submission against the instructions.

## Caveats
This does not replace the need for expert review of the submission.  While the plan is to improve this tool, AI will generate hallucinations from time to time. Having said that, you may need to tweak the AI instructions to improve the generated feedback.        

## Useful Links
- [Streamlit Documentation](https://docs.streamlit.io)
- [OpenAI API Documentation](https://beta.openai.com/docs/)
- [LangChain API Documentation](https://python.langchain.com/docs/get_started/introduction)
- [Source Code](https://github.com/empowerment-ai/code-assignment-checker)

Feel free to explore the code and contribute to the project. Your feedback and contributions are most welcome!

---
