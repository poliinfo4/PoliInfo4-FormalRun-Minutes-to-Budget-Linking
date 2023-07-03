# PoliInfo4-FormalRun-Minutes-to-Budget-Linking

## 目的
Minutes to Budget Linking (MBLink) は、予算に関する発言文と予算表が与えられたときに、発言文に関連する予算表を紐づけることを目的としています。

https://sites.google.com/view/poliinfo4/subtasks/minutes_to_budget_linking?authuser=0

# データセットについて
- MBLink の Formal Run では、Dry Run (V20230613) と同じデータを使用します。
- リーダーボード投稿の際にはバージョンとして Formal Run を指定してください。

- 入力
    - 議会会議録中の市長の発言文（HTML フォーマット， `*_Minutes.html`）
        - １発言が１つの`<p>`タグとなっています。
        - 予算表とリンクしている発言文には `data-mblink-sentence-id`属性が割り当てられており，文IDが付与されています。
        - トレーニングデータにはリンクしている表IDが `data-mblink-table-ids`属性として付与されています。複数の場合は半角スペース区切りで表IDが付与されます。
        - テストデータの場合でも，予算表とリンクしている発言文にのみ `data-mblink-sentence-id`属性が割り当てられています。
    - 予算説明書などに含まれる表（HTML フォーマット， `*_Budgets.html`）
        - PDFファイルからHTMLファイルへ変換したもの。
        - 各表の `<table>`タグには表IDとして `data-mblink-table-id`属性が割り当てられています。
        - 表の各セルにもIDが振られていますが本タスクでは用いません。
- 出力
    - 発言文に関連する予算表を紐づけたファイル (JSONフォーマット)
    - 書式は配布ファイルの `poliinfo4_mblink_random_20230613.json`を参照してください。

## 配布ファイル
- 学習用ファイル
    - `training/PoliInfo4_MBLink_v20230613_Otaru_*_Minutes.html`
    - `training/PoliInfo4_MBLink_v20230613_Otaru_*_Budgets.html`
- テスト用ファイル
    - `test/PoliInfo4_MBLink_v20230613_Otaru_*_Minutes.html`
    - `test/PoliInfo4_MBLink_v20230613_Otaru_*_Budgets.html`
- サンプル出力ファイル
    - `poliinfo4_mblink_random_20230613.json`
    - `mblink_sample_output.py`によるランダム出力の結果です
- ランダム出力スクリプト
    - `mblink_sample_output.py`
- 評価スクリプト
    - `mblink_eval.py`
