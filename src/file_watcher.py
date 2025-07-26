# ファイル監視機能
# 指定されたディレクトリ内のファイル変更を監視し、コールバック関数を実行する
import asyncio
from collections.abc import Callable
from pathlib import Path

from watchfiles import awatch


# ファイル監視クラス
class FileWatcher:
    def __init__(self, watch_paths: list[str], callback: Callable[[], None]):
        # 監視対象パスをPathオブジェクトに変換
        self.watch_paths = [Path(path) for path in watch_paths]
        # ファイル変更時に実行するコールバック関数
        self.callback = callback
        # バックグラウンドタスクの参照
        self._task = None

    # ファイル監視を開始する非同期メソッド
    async def start(self) -> None:
        print(f"Watching for changes in: {', '.join(str(p) for p in self.watch_paths)}")

        # watchfilesライブラリを使用してファイル変更を監視
        async for changes in awatch(*self.watch_paths):
            print(f"Files changed: {len(changes)} files")
            # 変更されたファイルの詳細を出力
            for change_type, file_path in changes:
                print(f"  {change_type.name}: {file_path}")

            # コールバック関数を別スレッドで実行（ブロッキング処理を避けるため）
            try:
                await asyncio.get_event_loop().run_in_executor(None, self.callback)
            except Exception as e:
                print(f"Error in callback: {e}")

    # ファイル監視をバックグラウンドで開始するメソッド
    def start_background(self) -> None:
        # タスクが存在しない、または完了している場合に新しいタスクを作成
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self.start())

    # ファイル監視を停止するメソッド
    def stop(self) -> None:
        # 実行中のタスクがある場合はキャンセル
        if self._task and not self._task.done():
            self._task.cancel()
