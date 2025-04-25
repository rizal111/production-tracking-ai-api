import os
from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine

from llama_index.core import ( SQLDatabase,VectorStoreIndex
)
from llama_index.llms.openai import OpenAI
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)
from llama_index.core.indices.struct_store.sql_query import (
    SQLTableRetrieverQueryEngine,
)

load_dotenv()
app = FastAPI(openapi_url=None,docs_url=None, redoc_url=None)

# Setup LLM
llm = OpenAI(temperature=0, model="gpt-4.1-mini")

class QueryInput(BaseModel):
    question: str

# Setup DB connection
db_uri = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(db_uri)

sql_database = SQLDatabase(
    engine,
    include_tables=["production_logs", "machines", "operators"],
)

production_logs_text = (
    "Table production_logs contains production output data.\n"
    "Columns:\n"
    "- units_produced (integer): Quantity produced by a machine during the shift.\n"
    "- machine_id (integer): Identifier of the machine, foreign key to machines.id.\n"
    "- log_date (date): Date when the production was logged.\n"
    "- shift (string): Shift during which production occurred (morning, evening, night).\n"
    "The maximum capacity per shift of a machine is stored in machines.capacity."
)

machines_text = (
    "Table machines contains machine details.\n"
    "Columns:\n"
    "- id (integer): Primary key, machine identifier.\n"
    "- name (string): Machine name, e.g., 'Cutter 01'.\n"
    "- capacity (integer): Maximum units producible per shift."
)

operators_text = (
    "Table operators contains operator details.\n"
    "Columns:\n"
    "- id (integer): Operator identifier.\n"
    "- name (string): Operator's name.\n"
    "- employee_id (string): Employee ID."
)

table_node_mapping = SQLTableNodeMapping(sql_database)
table_schema_objs = [
    (SQLTableSchema(table_name="production_logs", context_str=production_logs_text)),
    (SQLTableSchema(table_name="machines", context_str=machines_text)),
    (SQLTableSchema(table_name="operators", context_str=operators_text))
]


obj_index = ObjectIndex.from_objects(
    table_schema_objs,
    table_node_mapping,
    VectorStoreIndex
)

query_engine = SQLTableRetrieverQueryEngine(
    sql_database, obj_index.as_retriever(similarity_top_k=1), llm=llm
)


malaysia_context = """
You have access to three tables: production_logs, machines, and operators.
each day have 3 shift for each machine.
The production_logs.log_date column stores production date record as DATE in Malaysia local time.
Use column 'units_produced' for output.
Answer all queries assuming Malaysia local dates.
Answer in English.
"""

@app.post("/ask")
def ask(input: QueryInput):
    response = query_engine.query(malaysia_context + "\nQuestion: " + input.question)
    return {"answer":  str(response)}
