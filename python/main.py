import os
import yaml
import uuid
import aiosqlite
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html

# --- CẤU HÌNH ĐƯỜNG DẪN ---
DB_PATH = "sns_api.db"
# Tìm file openapi.yaml ở thư mục gốc
OPENAPI_PATH = Path(__file__).parent.parent / "openapi.yaml"

if not OPENAPI_PATH.exists():
    OPENAPI_PATH = Path(__file__).parent / "openapi.yaml"

# Nạp file đặc tả OpenAPI
with open(OPENAPI_PATH.resolve(), encoding="utf-8") as f:
    openapi_yaml = yaml.safe_load(f)

app = FastAPI(title="Contoso Social API", openapi_url="/openapi.json")

# --- CẤU HÌNH CORS (Cho phép React từ cổng 3000 truy cập) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- KHỞI TẠO DATABASE ---
@app.on_event("startup")
async def startup_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # Tạo bảng Sản phẩm
        await db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                createdAt TEXT NOT NULL
            )
        """)
        # Tạo bảng Bài đăng (Posts)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                createdAt TEXT NOT NULL,
                likesCount INTEGER DEFAULT 0
            )
        """)
        await db.commit()
    app.openapi_schema = openapi_yaml

# --- ENDPOINTS CHO PRODUCTS ---
@app.get("/products", tags=["Products"])
async def get_products():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM products")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

@app.post("/products", status_code=201, tags=["Products"])
async def create_product(product: dict):
    product_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat() + "Z"
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO products (id, name, description, price, createdAt) VALUES (?, ?, ?, ?, ?)",
            (product_id, product['name'], product.get('description', ''), product['price'], created_at)
        )
        await db.commit()
    return {"id": product_id, **product, "createdAt": created_at}

# --- ENDPOINTS CHO POSTS (Dùng cho React Frontend) ---
@app.get("/posts", tags=["Posts"])
async def get_posts():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM posts ORDER BY createdAt DESC")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

@app.post("/posts", status_code=201, tags=["Posts"])
async def create_post(post: dict):
    post_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat() + "Z"
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO posts (id, username, content, createdAt) VALUES (?, ?, ?, ?)",
            (post_id, post['username'], post['content'], created_at)
        )
        await db.commit()
    return {"id": post_id, **post, "createdAt": created_at}

# --- KHỞI CHẠY SERVER ---
if __name__ == "__main__":
    import uvicorn
    print("Đang khởi động Server tại cổng 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)