param(
    [string]$OutputFile = "C:\Users\kurro\.gemini\antigravity\scratch\haru-post-tool-ai-handoff-20261121\outputs\one_hundred_million_narration.wav"
)

Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice("Microsoft Haruka Desktop")
$synth.Rate = 1

$text = "今回ご紹介したいのは、橘玲さんと大橋弘祐さんの『難しいことはわかりませんが、1億円貯める方法を教えてください！』です。" +
"普通の会社員が資産1億円を築く道は、実はたった1つの方程式に集約されます。" +
"それは、収入から支出を引いたお金を、複利で運用し続けること。" +
"まず、会社員の最大の武器である人的資本を活かして、安定した給与を稼ぐ。" +
"次に、不要な民間保険や見栄の浪費、固定費を徹底的に削り、浮いた資金を確保する。" +
"そして、手数料が最安の全世界株式インデックスに、新NISAで毎月自動で積み立てて、あとは放置する。" +
"資産1億円があれば、年間400万円の不労所得が生まれ、やりたいことを自由に選べる人生が手に入ります。" +
"今日から、不要な保険を見直し、インデックス投資への一歩を踏み出してみませんか？"

$synth.SetOutputToWaveFile($OutputFile)
$synth.Speak($text)
$synth.Dispose()

Write-Output "Successfully generated: $OutputFile"
