# FastAPIアプリケーションのメイン設定ファイル
# ファイル監視機能と連携してOpenAPIドキュメントを自動生成する
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from .file_watcher import FileWatcher
from .openapi_generator import generate_openapi_yaml


# アプリケーションのライフサイクル管理
# アプリ起動時にファイル監視を開始し、終了時に停止する
@asynccontextmanager
async def lifespan(app: FastAPI):
    # OpenAPIドキュメント再生成関数
    def regenerate_openapi():
        generate_openapi_yaml(app, "docs/openapi.yaml")

    # srcディレクトリのファイル変更を監視
    watcher = FileWatcher(watch_paths=["src/"], callback=regenerate_openapi)

    # 初回のOpenAPIドキュメント生成
    regenerate_openapi()
    # ファイル監視をバックグラウンドで開始
    watcher.start_background()

    yield

    # アプリ終了時にファイル監視を停止
    watcher.stop()


# FastAPIアプリケーションのインスタンス作成
app = FastAPI(
    title="OpenAPI Auto Generation Sample",
    description="FastAPIでOpenAPIドキュメントを自動生成するサンプル",
    version="1.0.0",
    lifespan=lifespan,  # ライフサイクル管理を設定
)


# Pydanticモデル定義（リクエスト用）
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float


# Pydanticモデル定義（レスポンス用）
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float


# ルート（/）エンドポイント - サンプルのメッセージ返却
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


# アイテム取得エンドポイント - パスパラメータとクエリパラメータの例
@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, q: str | None = None):
    return ItemResponse(
        id=item_id,
        name=f"Item {item_id}",
        description=f"Description for item {item_id}" if q else None,
        price=99.99,
    )


# アイテム作成エンドポイント - リクエストボディの例
@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    return ItemResponse(
        id=1,
        name=item.name,
        description=item.description,
        price=item.price,
    )


# ヘルスチェックエンドポイント - サービス状態確認用
@app.get("/health")
async def health_check():
    return {"status": "ok"}
