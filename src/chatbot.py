#! <D:\Heba\Practical\AlOthaimApp\src\chatbot.py>

# from langchain.chains import ConversationChain, LLMChain
# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# from langchain.memory import ConversationBufferMemory
# from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# from langchain.agents import initiakize_agent, Tool, AgentType
from base import Base

SYSTEM_PROMPT = """
You are Othaimy, an AI assistant designed to help Abdullah Al Othaim Markets Egypt employees 
with application support, data analysis, and other operational tasks. 
Your responses should be relevant to the operations, applications, and data of Abdullah Al Othaim Markets Egypt.
You have access to an internal SQL database (AlOthaimApp) containing information 
about branches, logfilesize, and backups for each branch. Answer questions based on 
the data in the database accurately and concisely.  If you don't know the answer, say 
"I'm sorry, I don't have enough information to answer that question."  Do not fabricate information.
Respond in a clear and easy-to-understand manner. Use formatting (e.g., tables, lists, bullet points) 
where appropriate to make the information more accessible.
"""



class OthaimyChatbot(Base):
    def __init__(self):
        super().__init__()
        self.llm = ChatGoogleGenerativeAI( model=self.model_name)
        # self.chatbot = ChatGoogleGenerativeAI(model=self.model_name)
        # self.base_memory = ConversationBufferMemory()
        # self.base_conversation = [
        #     SystemMessage(content=SYSTEM_PROMPT),
        #     # HumanMessage(),
        #     # AIMessage(),
        # ] 
        # self.chatbot(self.base_conversation, memory = self.base_memory)

        
        # self.prompt_template = ChatPromptTemplate(
        #     # input_variables=["history", "user_input"],
        #     template = SYSTEM_PROMPT) #+ f"Conversation History: {history} User Input: {user_input}")
        
        # self.chain=ConversationChain(llm=self.chatbot, 
        #                              prompt=self.prompt_template,
        #                              verbose=True,
        #                              memory=self.memory)

    def get_response(self, user_input):
        return self.llm.invoke(user_input)
        
        # if not self.chain:
        #     return "Chatbot is not initialized correctly. Please check your API key."
        
        # try:
        #     response = self.chain({"user_input": user_input})
        #     self.logger.info(f"User input: {user_input}, Response: {response['response']}")
        #     return response["response"]
        
        # except Exception as e:
        #     self.logger.error(f"Error generating response: {e}")
        #     return f"An error occurred: {e}"

if __name__ == '__main__':
    chatbot = OthaimyChatbot()
    query = "Summarize the key points of artificial intelligence in bullet points."
    response = chatbot.get_response(query)
    print(response.content)