"""
PoliInfo4 MBLinkタスクの評価スクリプト。
使い方：
    [-i] 推定結果ファイル
    [-g] Gold Standardファイル
出力：
    標準出力に評価結果がJSON形式で出力される。
作成：2023/06/19 乙武北斗
"""

import argparse
import json
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class EvalResult:
    """
    評価結果のスキーマ
    """
    success: bool
    f1: float
    sentences: dict[str, dict[str, int | float | None]]


@dataclass
class SentenceEvals:
    org: int
    est: int
    crr: int

    def precision(self) -> float | None:
        if self.est == 0:
            return None
        return self.crr / self.est

    def recall(self) -> float | None:
        if self.org == 0:
            return None
        return self.crr / self.org

    def f1(self) -> float | None:
        p = self.precision()
        r = self.recall()
        if p is None and r is None:
            return None
        if p is None or r is None:
            return 0
        if p + r == 0:
            return 0
        return (2 * p * r) / (p + r)

    def to_dict(self) -> dict[str, int | float | None]:
        return {
            "org": self.org,
            "est": self.est,
            "crr": self.crr,
            "precision": self.precision(),
            "recall": self.recall(),
            "f1": self.f1()
        }


def get_args():
    """
    コマンドライン引数を処理する関数．
    [-i] 推定結果ファイル
    [-g] Gold Standardファイル
    """
    parser = argparse.ArgumentParser(
        description="""PoliInfo4 MBLinkタスクの評価スクリプト。"""
    )

    parser.add_argument("-i", "--input", required=True,
                        help="推定結果ファイルを指定します")
    parser.add_argument("-g", "--gs", required=True,
                        help="Gold Standardファイルを指定します")
    return parser.parse_args()


def load_json(s: str) -> dict[str, set[str]]:
    ret: dict[str, set[str]] = {}
    org = json.loads(s)
    for x in org:
        ret[x["sentenceID"]] = set()
        for tid in x["tableIds"]:
            ret[x["sentenceID"]].add(tid)
    return ret


if __name__ == "__main__":
    # コマンドライン引数の解析
    args = get_args()

    evals = EvalResult(True, 0, {})
    sentences: list[SentenceEvals] = []
    result = load_json(Path(args.input).read_text(encoding="utf-8"))
    gs = load_json(Path(args.gs).read_text(encoding="utf-8"))

    for sid, anss in gs.items():
        if sid not in result:
            evals.success = False
            break

        n = SentenceEvals(
            org=len(anss),
            est=len(result[sid]),
            crr=len(anss & result[sid])
        )
        sentences.append(n)

        evals.sentences[sid] = n.to_dict()

    if evals.success:
        f1s = [y for x in sentences if (y := x.f1()) is not None]
        evals.f1 = sum(f1s) / len(f1s)
        print(json.dumps(asdict(evals), ensure_ascii=False, indent=4))
    else:
        print(json.dumps(asdict(evals), ensure_ascii=False, indent=4))
