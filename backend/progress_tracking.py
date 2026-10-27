import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "instincts_ai.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Create existing tables and safely add solution-attempt tracking."""
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT,
                goal TEXT,
                plan_json TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS checkpoints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_id INTEGER,
                milestone_text TEXT,
                status TEXT DEFAULT 'not_started',
                FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE CASCADE
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS solution_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                task TEXT NOT NULL,
                solution TEXT NOT NULL,
                score REAL NOT NULL CHECK(score >= 0 AND score <= 1),
                feedback TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE CASCADE
            )
        """)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_solution_submissions_plan_topic "
            "ON solution_submissions(plan_id, topic, id)"
        )


def _split_milestones(milestones_text: str) -> list[str]:
    lines = [line.strip(" -*0123456789.\t") for line in (milestones_text or "").splitlines()]
    return [line for line in lines if line]


def save_plan(profile: dict, plan: dict) -> int:
    with _connect() as conn:
        cursor = conn.execute(
            "INSERT INTO plans (created_at, goal, plan_json) VALUES (?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), profile["goal"], json.dumps(plan, ensure_ascii=False)),
        )
        plan_id = int(cursor.lastrowid)
        for milestone in _split_milestones(str(plan.get("milestones", ""))):
            conn.execute(
                "INSERT INTO checkpoints (plan_id, milestone_text) VALUES (?, ?)",
                (plan_id, milestone),
            )
        return plan_id


def plan_exists(plan_id: int) -> bool:
    with _connect() as conn:
        return conn.execute("SELECT 1 FROM plans WHERE id = ?", (plan_id,)).fetchone() is not None


def get_checkpoints(plan_id: int) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, milestone_text, status FROM checkpoints WHERE plan_id = ? ORDER BY id",
            (plan_id,),
        ).fetchall()
        return [{"id": row["id"], "text": row["milestone_text"], "status": row["status"]} for row in rows]


def update_checkpoint_status(checkpoint_id: int, status: str) -> bool:
    with _connect() as conn:
        cursor = conn.execute(
            "UPDATE checkpoints SET status = ? WHERE id = ?",
            (status, checkpoint_id),
        )
        return cursor.rowcount > 0


def get_latest_plan() -> dict | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, plan_json FROM plans ORDER BY id DESC LIMIT 1"
        ).fetchone()
        if row is None:
            return None
        return {"plan_id": row["id"], "plan": json.loads(row["plan_json"])}


def save_solution_submission(
    plan_id: int,
    topic: str,
    task: str,
    solution: str,
    score: float,
    feedback: str,
) -> dict:
    raw_score = float(score)
    if not 0.0 <= raw_score <= 1.0:
        raise ValueError("Solution score must be between 0 and 1.")
    score = round(raw_score, 2)
    # Do not let rounding turn a near-perfect attempt into a false perfect score.
    if raw_score < 1.0 and score >= 1.0:
        score = 0.99
    created_at = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        cursor = conn.execute(
            """INSERT INTO solution_submissions
               (plan_id, topic, task, solution, score, feedback, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                plan_id,
                topic.strip(),
                task.strip(),
                solution,
                score,
                feedback.strip(),
                created_at,
            ),
        )
        return {
            "submission_id": int(cursor.lastrowid),
            "plan_id": plan_id,
            "topic": topic.strip(),
            "score": score,
            "feedback": feedback.strip(),
            "created_at": created_at,
        }


def get_solution_history(plan_id: int, topic: str) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            """SELECT id, topic, task, solution, score, feedback, created_at
               FROM solution_submissions
               WHERE plan_id = ? AND topic = ? COLLATE NOCASE
               ORDER BY id ASC""",
            (plan_id, topic.strip()),
        ).fetchall()
        return [
            {
                "submission_id": row["id"],
                "topic": row["topic"],
                "task": row["task"],
                "solution": row["solution"],
                "score": row["score"],
                "percentage": round(row["score"] * 100),
                "feedback": row["feedback"],
                "created_at": row["created_at"],
                "mastered": row["score"] >= 1.0,
            }
            for row in rows
        ]


def get_solution_progress(plan_id: int) -> dict:
    """Summarize effort and best/latest correctness, not just submission counts."""
    with _connect() as conn:
        rows = conn.execute(
            """SELECT topic, score, feedback, created_at
               FROM solution_submissions
               WHERE plan_id = ?
               ORDER BY id ASC""",
            (plan_id,),
        ).fetchall()

    by_topic: dict[str, dict] = {}
    for row in rows:
        key = row["topic"].casefold()
        if key not in by_topic:
            by_topic[key] = {
                "topic": row["topic"],
                "attempt_count": 0,
                "best_score": 0.0,
                "latest_score": 0.0,
                "latest_feedback": "",
                "last_attempt_at": row["created_at"],
                "mastered": False,
            }
        item = by_topic[key]
        item["attempt_count"] += 1
        item["best_score"] = max(item["best_score"], float(row["score"]))
        item["latest_score"] = float(row["score"])
        item["latest_feedback"] = row["feedback"]
        item["last_attempt_at"] = row["created_at"]
        item["mastered"] = item["best_score"] >= 1.0

    topics = sorted(by_topic.values(), key=lambda item: item["topic"].casefold())
    return {
        "plan_id": plan_id,
        "total_topics_attempted": len(topics),
        "mastered_topics": sum(1 for item in topics if item["mastered"]),
        "total_solution_attempts": sum(item["attempt_count"] for item in topics),
        "topics": topics,
    }
