# Subtitle Merger (submerger.py)

A Python tool designed to merge dual-language subtitles with flexible styling options and customization. This tool is particularly useful for language learners who want to improve comprehension by watching videos with two subtitle tracks—one for their native language and one for the target language. By seeing the translations side-by-side or consecutively, learners can associate words and phrases more effectively.

## 📥 Installation

### Clone the Repository

```bash
git clone https://github.com/faridzfr/submerger.git
cd submerger
```

### Or Download the ZIP File

1. Go to the repository page and click on the **Code** button.
2. Select **Download ZIP**.
3. Extract the ZIP file to your desired location.
4. Open a terminal in the extracted folder.

### Install Dependencies

Ensure you have Python installed. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

## 🚀 Basic Usage

### For Single Files

```bash
# Side-by-side merge
python submerger.py "en/Episode 01.ass" "ja/Episode 01.srt" -m side -o "output/Merged Episode 01.ass" --fontsize 22 --lang1 English --lang2 Japanese

# Bottom merge
python submerger.py "en/Episode 01.srt" "ja/Episode 01.ass" -m consecutive -o "output/Merged Episode 01.ass" --fontsize 24
```

### For Bulk Processing

```bash
# Side-by-side (all files)
python submerger.py en/ ja/ -m side -o output/ --fontsize 20 --lang1 English --lang2 Japanese

# Bottom (all files)
python submerger.py en/ ja/ -m consecutive -o output/ --fontsize 24
```

## 🛠️ All Arguments

| Argument       | Description                            | Default    | Required |
| -------------- | -------------------------------------- | ---------- | -------- |
| `sub1`         | First subtitle file/folder (English)   | -          | Yes      |
| `sub2`         | Second subtitle file/folder (Japanese) | -          | Yes      |
| `-o, --output` | Output path                            | `output/`  | No       |
| `-m, --mode`   | `side` or `consecutive`                | `side`     | No       |
| `--lang1`      | First language label                   | `English`  | No       |
| `--lang2`      | Second language label                  | `Japanese` | No       |
| `--fontsize`   | Base font size (overrides custom)      | `24`       | No       |

## 🎨 Customization

### Configuration Files

Ensure these files exist in the script directory; create them if they don't:

- `default_style.txt` - Defines subtitle appearance
- `script_info.txt` - Sets script metadata

### File Format Examples

`default_style.txt`:

```ini
fontname=Arial
fontsize=22
primarycolor=255,255,255,0  # RGBA
alignment=2  # 1=Left, 3=Right, 2=Center
outline=1.5
```

`script_info.txt`:

```ini
PlayResX=1280
PlayResY=720
ScaledBorderAndShadow=no
```

### Features

- Merge single files or batches
- Persistent custom styles
- Command-line fontsize overrides
- Detailed error reporting
- Customization prompts once at the start for batch processing
- Resets customization prompts for single file operations

## 📝 Notes

- Automatically creates the output folder if it doesn't exist
- Keeps original timestamps intact for accurate synchronization
- Uses natural sorting for batch file matching
- Prompts for confirmation if file names don't match
- Output files are saved in .ASS format for rich styling options

## 🔗 Resources

- [Tokyo Insider](https://www.tokyoinsider.com/) - Anime Downloads
- [Kitsunekko](https://kitsunekko.net/) - Subtitle Archives

