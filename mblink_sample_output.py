from __future__ import annotations

"""
PoliInfo4 MBLinkタスクの推論スクリプトサンプル。
ランダムにテーブルIDを付与する。
依存ライブラリ：
    HTML解析ライブラリのBeautifusoup4を使用します。
    pip install beautifulsoup4
    などでインストールしてください。
使い方：
    [-i] 資料HTMLファイル（複数指定）
出力：
    標準出力に推論結果がJSON形式で出力される。

作成：2023/06/19 乙武北斗
"""

import argparse
import random
import json
from pathlib import Path
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict


@dataclass
class MBLinkData:
    """
    MBLinkのデータインスタンス一つ分の書式
    """
    sentenceID: str
    tableIds: list[str]


def get_args():
    """
    コマンドライン引数を処理する関数．
    [-i] 資料HTMLファイルを含むディレクトリを指定する。
    """
    parser = argparse.ArgumentParser(
        description="""PoliInfo4 MBLinkタスクの推論スクリプトサンプル。
ランダムにテーブルIDを付与する。"""
    )

    parser.add_argument("-i", "--input-files", nargs="+", required=True,
                        help="Minutes HTMLファイルを指定します")
    return parser.parse_args()


if __name__ == "__main__":
    # コマンドライン引数の解析
    args = get_args()

    # 結果オブジェクト
    ret: list[MBLinkData] = []

    for minutes_file in [Path(x) for x in args.input_files]:
        budget_file = minutes_file.parent / f"{minutes_file.stem.rsplit('_', 1)[0]}_Budgets.html"
        
        table_ids: list[str] = []
        bs = BeautifulSoup(budget_file.read_text(encoding="utf-8"), "html.parser")
        for t in bs.select("table[data-mblink-table-id]"):
            table_ids.append(t.attrs["data-mblink-table-id"])
        
        bs = BeautifulSoup(minutes_file.read_text(encoding="utf-8"), "html.parser")
        ps = bs.select("p[data-mblink-sentence-id]")
        for p in ps:
            ret.append(MBLinkData(
                sentenceID=p.attrs["data-mblink-sentence-id"],
                tableIds=random.sample(table_ids, random.randint(1, 5))
            ))

    print(json.dumps([asdict(x) for x in ret], ensure_ascii=False, indent=4))
