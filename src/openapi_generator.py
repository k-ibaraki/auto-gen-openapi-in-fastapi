# OpenAPIスキーマの自動生成機能
# FastAPIアプリからJSONとYAML形式でOpenAPIドキュメントを出力する
import json
from pathlib import Path

from fastapi import FastAPI


# OpenAPIスキーマをJSON形式で生成・保存する関数
def generate_openapi_json(app: FastAPI, output_path: str = "openapi.json") -> None:
    # FastAPIアプリからOpenAPIスキーマを取得
    openapi_schema = app.openapi()

    # 出力ファイルパスを作成し、必要に応じてディレクトリを作成
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # JSON形式でスキーマをファイルに保存
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, ensure_ascii=False, indent=2)

    print(f"OpenAPI schema generated: {output_file.absolute()}")


# OpenAPIスキーマをYAML形式で生成・保存する関数
def generate_openapi_yaml(app: FastAPI, output_path: str = "openapi.yaml") -> None:
    # PyYAMLライブラリの動的インポート（オプション依存）
    try:
        import yaml
    except ImportError:
        print("PyYAML is required for YAML output")
        return

    # FastAPIアプリからOpenAPIスキーマを取得
    openapi_schema = app.openapi()

    # 出力ファイルパスを作成し、必要に応じてディレクトリを作成
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # YAML形式でスキーマをファイルに保存
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(openapi_schema, f, default_flow_style=False, allow_unicode=True)

    print(f"OpenAPI schema generated: {output_file.absolute()}")
