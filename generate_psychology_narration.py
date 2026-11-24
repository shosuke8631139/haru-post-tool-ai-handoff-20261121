import asyncio
import edge_tts
import imageio_ffmpeg
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

NARRATION_TEXT_PERSONAL = (
    "今回ご紹介したいのは、モーガン・ハウセルさんの『サイコロジー・オブ・マネー』です。"
    "お金が人生にもたらす最大の価値、それは『自由』です。"
    "好きな時に、好きな人と、好きなだけ過ごせること。"
    "お金持ちになれるかどうかを分けるのは、頭の良さではなく日々の『感情のコントロール』です。"
    "投資で最も重要なアドバイスは、『黙ってじっと待つこと』。"
    "投資の神様バフェットの富の99%は、50歳を過ぎてから築かれました。"
    "市場の暴落や不安は、罰金ではなくリターンを得るための『入場料』です。"
    "見栄の消費を手放し、時間を最大の味方にして、自分らしい自由を手に入れませんか？"
)

NARRATION_TEXT_STUDIO = (
    "今回ご紹介したいのは、世界中で大ベストセラーの『サイコロジー・オブ・マネー』です！"
    "お金が私たちにもたらす最高の配当、それは『自由』です。"
    "自分の時間を自分でコントロールできること。"
    "成功を分けるのは、高度な知識ではなく『感情のコントロール』と身軽さです。"
    "投資の最重要ルールは、『時間を味方にしてじっと待つこと』。"
    "富の99%は、複利の力で時間をかけて育ちます。"
    "一時的な不安や下落は、夢を叶えるための『入場料』！"
    "見栄を手放し、時間を味方につけて、自由で身軽な未来を創りましょう！"
)


async def synthesize(text: str, voice: str, rate: str, output_stem: str):
    mp3_path = OUTPUTS / f"{output_stem}.mp3"
    wav_path = OUTPUTS / f"{output_stem}.wav"

    print(f"Generating narration: {output_stem} with {voice} (rate={rate})...")
    comm = edge_tts.Communicate(text, voice, rate=rate)
    await comm.save(str(mp3_path))

    subprocess.run(
        [
            ffmpeg, "-y", "-i", str(mp3_path),
            "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le",
            str(wav_path)
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print(f"Saved: {wav_path}")
    return wav_path


async def main():
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    # 個人版（落ち着いたナレーション）
    await synthesize(NARRATION_TEXT_PERSONAL, "ja-JP-NanamiNeural", "+12%", "psychology_of_money_narration_personal")
    # スタジオ版（明るく元気なナレーション）
    await synthesize(NARRATION_TEXT_STUDIO, "ja-JP-NanamiNeural", "+14%", "psychology_of_money_narration_studio")


if __name__ == "__main__":
    asyncio.run(main())
