from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = Path(__file__).resolve().parent / "dist"
ASSET_DIR = OUTPUT_DIR / "assets"
OUTPUT = OUTPUT_DIR / "content.json"

POSTS = [
    {
        "id": "gelatin-evidence",
        "file": "ゼラチンを知る_投稿セット.md",
        "title": "ゼラチンを知る 動画の主張と確認したいこと",
        "sourceTitle": "参考動画：ゼラチンに関する動画",
        "sourceUrl": "https://youtu.be/25MfSVf1dDA",
        "updatedAt": "2026年11月28日",
        "personal": "ゼラチンを知る_個人版_インフォグラフィック.png",
        "studio": "ゼラチンを知る_スタジオ版_インフォグラフィック.png",
        "video": "ゼラチンを知る_個人版_動画.mp4",
        "poster": "ゼラチンを知る_個人版_ポスター.png",
        "videoLabel": "ゼラチンを知る・個人版 120秒",
        "videoDuration": "120秒",
        "studioVideo": "ゼラチンを知る_スタジオ版_動画.mp4",
        "studioPoster": "ゼラチンを知る_スタジオ版_ポスター.png",
        "studioVideoLabel": "ゼラチンを知る・スタジオ版 128秒",
        "studioVideoDuration": "128秒",
    },
    {
        "id": "new-class-society",
        "file": "新しい階級社会_投稿セット.md",
        "title": "橋本健二『新しい階級社会 最新データが明かす〈格差拡大の果て〉』",
        "sourceTitle": "参考動画：『新しい階級社会』本要約",
        "sourceUrl": "https://youtu.be/u2QKfmO-yzw",
        "updatedAt": "2026年11月28日",
        "personal": "新しい階級社会_個人版_インフォグラフィック_v2.png",
        "studio": "新しい階級社会_スタジオ版_インフォグラフィック_v2.png",
        "video": "新しい階級社会_個人版_動画.mp4",
        "poster": "新しい階級社会_個人版_ポスター.png",
        "videoLabel": "格差を知り社会を考える・個人版 136秒",
        "videoDuration": "136秒",
        "studioVideo": "新しい階級社会_スタジオ版_動画.mp4",
        "studioPoster": "新しい階級社会_スタジオ版_ポスター.png",
        "studioVideoLabel": "格差を知り社会を考える・スタジオ版 146秒",
        "studioVideoDuration": "146秒",
    },
    {
        "id": "money-time",
        "file": "お金と時間_投稿セット.md",
        "title": "投資うさぎ『給料だけでは、お金持ちになれないから』",
        "sourceTitle": "参考動画：『給料だけでは、お金持ちになれないから』本要約",
        "sourceUrl": "https://youtu.be/As8Jz70ogvg",
        "updatedAt": "2026年11月27日",
        "personal": "お金と時間_個人版_インフォグラフィック_v2.png",
        "studio": "お金と時間_スタジオ版_インフォグラフィック_v2.png",
        "video": "お金と時間_個人版_動画.mp4",
        "poster": "お金と時間_個人版_ポスター.png",
        "videoLabel": "お金と時間を育てる・個人版 130秒",
        "videoDuration": "130秒",
        "studioVideo": "お金と時間_スタジオ版_動画.mp4",
        "studioPoster": "お金と時間_スタジオ版_ポスター.png",
        "studioVideoLabel": "お金と時間を育てる・スタジオ版 140秒",
        "studioVideoDuration": "140秒",
    },
    {
        "id": "think-again",
        "file": "THINK_AGAIN_投稿セット.md",
        "title": "アダム・グラント『THINK AGAIN 発想を変える、思い込みを手放す』",
        "sourceTitle": "参考動画：『THINK AGAIN』本要約",
        "sourceUrl": "https://youtu.be/0ZwSo8ugsjI",
        "updatedAt": "2026年11月26日",
        "personal": "THINK_AGAIN_個人版_インフォグラフィック.png",
        "studio": "THINK_AGAIN_スタジオ版_インフォグラフィック.png",
        "video": "THINK_AGAIN_個人版_動画.mp4",
        "poster": "THINK_AGAIN_個人版_ポスター.png",
        "videoLabel": "考え直す力・個人版 111秒",
        "videoDuration": "111秒",
        "studioVideo": "THINK_AGAIN_スタジオ版_動画.mp4",
        "studioPoster": "THINK_AGAIN_スタジオ版_ポスター.png",
        "studioVideoLabel": "考え直す力・スタジオ版 119秒",
        "studioVideoDuration": "119秒",
    },
    {
        "id": "life-choices",
        "file": "人生は攻略できる_投稿セット.md",
        "title": "橘玲『人生は攻略できる』",
        "sourceTitle": "参考動画：『人生は攻略できる』本要約",
        "sourceUrl": "https://youtu.be/teObCPv3l2s",
        "updatedAt": "2026年11月26日",
        "personal": "人生は攻略できる_個人版_インフォグラフィック.png",
        "studio": "人生は攻略できる_スタジオ版_インフォグラフィック.png",
        "video": "人生は攻略できる_個人版_動画.mp4",
        "poster": "人生は攻略できる_個人版_ポスター.png",
        "videoLabel": "人生の自由を広げる・個人版 127秒",
        "videoDuration": "127秒",
        "studioVideo": "人生は攻略できる_スタジオ版_動画.mp4",
        "studioPoster": "人生は攻略できる_スタジオ版_ポスター.png",
        "studioVideoLabel": "人生の自由を広げる・スタジオ版 136秒",
        "studioVideoDuration": "136秒",
    },
    {
        "id": "mama-investor",
        "file": "ママ投資家_投稿セット.md",
        "title": "ちょる子『ママ投資家が育休中に１億貯めた株式投資』",
        "sourceTitle": "参考動画：『ママ投資家が育休中に１億貯めた株式投資』本要約",
        "sourceUrl": "https://youtu.be/wpatta-OWVU",
        "updatedAt": "2026年11月26日",
        "personal": "ママ投資家_個人版_インフォグラフィック.png",
        "studio": "ママ投資家_スタジオ版_インフォグラフィック.png",
        "video": "ママ投資家_個人版_動画.mp4",
        "poster": "ママ投資家_個人版_ポスター.png",
        "videoLabel": "株式投資を学ぶ・個人版 144秒",
        "videoDuration": "144秒",
        "studioVideo": "ママ投資家_スタジオ版_動画.mp4",
        "studioPoster": "ママ投資家_スタジオ版_ポスター.png",
        "studioVideoLabel": "株式投資を学ぶ・スタジオ版 154秒",
        "studioVideoDuration": "154秒",
    },
    {
        "id": "gold-silver",
        "file": "金と銀_投稿セット.md",
        "title": "副島隆彦『金を握りしめた者が勝つ 銀は10倍になる』",
        "sourceTitle": "参考動画：『金を握りしめた者が勝つ 銀は10倍になる』本要約",
        "sourceUrl": "https://youtu.be/0atZIODuVDQ",
        "updatedAt": "2026年11月25日",
        "personal": "金と銀_個人版_インフォグラフィック.png",
        "studio": "金と銀_スタジオ版_インフォグラフィック.png",
        "video": "金と銀_個人版_動画.mp4",
        "poster": "金と銀_個人版_ポスター.png",
        "videoLabel": "金と銀を考える・個人版 128秒",
        "videoDuration": "128秒",
        "studioVideo": "金と銀_スタジオ版_動画.mp4",
        "studioPoster": "金と銀_スタジオ版_ポスター.png",
        "studioVideoLabel": "金と銀を考える・スタジオ版 138秒",
        "studioVideoDuration": "138秒",
    },
    {
        "id": "japan-stocks-inflation",
        "file": "日本株_投稿セット.md",
        "title": "エミン・ユルマズ・武者陵司『なぜこれから30年日本株は爆上げし続けるのか？』",
        "sourceTitle": "参考動画：『なぜこれから30年日本株は爆上げし続けるのか？』本要約",
        "sourceUrl": "https://youtu.be/qRqwtJ4VAgs",
        "updatedAt": "2026年11月25日",
        "personal": "日本株_個人版_インフォグラフィック.png",
        "studio": "日本株_スタジオ版_インフォグラフィック.png",
        "video": "日本株_個人版_動画.mp4",
        "poster": "日本株_個人版_ポスター.png",
        "videoLabel": "日本株とインフレ・個人版 127秒",
        "videoDuration": "127秒",
        "studioVideo": "日本株_スタジオ版_動画.mp4",
        "studioPoster": "日本株_スタジオ版_ポスター.png",
        "studioVideoLabel": "日本株とインフレ・スタジオ版 137秒",
        "studioVideoDuration": "137秒",
    },
    {
        "id": "inflation-living",
        "file": "物価上昇_投稿セット.md",
        "title": "物価上昇に負けない 暮らしを守る６つのヒント",
        "sourceTitle": "参考動画：30年に1度のチャンス到来！本要約",
        "sourceUrl": "https://youtu.be/G1Oq6Te4Xlk",
        "updatedAt": "2026年11月25日",
        "personal": "物価上昇_個人版_インフォグラフィック.png",
        "studio": "物価上昇_スタジオ版_インフォグラフィック.png",
        "video": "物価上昇_個人版_動画.mp4",
        "poster": "物価上昇_個人版_ポスター.png",
        "videoLabel": "物価上昇への備え・個人版 104秒",
        "videoDuration": "104秒",
        "studioVideo": "物価上昇_スタジオ版_動画.mp4",
        "studioPoster": "物価上昇_スタジオ版_ポスター.png",
        "studioVideoLabel": "物価上昇への備え・スタジオ版 110秒",
        "studioVideoDuration": "110秒",
    },
    {
        "id": "food-investment",
        "file": "食べる投資_投稿セット.md",
        "title": "『食べる投資〜ハーバードが教える世界最高の食事術〜』",
        "sourceTitle": "参考動画：『食べる投資』本要約",
        "sourceUrl": "https://youtu.be/wusWQQnhVw8",
        "updatedAt": "2026年11月24日",
        "personal": "食べる投資_個人版_インフォグラフィック_v2.png",
        "studio": "食べる投資_スタジオ版_インフォグラフィック_v2.png",
        "video": "食べる投資_個人版_ショート動画.mp4",
        "poster": "食べる投資_個人版_ポスター.png",
        "videoLabel": "『食べる投資』個人版49秒ショート",
        "videoDuration": "49秒",
        "studioVideo": "食べる投資_スタジオ版_ショート動画.mp4",
        "studioPoster": "食べる投資_スタジオ版_ポスター.png",
        "studioVideoLabel": "『食べる投資』スタジオ版53秒ショート",
        "studioVideoDuration": "53秒",
    },
    {
        "id": "great-life",
        "file": "グレートライフ_投稿セット.md",
        "title": "スコット・アラン『GREAT LIFE 一度しかない人生を最高の人生にする方法』",
        "sourceTitle": "参考動画：『GREAT LIFE 一度しかない人生を最高の人生にする方法』本要約",
        "sourceUrl": "https://youtu.be/TFy-hbwTXnU",
        "updatedAt": "2026年11月24日",
        "personal": "グレートライフ_個人アカウント用.png",
        "studio": "グレートライフ_ダンススタジオ用.png",
        "video": "great_life_short/グレートライフ_ショート動画.mp4",
        "poster": "great_life_short/slides/slide-01.png",
        "videoLabel": "『グレートライフ』個人版51秒ショート",
        "videoDuration": "51秒",
        "studioVideo": "great_life_studio_short/グレートライフ_スタジオ版ショート動画.mp4",
        "studioPoster": "great_life_studio_short/slides/slide-01.png",
        "studioVideoLabel": "『グレートライフ』スタジオ版51秒ショート",
    },
    {
        "id": "psychology-of-money",
        "file": "サイコロジー・オブ・マネー_投稿セット.md",
        "title": "モーガン・ハウセル『サイコロジー・オブ・マネー 一生お金に困らない「富」のマインドセット』",
        "sourceTitle": "参考動画：『サイコロジー・オブ・マネー 一生お金に困らない「富」のマインドセット』本要約",
        "sourceUrl": "https://youtu.be/H3__XxCja1U",
        "updatedAt": "2026年11月24日",
        "personal": "サイコロジー・オブ・マネー_個人アカウント用.png",
        "studio": "サイコロジー・オブ・マネー_ダンススタジオ用.png",
        "video": "psychology_of_money_short/サイコロジー・オブ・マネー_ショート動画.mp4",
        "poster": "psychology_of_money_short/slides/slide-01.png",
        "videoLabel": "『サイコロジー・オブ・マネー』個人版46秒ショート",
        "videoDuration": "46秒",
        "studioVideo": "psychology_of_money_studio_short/サイコロジー・オブ・マネー_スタジオ版ショート動画.mp4",
        "studioPoster": "psychology_of_money_studio_short/slides/slide-01.png",
        "studioVideoLabel": "『サイコロジー・オブ・マネー』スタジオ版41秒ショート",
    },
    {
        "id": "what-rich-dont-buy",
        "file": "金持ちが絶対買わないもの_投稿セット.md",
        "title": "本要約チャンネル『金持ちが絶対買わないもの・上位1%の養分にならない6つのルール』",
        "sourceTitle": "参考動画：『金持ちが絶対買わないものを暴露します。上位1%の投資家の養分になりたくなければ、この6つだけは絶対に買うな！！』本要約",
        "sourceUrl": "https://www.youtube.com/watch?v=il1-ti8GlEY",
        "updatedAt": "2026年11月23日",
        "personal": "金持ちが絶対買わないもの_個人アカウント用.png",
        "studio": "金持ちが絶対買わないもの_ダンススタジオ用.png",
        "video": "what_rich_dont_buy_short/金持ちが絶対買わないもの_ショート動画.mp4",
        "poster": "what_rich_dont_buy_short/slides/slide-01.png",
        "videoLabel": "『金持ちが絶対買わないもの』個人版55秒ショート",
        "videoDuration": "55秒",
        "studioVideo": "what_rich_dont_buy_studio_short/金持ちが絶対買わないもの_スタジオ版ショート動画.mp4",
        "studioPoster": "what_rich_dont_buy_studio_short/slides/slide-01.png",
        "studioVideoLabel": "『金持ちが絶対買わないもの』スタジオ版55秒ショート",
    },
    {
        "id": "100m-yen-savings",
        "file": "1億円貯める方法_投稿セット.md",
        "title": "橘玲・大橋弘祐『難しいことはわかりませんが、1億円貯める方法を教えてください！』",
        "sourceTitle": "参考動画：『難しいことはわかりませんが、1億円貯める方法を教えてください！』本要約",
        "sourceUrl": "https://www.youtube.com/watch?v=BKDca2K6rvo",
        "updatedAt": "2026年11月22日",
        "personal": "1億円貯める方法_個人アカウント用.png",
        "studio": "1億円貯める方法_ダンススタジオ用.png",
        "video": "100m_yen_short/1億円貯める方法_ショート動画.mp4",
        "poster": "100m_yen_short/slides/slide-01.png",
        "videoLabel": "『1億円貯める方法』個人版57秒ショート",
        "videoDuration": "57秒",
        "studioVideo": "100m_yen_studio_short/1億円貯める方法_スタジオ版ショート動画.mp4",
        "studioPoster": "100m_yen_studio_short/slides/slide-01.png",
        "studioVideoLabel": "『1億円貯める方法』スタジオ版57秒ショート",
    },
    {
        "id": "clothes-declutter",
        "file": "服捨て_投稿セット.md",
        "title": "昼田祥子『服捨て 自分を解き放つメソッド』",
        "sourceTitle": "参考動画：『服捨て 自分を解き放つメソッド』本要約",
        "sourceUrl": "https://www.youtube.com/watch?v=HYM-bLN9UmQ",
        "updatedAt": "2026年11月21日",
        "personal": "服捨て_個人アカウント用.png",
        "studio": "服捨て_ダンススタジオ用.png",
        "video": "clothes_declutter_short/服捨て_ショート動画.mp4",
        "poster": "clothes_declutter_short/slides/slide-01.png",
        "videoLabel": "『服捨て』個人版56秒ショート",
        "videoDuration": "56秒",
        "studioVideo": "clothes_declutter_studio_short/服捨て_スタジオ版ショート動画.mp4",
        "studioPoster": "clothes_declutter_studio_short/slides/slide-01.png",
        "studioVideoLabel": "『服捨て』スタジオ版56秒ショート",
    },
    {
        "id": "japanese-origins",
        "file": "日本人とは何か_投稿セット.md",
        "title": "覚張隆史『日本人とは何か』",
        "sourceTitle": "参考動画：『日本人とは何か』本要約",
        "sourceUrl": "https://www.youtube.com/watch?v=X6I-ZF4hkfA",
        "updatedAt": "2026年11月21日",
        "personal": "日本人とは何か_個人アカウント用.png",
        "studio": "日本人とは何か_ダンススタジオ用.png",
        "video": "japanese_origins_short/日本人とは何か_ショート動画.mp4",
        "poster": "japanese_origins_short/slides/slide-01.png",
        "videoLabel": "『日本人とは何か』個人版51秒ショート",
        "videoDuration": "51秒",
        "studioVideo": "japanese_origins_studio_short/日本人とは何か_スタジオ版ショート動画.mp4",
        "studioPoster": "japanese_origins_studio_short/slides/slide-01.png",
        "studioVideoLabel": "『日本人とは何か』スタジオ版51秒ショート",
    },
    {
        "id": "cant-live-with-people",
        "file": "人と暮らせない_投稿セット.md",
        "title": "石橋典子『人と暮らせない』",
        "sourceTitle": "参考動画：『人と暮らせない』本要約",
        "sourceUrl": "https://www.youtube.com/watch?v=9Pq1prm-MZ8",
        "updatedAt": "2026年11月21日",
        "personal": "人と暮らせない_個人アカウント用.png",
        "studio": "人と暮らせない_ダンススタジオ用.png",
        "video": "live_alone_short/人と暮らせない_ショート動画.mp4",
        "poster": "live_alone_short/slides/slide-01.png",
        "videoLabel": "『人と暮らせない』個人版60秒ショート",
        "videoDuration": "60秒",
        "studioVideo": "live_alone_studio_short/人と暮らせない_スタジオ版ショート動画.mp4",
        "studioPoster": "live_alone_studio_short/slides/slide-01.png",
        "studioVideoLabel": "『人と暮らせない』スタジオ版60秒ショート",
    },
    {
        "id": "money-life",
        "file": "お金のある人生_投稿セット.md",
        "title": "三浦さやか『「お金のある人生」を叶える習慣』",
        "sourceTitle": "参考動画：『「お金のある人生」を叶える習慣』本要約",
        "sourceUrl": "https://www.youtube.com/watch?v=Z9bs2Gsw20c",
        "updatedAt": "2026年11月20日",
        "personal": "お金のある人生_個人アカウント用.png",
        "studio": "お金のある人生_ダンススタジオ用.png",
        "video": "money_life_short/お金のある人生_ショート動画.mp4",
        "poster": "money_life_short/slides/slide-01.png",
        "videoLabel": "『お金のある人生を叶える習慣』53秒ショート",
        "videoDuration": "53秒",
        "studioVideo": "money_life_studio_short/お金のある人生_スタジオ版ショート動画.mp4",
        "studioPoster": "money_life_studio_short/slides/slide-01.png",
        "studioVideoLabel": "『お金のある人生を叶える習慣』スタジオ版53秒ショート",
    },
    {
        "id": "scientific-job",
        "file": "科学的な適職_投稿セット.md",
        "title": "鈴木祐『新版 科学的な適職』",
        "sourceTitle": "参考動画：『新版 科学的な適職』本要約",
        "sourceUrl": "https://www.youtube.com/watch?v=xROUrM1HRho",
        "updatedAt": "2026年11月19日",
        "personal": "科学的な適職_個人アカウント用.png",
        "studio": "科学的な適職_ダンススタジオ用.png",
        "video": "scientific_job_short/科学的な適職_ショート動画.mp4",
        "poster": "scientific_job_short/slides/slide-01.png",
    },
    {
        "id": "your-life",
        "file": "君だけの人生_投稿セット.md",
        "title": "伊藤羊一『君は、君だけの人生を歩め』",
        "sourceTitle": "参考動画：『君は、君だけの人生を歩め』本要約",
        "sourceUrl": "https://www.youtube.com/watch?v=tmLFOQwR-U8",
        "updatedAt": "2026年11月18日",
        "personal": "君だけの人生_個人アカウント用.png",
        "studio": "君だけの人生_ダンススタジオ用.png",
    },
    {
        "id": "self-axis",
        "file": "自分軸習慣_投稿セット.md",
        "title": "一番ケ瀬瑶子『「やるべきこと」に追われない 自分軸習慣』",
        "sourceTitle": "参考動画：『自分軸習慣』本要約",
        "sourceUrl": "https://www.youtube.com/watch?v=Y77Z3n3z-40",
        "updatedAt": "2026年11月18日",
        "personal": "自分軸習慣_個人アカウント用_詳細版.png",
        "studio": "自分軸習慣_ダンススタジオ用_詳細版.png",
    },
    {
        "id": "is-it-necessary",
        "file": "それって必要_投稿セット.md",
        "title": "『それって、必要？』",
        "sourceTitle": "参考動画：『それって、必要？』本要約",
        "sourceUrl": "https://www.youtube.com/watch?v=l2mxHV-zvQc",
        "updatedAt": "2026年11月18日",
        "personal": "それって必要_個人アカウント用.png",
        "studio": "それって必要_ダンススタジオ用.png",
    },
    {
        "id": "subtraction-thinking",
        "file": "引き算思考_投稿セット.md",
        "title": "ミニマリストTakeru『人生は「引き算」で軽くなる』",
        "sourceTitle": "参考動画：『人生は「引き算」で軽くなる』本要約",
        "sourceUrl": "https://www.youtube.com/watch?v=HXcbklUixQk",
        "updatedAt": "2026年11月18日",
        "personal": "引き算思考_個人アカウント用.png",
        "studio": "引き算思考_ダンススタジオ用.png",
    },
]


def section(text: str, start: str, end: str) -> str:
    match = re.search(
        rf"^## {re.escape(start)}\s*$\n(.*?)(?=^## {re.escape(end)}\s*$)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError(f"Section not found: {start}")
    return match.group(1).strip()


def plain(value: str) -> str:
    value = re.sub(r"^#{3,6} .*$", "", value, flags=re.MULTILINE)
    value = re.sub(r"^[-*] ", "", value, flags=re.MULTILINE)
    return re.sub(r"\n{3,}", "\n\n", value).strip()


def build_post(config: dict) -> dict:
    source = ROOT / "outputs" / config["file"]
    text = source.read_text(encoding="utf-8")
    long_post = plain(section(text, "長文投稿", "約500文字投稿"))
    medium_post = plain(section(text, "約500文字投稿", "X用・140文字以内"))
    x_post = plain(section(text, "X用・140文字以内", "ハッシュタグ候補"))
    image_heading = "画像内テキスト案" if "## 画像内テキスト案" in text else "画像内テキスト"
    hashtag_block = section(text, "ハッシュタグ候補", image_heading)
    hashtags = " ".join(re.findall(r"#\S+", hashtag_block))

    post_asset_dir = ASSET_DIR / config["id"]
    post_asset_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "outputs" / config["personal"], post_asset_dir / "personal.png")
    shutil.copy2(ROOT / "outputs" / config["studio"], post_asset_dir / "studio.png")

    videos = []
    if config.get("video"):
        video_target = post_asset_dir / "short-personal.mp4"
        poster_target = post_asset_dir / "short-personal-poster.png"
        shutil.copy2(ROOT / "outputs" / config["video"], video_target)
        shutil.copy2(ROOT / "outputs" / config["poster"], poster_target)
        videos.append({
            "label": config.get("videoLabel", "『新版 科学的な適職』60秒ショート"),
            "src": f"assets/{config['id']}/short-personal.mp4",
            "poster": f"assets/{config['id']}/short-personal-poster.png",
            "duration": config.get("videoDuration", "55秒"),
        })
    if config.get("studioVideo"):
        studio_video_target = post_asset_dir / "short-studio.mp4"
        studio_poster_target = post_asset_dir / "short-studio-poster.png"
        shutil.copy2(ROOT / "outputs" / config["studioVideo"], studio_video_target)
        shutil.copy2(ROOT / "outputs" / config["studioPoster"], studio_poster_target)
        videos.append({
            "label": config["studioVideoLabel"],
            "src": f"assets/{config['id']}/short-studio.mp4",
            "poster": f"assets/{config['id']}/short-studio-poster.png",
            "duration": config.get("studioVideoDuration", config.get("videoDuration", "53秒")),
        })

    return {
        "id": config["id"],
        "title": config["title"],
        "sourceTitle": config["sourceTitle"],
        "sourceUrl": config["sourceUrl"],
        "updatedAt": config["updatedAt"],
        "longPost": long_post,
        "mediumPost": medium_post,
        "xPost": x_post,
        "hashtags": hashtags,
        "images": [
            {"label": "個人アカウント用", "src": f"assets/{config['id']}/personal.png"},
            {"label": "ダンススタジオ用", "src": f"assets/{config['id']}/studio.png"},
        ],
        "video": videos[0] if videos else None,
        "videos": videos,
    }


payload = {"latest": POSTS[0]["id"], "items": [build_post(config) for config in POSTS]}
OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(OUTPUT)
for item in payload["items"]:
    print(item["id"], len(item["longPost"]), len(item["mediumPost"]), len(item["xPost"]))
