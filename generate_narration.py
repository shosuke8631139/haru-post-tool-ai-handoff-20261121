import asyncio
import edge_tts
import imageio_ffmpeg
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

NARRATION_TEXT = (
    "今回ご紹介したいのは、橘玲さんと大橋弘祐さんの『難しいことはわかりませんが、1億円貯める方法を教えてください！』です。"
    "普通の会社員が資産1億円を築く道は、実はたった1つの方程式に集約されます。"
    "それは、収入から支出を引いたお金を、複利で運用し続けること。"
    "まず、会社員の最大の武器である人的資本を活かして、安定した給与を稼ぐ。"
    "次に、不要な民間保険や見栄の浪費、固定費を徹底的に削り、浮いた資金を確保する。"
    "そして、手数料が最安の全世界株式インデックスに、新NISAで毎月自動で積み立てて、あとは放置する。"
    "資産1億円があれば、年間400万円の不労所得が生まれ、やりたいことを自由に選べる人生が手に入ります。"
    "今日から、不要な保険を見直し、インデックス投資への一歩を踏み出してみませんか？"
)


async def synthesize(voice: str = "ja-JP-NanamiNeural", rate: str = "+14%", output_stem: str = "one_hundred_million_narration"):
    mp3_path = OUTPUTS / f"{output_stem}.mp3"
    wav_path = OUTPUTS / f"{output_stem}.wav"

    print(f"Generating narration with {voice} (rate={rate})...")
    comm = edge_tts.Communicate(NARRATION_TEXT, voice, rate=rate)
    await comm.save(str(mp3_path))

    # Convert to 24kHz / 16-bit mono PCM wav for video alignment
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
    # 1. デフォルト: ja-JP-NanamiNeural (穏やかで聞き取りやすい女性ナレーター・完全無料・クレジット不要)
    await synthesize("ja-JP-NanamiNeural", rate="+14%", output_stem="one_hundred_million_narration")
    # バックアップ / 比較用
    await synthesize("ja-JP-NanamiNeural", rate="+14%", output_stem="one_hundred_million_narration_nanami")
    await synthesize("ja-JP-KeitaNeural", rate="+8%", output_stem="one_hundred_million_narration_keita")


if __name__ == "__main__":
    asyncio.run(main())
