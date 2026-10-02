import argparse
from collections import Counter
from pathlib import Path

import jieba
import matplotlib.pyplot as plt
from matplotlib import font_manager


ENGLISH_GLOSSES = {
    "了": "completed action / change",
    "的": "possessive / modifier particle",
    "我": "I / me",
    "他": "he / him",
    "道": "say (literary)",
    "说": "say / speak",
    "你": "you",
    "也": "also",
    "是": "be / is",
    "又": "again",
    "着": "ongoing aspect particle",
    "去": "go / leave",
    "宝玉": "Baoyu (name)",
    "来": "come",
    "不": "not",
    "便": "then / thereupon",
    "在": "at / in",
    "人": "person / people",
    "都": "all",
    "有": "have / there is",
}


def save_top_words(counts: Counter[str], output_path: Path) -> None:
    top_words = counts.most_common(20)
    labels = [
        f"{word} — {ENGLISH_GLOSSES.get(word, 'translation unavailable')}"
        for word, _ in reversed(top_words)
    ]
    frequencies = [count for _, count in reversed(top_words)]

    font_path = Path.home() / ".local/share/fonts/NotoSansSC-VF.ttf"
    if font_path.exists():
        font_manager.fontManager.addfont(font_path)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=font_path).get_name()
    figure, axis = plt.subplots(figsize=(11, 8))
    bars = axis.barh(labels, frequencies, color="#287a72")
    axis.bar_label(bars, padding=4, fmt="{:,.0f}")
    axis.set_title("Top 20 Word Frequencies / 高频词前20位")
    axis.set_xlabel("Occurrences / 出现次数")
    axis.set_ylabel("Word / 词语")
    axis.spines[["top", "right"]].set_visible(False)
    figure.tight_layout()
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def count_words(path: Path) -> Counter[str]:
    text = path.read_text(encoding="utf-8")
    words = (word.strip() for word in jieba.cut(text))
    return Counter(word for word in words if word and any(char.isalnum() for char in word))


def main() -> None:
    parser = argparse.ArgumentParser(description="Count words in a Chinese text file.")
    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("红楼梦.txt"),
        help="UTF-8 text file to count (default: 红楼梦.txt)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="PNG output path (default: top_20_word_counts.png beside the input file)",
    )
    args = parser.parse_args()

    counts = count_words(args.file)
    for word, count in counts.most_common():
        print(f"{word}\t{count}")

    output_path = args.output or args.file.with_name("top_20_word_counts.png")
    save_top_words(counts, output_path)
    print(f"Saved top-20 chart to {output_path}")


if __name__ == "__main__":
    main()