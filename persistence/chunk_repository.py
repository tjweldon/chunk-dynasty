from persistence import db
from chunk_dynasty.core.chunk import Chunk
import json

table_name = "chunks"
columns = ("header", "salt", "parent_header", "data")


def save(chunk: Chunk) -> None:
    columns_string = ", ".join(list(columns))
    values = [
        chunk.header.decode(),
        chunk.salt.decode(),
        chunk.parent_header.decode(),
        chunk.data.decode()
    ]
    values = map(
        lambda v: f"'{v}'",
        values
    )
    values_string = ", ".join(values)
    sql = f"INSERT INTO {table_name} ({columns_string}) VALUES ({values_string})"
    cursor = db.get_cursor()
    cursor.execute(sql)
    db.commit()


def get_by_header(header: str) -> Chunk:
    sql = f"SELECT data, parent_header, header, salt FROM chunks WHERE header = '{header}'"
    cursor = db.get_cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    row_dict = {
        "data": json.dumps(row[0]).encode(),
        "parent_header": row[1].encode(),
        "header": row[2].encode(),
        "salt": row[3].encode(),
    }
    chunk = Chunk(**row_dict)
    return chunk
