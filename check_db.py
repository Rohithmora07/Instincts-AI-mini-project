import sqlite3

with sqlite3.connect("instincts_ai.db") as conn:
    rows = conn.execute("SELECT id, plan_id, milestone_text, status FROM checkpoints").fetchall()
    for row in rows:
        print(row)