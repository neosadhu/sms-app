from db.dao import PostgresDAO
import os



with open('db/queries/insert_message.sql', 'r') as f:
    insert_query = f.read()
with open('db/queries/select_message.sql', 'r') as f:
    select_message_query = f.read()
with open('db/queries/select_messages.sql', 'r') as f:
    select_messages_query = f.read()    
with open('db/queries/remove_message.sql', 'r') as f:
    remove_message_query = f.read()    

def connect_to_db():
    HOST=os.getenv("HOST") or "localhost"
    USER=os.getenv("USER") or "bipop"
    PASSWORD=os.getenv("PASSWORD") or ''
    DATABASE=os.getenv("DATABASE") or "postgres"
    client = PostgresDAO(host=HOST, port=5432, database=DATABASE, user=USER, password=PASSWORD)
    return client

def add_message(dbClient:PostgresDAO, message_id:str, message:str):
    dbClient.execute_query(query=insert_query,params=(message_id,message))    

def remove_message(dbClient:PostgresDAO, message_id:str):
    dbClient.execute_query(query=remove_message_query,params=(message_id,))

def get_message(dbClient:PostgresDAO, message_id:str):
    return dbClient.execute_query(query=select_message_query, params=(message_id,))
    
def get_messages(dbClient:PostgresDAO):
    return dbClient.execute_query(query=select_messages_query)




