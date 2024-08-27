from sqlalchemy import create_engine, text

DATABASE_URL = "sqlite:///instance/sendit.db"
engine = create_engine(DATABASE_URL)

table_name = "myorders"
column_name = "parcel_id"

sql_command = f'ALTER TABLE {table_name} DROP COLUMN {column_name}'

with engine.connect() as connection:
    connection.execute(text(sql_command))

print("Column removed successfully.")