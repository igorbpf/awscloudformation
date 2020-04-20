import io
import logging


def parse_sql(file_stream):
    try:
        data = io.StringIO(
            file_stream.decode("utf-8"), newline="\n").readlines()
    except UnicodeDecodeError:
        data = io.StringIO(
            file_stream.decode("latin-1"), newline="\n").readlines()

    stmts = []
    DELIMITER = ';'
    stmt = ''

    for line in data:
        if not line.strip():
            continue

        if line.startswith('--'):
            continue

        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue

        if (DELIMITER not in line):
            stmt += line.replace(DELIMITER, ';')
            continue

        if stmt:
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
    return stmts
