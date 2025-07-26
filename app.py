# FastAPIサーバー起動スクリプト
# uvicornを使用してアプリケーションを起動し、開発モードでホットリロードを有効にする
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",  # FastAPIアプリケーションの場所
        host="0.0.0.0",  # すべてのIPアドレスでアクセス可能
        port=8000,       # ポート番号
        reload=True,     # ファイル変更時の自動リロード
        reload_dirs=["src"],  # リロード監視対象ディレクトリ
    )
