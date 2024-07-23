from langchain_community.utilities import SQLDatabase
import getpass
import os
from langchain_cohere import ChatCohere
from dotenv import load_dotenv
from langchain.chains import create_sql_query_chain

db = SQLDatabase.from_uri(f'sqlite:///C:/Users/GIUSTOS/PycharmProjects/chatbot/SQL_query/sqlite/database/Chinook.db')
print(db.dialect)

print(db.get_usable_table_names())
res = db.run("SELECT * FROM Artist LIMIT 10;")


llm = ChatCohere(model="command-r", cohere_api_key="zJgq3ddpOhkyHyBkg92w9h28whjgF6dymGg8qdH2")

chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "How many employees are there"})
