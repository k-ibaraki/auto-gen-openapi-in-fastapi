# FastAPI OpenAPI Auto Generation Sample

FastAPIでOpenAPIドキュメントをホットリロードで自動生成するサンプルプロジェクト

## 特徴

- ファイル変更を監視してOpenAPIドキュメントを自動生成
- JSON・YAML両形式でのエクスポート
- 開発中のホットリロードに対応

## セットアップ

```bash
# 依存関係のインストール
uv sync --all-extras

# サーバー起動
uv run python app.py
```

## 生成されるファイル

- `docs/openapi.yaml` - YAML形式のOpenAPIスキーマ

## エンドポイント

- `GET /` - Hello World
- `GET /items/{item_id}` - アイテム取得
- `POST /items/` - アイテム作成
- `GET /health` - ヘルスチェック
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

## 仕組み

1. アプリ起動時に初回のOpenAPIドキュメントを生成
2. `watchfiles`を使用してPythonファイルの変更を監視
3. ファイル変更検知時に自動でOpenAPIドキュメントを再生成
