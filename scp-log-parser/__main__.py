import pathlib
import sys

import psycopg2

import rounds_loader

if __name__ == "__main__":
    rounds_loader = rounds_loader.RoundsLoader(pathlib.Path(sys.argv[1]))
    rounds = rounds_loader.load()

    conn = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    cur.execute("TRUNCATE round CASCADE")
    conn.commit()

    for rnd in rounds:
        rnd.export(cur)
        conn.commit()

    cur.close()
    conn.close()
