from persistence import db
from chunk_dynasty.core.chunk import Chunk

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
    print(sql)
    cursor = db.get_cursor()
    cursor.execute(sql)
    db.commit()
