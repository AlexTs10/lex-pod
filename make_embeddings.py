from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.vectorstores import Pinecone
import pinecone
import os 

os.environ['OPENAI_API_KEY'] = "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"

loader = DirectoryLoader('C:\\Users\\alexa\\langchain-tutorial\\lex_podcast', loader_cls=TextLoader)
docs = loader.load()
print(f'Lenght of full docs: {len(docs)}')
text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(docs)

# for debug
texts = texts[0:20]
embeddings = OpenAIEmbeddings()

pinecone.init(
    api_key="66900923-65d0-4456-8864-8ff7cf5abc81",  # find at app.pinecone.io
    environment="us-west1-gcp"  # next to api key in console
)

index_name = "lex-pod"

docsearch = Pinecone.from_documents(texts, embeddings, index_name=index_name)
print('Success!')
#db = DeepLake.from_documents(texts, embeddings)
