import os
import sqlite3
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs.db")


def run(sql, params=()):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(sql, params)
    conn.commit()
    rows = cur.fetchall()
    new_id = cur.lastrowid
    conn.close()
    return rows, new_id


run("""CREATE TABLE IF NOT EXISTS documents (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           company TEXT NOT NULL,
           heading TEXT NOT NULL,
           text TEXT NOT NULL)""")


class Document(BaseModel):
    company: str
    heading: str
    text: str


def get_or_404(doc_id):
    rows, _ = run("SELECT * FROM documents WHERE id = ?", (doc_id,))
    if len(rows) == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    return dict(rows[0])


@app.post("/documents", status_code=201)
def create_document(doc: Document):
    _, new_id = run(
        "INSERT INTO documents (company, heading, text) VALUES (?, ?, ?)",
        (doc.company, doc.heading, doc.text),
    )
    return get_or_404(new_id)


@app.get("/documents")
def get_documents(company: Optional[str] = None):
    if company:
        rows, _ = run("SELECT * FROM documents WHERE company = ? ORDER BY id", (company,))
    else:
        rows, _ = run("SELECT * FROM documents ORDER BY id")
    return [dict(r) for r in rows]


@app.get("/documents/{doc_id}")
def get_document(doc_id: int):
    return get_or_404(doc_id)


@app.put("/documents/{doc_id}")
def update_document(doc_id: int, doc: Document):
    get_or_404(doc_id)
    run(
        "UPDATE documents SET company = ?, heading = ?, text = ? WHERE id = ?",
        (doc.company, doc.heading, doc.text, doc_id),
    )
    return get_or_404(doc_id)


@app.delete("/documents/{doc_id}")
def delete_document(doc_id: int):
    get_or_404(doc_id)
    run("DELETE FROM documents WHERE id = ?", (doc_id,))
    return {"message": "Document deleted"}
