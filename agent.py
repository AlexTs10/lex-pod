from langchain.document_loaders import TextLoader
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
import pinecone 
import os 
from dotenv import load_dotenv

load_dotenv()

pinecone.init(
    api_key=os.environ.get('PINECONE_API_KEY'),  # find at app.pinecone.io
    environment=os.environ.get('PINECONE_LOCATION')  # next to api key in console
)
index_name = "lex-pod"

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
docsearch = Pinecone.from_existing_index("lex-pod", embeddings)
llm = ChatOpenAI(
    #temperature=1.0,
    model_name='gpt-3.5-turbo'
)
retriever = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever()
)
tool_desc = """Use this tool to answer user questions using Lex Fridman podcasts. If the user states 'ask Lex' use this tool to get the answer. This tool can also be used for follow up questions from the user."""
tools = [Tool(
    func=retriever.run,
    description=tool_desc,
    name='Lex Friedman DB'
)]
memory = ConversationBufferWindowMemory(
    memory_key="chat_history", # important to align with agent prompt (below)
    k=5,
    return_messages=True
)
sys_msg =  """You are a helpful chatbot that answers the user's questions."""

    ## configs 
conversational_agent = initialize_agent(
        agent='chat-conversational-react-description',
        tools=tools,
        llm=llm,
        verbose=True,
        #max_iterations=10,
        early_stopping_method="generate",
        memory=memory,
        )
prompt = conversational_agent.agent.create_prompt(
        system_message=sys_msg,
        tools=tools
    )
conversational_agent.agent.llm_chain.prompt = prompt
    ###