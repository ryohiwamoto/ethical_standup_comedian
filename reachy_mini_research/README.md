# Reachy Mini 研究用コントローラー

## 開発と実行の分担

デスクトップPCのCodexでコードを編集する。GitHubにpushし、ラップトップで同じブランチをpullして実行する。
実機とReachy Mini Control、制御サーバーはラップトップ側。`127.0.0.1`は実行中のPC自身を意味する。
デスクトップからラップトップの画面を遠隔操作する場合も、実行するターミナルはラップトップ側である。

## このプログラムでできること

Enter操作で、小さい頭部動作と復帰、または静止を一つずつ実行する。
最初は正負の方向を実機で確認し、後から「下向き」「視線回避」などの表現名を付ける。
角度5度、片道1.5秒、保持1秒は動作確認用の仮値であり、研究上の最適値ではない。
ログには指定値と実際に取得した姿勢行列を保存する。セリフ、録音、笑顔検知、学習はまだ含まない。

## ラップトップでの実行

PowerShellを開き、次を実行する。

```powershell
cd C:\Users\ryoh1\ethical_standup_comedian
git pull --ff-only
cd .\reachy_mini_research
```

`pull`はデスクトップでpushしたものと同じブランチで実行する。ローカル変更で失敗したら上書きせず内容を確認する。

まず、標準Pythonでオフラインのメニューとログ保存を確認できる。SDK不要でロボットへは接続しない。

```powershell
python .\reachy_motion_controller.py
```

Control付属Pythonも利用できる。毎回パスを短くするには、このPowerShell内だけの変数を用意する。

```powershell
$reachyPython = "$env:LOCALAPPDATA\Reachy Mini Control\.venv\Scripts\python.exe"
& $reachyPython .\reachy_motion_controller.py --check
```

`--check`はサーバーの状態を読むだけで、動作・モーター・メディア設定を変更しない。
実機操作前にControlで接続し、Conversationや顔追跡、Expressionを止め、Wake Up後の通常姿勢にする。
Controlは起動したまま、次を実行する。

```powershell
& $reachyPython .\reachy_motion_controller.py --robot
```

1. 起動後に`READY`と入力する。この時点では頭を動かさない。
2. `1`（静止）を選び、次のEnterで試行する。
3. 問題なければ`2`から`5`を一つずつ試す。動作終了を待ってから次へ進む。
4. 見えた方向や引っ掛かりなどを任意のメモに入力する。`q`で終了する。

時間と角度を変更する例:

```powershell
& $reachyPython .\reachy_motion_controller.py --robot --angle 5 --move 2 --hold 2
```

`--angle`は1から10度、`--move`は片道1から5秒、`--hold`は0から10秒。
各試行の開始姿勢を保存し、その姿勢から相対回転して戻る。胴体とアンテナは指定しない。
開始姿勢が基準方向から20度以上、または原点から30mmを超えている場合は試行を拒否する。
これらの制限は初回動作確認用であり、すべての姿勢の到達可能性を保証するものではない。
以前のIK警告・異音・引っ掛かりがあれば続行しない。
Ctrl+Cは送信済み動作の即時停止を保証しない。エラー・中断後に自動復帰動作は送信しない。

動作専用の`no_media`接続を使うため、実行中は制御サーバーがカメラと音声を解放する。
正常終了時にSDKがメディアを再取得する。強制終了時はControlを確認・再接続する。
SDK接続時にautomatic_body_yawはSDKの既定値が適用される。

## ログ

試行すると、このフォルダー直下の`logs`へ日時別CSVを作る。Excelで読めるUTF-8 BOM形式。
プレビューと実機のファイル名・modeを分け、プレビューログを研究結果に含めない。
`sequence_completed`はSDKの指令処理が終了した意味で、目標姿勢への正確な到達を保証しない。
異常時の行にはエラーを保存するが、例外発生までの途中姿勢は保存されない場合がある。
本プログラムは人の主観評価や面白さの測定をまだ行わない。

## 環境

初回は既存のControl付属環境を使い、追加インストールを避ける。
Controlの更新でパスやSDKが変わる可能性があるため、研究を本格化する前に独立したPython環境へ移す。
その際はPython 3.10から3.12の範囲でSDK互換性を確認し、動作確認したバージョンを固定する。
現在確認したSDKは1.14.0。`requirements.txt`は独立環境を作る場合の記録用で、base環境へは無闇に入れない。

公式SDK: https://huggingface.co/docs/reachy_mini/SDK/python-sdk

引き継ぎの詳細は`HANDOVER_FOR_CODEX.md`を参照。
