# XXD VPS

[中文](./README.md) · [English](./README.en.md) · [한국어](./README.ko.md) · **日本語** · [العربية](./README.ar.md) · [Español](./README.es.md) · [Français](./README.fr.md) · [Русский](./README.ru.md) · [Deutsch](./README.de.md) · [Português](./README.pt.md)

ネットが使いにくい国へ出張しても、いつものウェブサイトや AI ツールをそのまま使えます。

手順を追ったチュートリアルサイト（英語・中国語）：<https://vps.xiaoxiaodong.ai/en/>（中国語版：<https://vps.xiaoxiaodong.ai>、ミラー：<https://nevertoday.github.io/xiaoxiaodong-vps/en/>）

やり方はシンプルです。自分のパソコンに Codex を入れ、海外サーバーを 1 台買い、このプロジェクトどおりに Codex にリモートで設定してもらい、スマホとパソコンに購読を読み込むだけ。**サーバーには何もインストールせず、ログインする必要もありません。** 回線は自分専用で、知らない人とは共有しません。

## 設定が終わると

- **自分だけの回線**：パソコン、スマホ、ルーターで使えます。メインと予備の 2 つのノードがあり、片方がつながらないと自動で切り替わります。
- **読み込めばすぐ使える**：よく使うサイトと AI ツールの振り分けルールは設定済み。中国本土のサイトは直接つながり、それ以外は自分のサーバーを経由します。
- **CLIProxyAPI**：自分専用の API と管理画面。最新版へ自動で更新されます。
  - ⚠️ **Claude のアカウントを CLIProxyAPI につながないでください**：Anthropic のポリシーで認められていません。ChatGPT などは OpenAI が公式に問題ないとしていて、私は画像作りによく使っています。
- **安全**：サーバーにはこのパソコンの鍵でしかログインできません。正式な HTTPS 証明書を使うので「保護されていない通信」の警告も出ません。
- **ほぼ手間なし**：証明書、ルール、CLIProxyAPI は自動で更新され、設定は毎日自動でバックアップされます。

## 4 ステップで使い始める

### 1. パソコンに Codex を入れる

Codex は OpenAI の AI アプリで、有料の ChatGPT プランでログインします。入れるのはサーバーではなく**自分のパソコン**です。

- **初心者の方**：デスクトップアプリを入れます。Windows は Microsoft Store で **Codex** を検索してインストール、Mac は [Codex の公式サイト](https://openai.com/codex/)からダウンロードします。開いたら ChatGPT アカウントでログインしてください。
- **慣れている方**：[Codex](https://github.com/openai/codex) のコマンドライン版を使います。インストール済みなら、ターミナルで `codex` を実行してそのまま話しかけるだけです。

ChatGPT のプランがない場合は、[チュートリアルサイト](https://vps.xiaoxiaodong.ai/en/guide/3-deploy/)（英語）のステップ 3 にある「Type it yourself」（自分で入力する）方法を使ってください。

### 2. サーバーを買う

いまは **BandwagonHost** をそのまま買うのがおすすめです。私自身も使い続けています。

この種のサーバーを勧めるのは、**自腹を切って何度も痛い目を見て得た教訓**だからです。回線が中国本土からの接続向けに最適化されていて、その安定ぶりに私はすっかり熱烈なファンになりました。

**[BandwagonHost を購入する](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=88&billingcycle=quarterly&configoption%5B17%5D=55)**

このリンクのプランは**毎月 2TB の転送量**、メモリ 2GB、ロサンゼルスの CN2 GIA データセンターで、家族で使っても余裕があります。

以前おすすめしていた ~~[1TB プラン](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=87&billingcycle=quarterly&configoption%5B17%5D=55)~~ は現在在庫切れで購入できません。

[DMIT](https://www.dmit.io/aff.php?aff=23544) も私が気に入って使っているサーバーですが、残念ながら現在は在庫切れです。待つ必要はありません。

**なぜこの 2 社だけをおすすめするのか？** BandwagonHost と DMIT は、私が何度もテストして残った 2 社で、いま安心しておすすめできる唯一の選択肢です。上のリンクのプランは、この 2 社で現在在庫のある唯一のエントリープランでもあります。ほかのサーバーは見た目は良さそうでも、実際に使うと落とし穴が多いものです。普段は問題なくても、状況が厳しくなると持ちこたえられず、切れたりつながらなくなったりして、AI サービスを使っているとアカウントにまで影響することがあります。私はこうしたことで何度も振り回され、正直うんざりしました。同じ回り道をしないよう、ここから買うことをおすすめします。

> いずれも私の紹介リンクです。リンク経由で購入されると私に紹介料が入る場合があり、その収入は慈善活動に使います。価格と在庫は公式サイトをご確認ください。

OS は **Ubuntu 24.04** を選んでください。開通したら管理画面で 3 つをメモします：**サーバー IP、root パスワード（または鍵ファイル）、SSH ポート**。BandwagonHost の場合は **VEID と API Key** もメモしておきます（KiwiVM 左メニューの「API」ページ、[探し方](https://vps.xiaoxiaodong.ai/en/howto/traffic-and-ip/)）。クライアントに表示される転送量が管理画面と一致するようになります。

購入後は、サーバーにログインしたり何かをインストールしたりする必要はありません。次のステップは Codex の仕事です。

### 3. Codex に設定してもらう

ステップ 1 の Codex を開きます（パソコンでコマンドを実行できるほかの AI ツールでも構いません）。下の文章をコピーし、埋めてから送ってください。

```text
「XXD VPS」方式で、新しく買ったサーバーを設定してください。

方式：https://github.com/nevertoday/xiaoxiaodong-vps
まずこのプロジェクトを私のパソコンにダウンロードし、
skills/xiaoxiaodong-vps/SKILL.md を最後まで読んでください。
その手順とルールに厳密に従い、プロジェクトのスクリプトで設定と検証を行ってください。
やり取りは日本語でお願いします。

私のサーバー：
- IP：
- ログイン方法：初期パスワード（私が自分で入力します。チャットで送るよう求めないでください）
- SSH ユーザーとポート：デフォルト
- 今後ログインに使う名前：bwg
- BandwagonHost の VEID と API Key（公式の転送量表示用。BandwagonHost でなければこの行を削除）：
```

埋めるところ：

- **IP**：管理画面に表示されているサーバー IP。
- **ログイン方法**：業者から鍵ファイルをもらった場合は `鍵ファイル：ファイルのパス` に変えてください（zip でも可）。
- **名前**：`bwg` を好きな名前に。以後は `ssh その名前` と打つだけでサーバーに入れます。
- **BandwagonHost**：最後の行に VEID と API Key を記入してください。クライアントの転送量の上限・使用量・リセット日が BandwagonHost の管理画面から直接読み込まれ、1TB でも 2TB でも一致します。**BandwagonHost でなければ、その行を削除してください。** その場合は毎月 1000GB として表示されます。

ユーザーとポートが root / 22 でない場合は、「デフォルト」を実際の値に変えてください。

あとは AI が終わるのを待つだけで、通常 10〜20 分です。途中で一度、パソコンにパスワード入力欄が表示されるので、サーバーのパスワードを入力してください。**パスワードはチャットに貼らないでください。** 設定が終わるとパスワードでのログインは無効になり、このパソコンからしかログインできなくなります。

AI がプロジェクトをダウンロードできない場合は、自分で [ZIP をダウンロード](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip)して解凍し、上の文章に「プロジェクトはここにあります：フォルダのパス」と一行足してください。

完了すると、デスクトップに `my-server-名前-subscriptions-and-accounts-ja.md` というファイルができます。中身は：

- パソコン・ルーター用の **Clash 購読 URL**、iPhone 用の **Shadowrocket 購読 URL**
- 3x-ui パネルの URL、ユーザー名、パスワード
- CLIProxyAPI 管理画面の URL、管理用ログインキー、API の URL と API キー

<details>
<summary>よくサーバーを設定する方へ：skill としてインストールすれば一言で呼び出せます</summary>

ターミナルで一度だけ実行します。

```bash
git clone https://github.com/nevertoday/xiaoxiaodong-vps.git
mkdir -p ~/.claude/skills ~/.codex/skills
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.claude/skills/
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.codex/skills/
```

以後は AI に「xiaoxiaodong-vps で新しいサーバーを設定して」と言うだけで、必要な情報を AI が聞いてきます。

</details>

### 4. 購読を読み込む

- **パソコン（おすすめは Clash Verge Rev）**：[Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases) をインストールして Clash 購読 URL を読み込み、**ルール**モードを選び、**TUN モード**（仮想ネットワークアダプター。求められたらサービスをインストール）をオンにします。システムプロキシだけだと、ブラウザの WebRTC から実際の IP が漏れることがあります。[WebRTC 漏洩の修正ガイド](./docs/Clash-Verge-WebRTC泄露修复手册.md)（中国語。AI アシスタントがそのまま手順どおりに進められるように書かれています）を参照してください。
- **iPhone**：Shadowrocket で Shadowrocket 購読 URL を読み込みます。
- **ルーター（OpenClash）**：同じ Clash 購読 URL がそのまま使え、家中の端末がこの回線を通ります。「設定の購読」に URL を追加してください（YAML ファイルをアップロードすると、通信量が表示されずルールも自動更新されません）。「オンライン購読変換」はオフ、コアは Meta を選びます。
- **すでに v2rayN を使っている場合（Windows / Mac / Linux）**：使えますが、あくまで代替です。「Shadowrocket（iPhone）」の行の購読 URL を読み込み（Clash の行ではありません）、ルーティングは「中国本土をバイパス」を選び、WebRTC 漏洩対策に TUN をオンにします。この購読はノードだけで、AI の振り分けや WeChat 直結のルールは入っていないため、パソコンでは引き続き Clash Verge Rev をおすすめします。詳しくは [v2rayN ガイド](https://vps.xiaoxiaodong.ai/en/howto/v2rayn/)（英語）。

最後に <https://ip.net.coffee/claude/> を開き、自分のサーバーの IP が表示されればつながっています。

## 出張の前に

- **出発前に設定して、一度テストしておきましょう。** 制限のあるネットワークに着いてからでは、プロジェクトのダウンロードや AI ツールを開くことさえ難しくなることがあります。
- スマホとパソコンの両方にクライアントを入れて購読を読み込み、2 つのノードがどちらもつながるか確認してください。
- 現地のあるネットワークでサーバーにつながらないときは、まず別のネットワークを試します（ホテルの Wi-Fi、モバイルデータ、別の通信会社）。どれもだめなら、その地域でサーバーの IP がブロックされている可能性が高く、設定では直りません。業者に IP の変更を依頼してください。
- 回線は自分と家族だけで使い、人とは共有しないでください。

## あとでサーバーを点検する

下の文章を AI に送ります（`bwg` は自分の名前に）。

```text
「XXD VPS」方式で私のサーバーを点検してください：ssh bwg

方式：https://github.com/nevertoday/xiaoxiaodong-vps
プロジェクトをダウンロードし、skills/xiaoxiaodong-vps/SKILL.md の
「以后的复核和维护」（その後の点検とメンテナンス）の部分を読んでください。
まず点検だけを行い、失敗した項目と原因を教えてください。修正は私が同意してからにしてください。
パスワード、購読 URL、キーはチャットに表示しないでください。やり取りは日本語でお願いします。
```

詳しい資料（[トラブルシューティング](./skills/xiaoxiaodong-vps/references/troubleshooting.md)、[設計の説明](./skills/xiaoxiaodong-vps/references/design.md)）は現在中国語のみです。AI に読んでもらえます。

## フィードバック・ご提案

ご提案や、分かりにくい箇所・手順どおりにやってもうまくいかない箇所があれば、[GitHub で Issue を作成](https://github.com/nevertoday/xiaoxiaodong-vps/issues)してください。[X の DM](https://x.com/xiaoxiaodong)（@xiaoxiaodong）や、WeChat で私（Xiaoxiaodong、小小东）を追加して伝えていただいても構いません。ガイドに反映します。

<img src="https://vip.xiaoxiaodong.ai/site-assets/wechat-qr.png" width="160" alt="Xiaoxiaodong の WeChat QR コード">

## プライバシー

- このプロジェクトには、実在するサーバーの情報は一切含まれていません。
- サーバーごとのパスワード、鍵、購読 URL、API キーは設定時に新しく生成され、サーバーと自分のパソコンにだけ保存されます。AI がチャットに表示することはありません。
- ログイン情報のファイル、購読 URL、キーは、どこにも投稿したりスクリーンショットを撮ったりしないでください。
- セキュリティ上の問題は [SECURITY.md](./SECURITY.md) をご覧ください。

つながるかどうか、速度がどうかは、現地のネットワークとサーバーの回線にも左右されます。このプロジェクトはサーバーが正しく設定されることを保証しますが、どの国のどの通信会社からも同じ IP につながることまでは保証できません。

## ライセンス

[MIT](./LICENSE)
