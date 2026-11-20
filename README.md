# ハル投稿ツール AI引き継ぎリポジトリ

このリポジトリは、YouTubeの本要約動画からSNS投稿文、2種類の正方形インフォグラフィック、2種類のショート動画を作り、スマートフォン向け投稿ツールへ追加する作業を別のAIへ引き継ぐためのパッケージです。

最初に [AI_HANDOFF_PROMPT.md](AI_HANDOFF_PROMPT.md) を全文読み、その内容を作業指示として扱ってください。

現在進行中の作品は、覚張隆史『日本人とは何か　私たちのルーツを巡る700万年の物語』です。投稿文、字幕、個人版インフォグラフィックまでは完成しています。スタジオ版画像、2種類の動画、サイト組み込みと公開が未完成です。

公開中の投稿ツール：<https://haru-post-tool.syosuke8631.chatgpt.site/>

主な場所：

- `outputs/`：投稿文、画像、字幕、完成動画
- `assets/character-references/`：2組のキャラクター資料
- `sites/haru-post-tool/`：公開サイト
- `create_*_short.py`：ショート動画の参考実装

サイトのコンテンツを再生成するコマンド：

```powershell
python sites/haru-post-tool/build_content.py
node --check sites/haru-post-tool/dist/app.js
```

