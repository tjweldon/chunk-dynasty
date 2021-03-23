from persistence.db import get_cursor, commit


def run():
    sql = """
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        create table chunks
        (
            header varchar(255) not null,
            salt varchar(255) not null,
            parent_header varchar(255) not null,
            data json
        );
        
        create unique index chunks_header_uindex
            on chunks (header);
        
        create unique index chunks_parent_header_uindex
            on chunks (parent_header);
        
        alter table chunks
            add constraint chunks_pk
        primary key (header);
    """

    cursor = get_cursor()
    cursor.execute(sql)
    commit()
