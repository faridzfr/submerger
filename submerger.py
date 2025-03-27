import os
import argparse
from pathlib import Path
import chardet
import pysrt
import pysubs2
from natsort import natsorted

# Global variables to track customization preferences
USE_CUSTOM_STYLE = None          # Flag for using custom style settings
USE_CUSTOM_SCRIPT_INFO = None    # Flag for using custom script info

def detect_encoding(file_path):
    """
    Detect the text encoding of a file using chardet.
    Returns the most probable encoding as a string.
    """
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    return chardet.detect(raw_data)['encoding']

def load_subtitle_file(file_path):
    """
    Load subtitle file and convert to pysubs2 format.
    Supports both .srt and .ass formats.
    Returns SSAFile object.
    """
    encoding = detect_encoding(file_path)
    ext = Path(file_path).suffix.lower()

    if ext == '.srt':
        subs = pysrt.open(file_path, encoding=encoding)
        subs2 = pysubs2.SSAFile()
        for sub in subs:
            start = sub.start.ordinal
            end = sub.end.ordinal
            text = sub.text.replace('\n', '\\N')
            subs2.append(pysubs2.SSAEvent(start=start, end=end, text=text))
        return subs2
    elif ext == '.ass':
        return pysubs2.load(file_path, encoding=encoding)
    else:
        raise ValueError(f"Unsupported subtitle format: {ext}")

def prompt_for_customization():
    """
    Prompt user once to use customization files if they exist.
    Sets global USE_CUSTOM_STYLE and USE_CUSTOM_SCRIPT_INFO flags.
    """
    global USE_CUSTOM_STYLE, USE_CUSTOM_SCRIPT_INFO
    
    if os.path.exists("default_style.txt"):
        print("\nCustom style file (default_style.txt) found!")
        USE_CUSTOM_STYLE = input("Use custom style settings for all files? (Y/n): ").strip().lower() in ('', 'y', 'yes')
    
    if os.path.exists("script_info.txt"):
        print("\nCustom script info file (script_info.txt) found!")
        USE_CUSTOM_SCRIPT_INFO = input("Use custom script info for all files? (Y/n): ").strip().lower() in ('', 'y', 'yes')

def get_custom_style():
    """
    Load custom style settings from default_style.txt if enabled.
    Returns dictionary of style properties or None if not used.
    """
    if not USE_CUSTOM_STYLE:
        return None
        
    custom_style = {}
    try:
        with open("default_style.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    custom_style[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error reading custom style: {e}")
        return None
    return custom_style

def get_custom_script_info():
    """
    Load custom script info from script_info.txt if enabled.
    Returns dictionary of script info properties or None if not used.
    """
    if not USE_CUSTOM_SCRIPT_INFO:
        return None
        
    custom_script_info = {}
    try:
        with open("script_info.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    custom_script_info[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error reading script info: {e}")
        return None
    return custom_script_info

def create_default_style(fontsize=24):
    """
    Create subtitle style with either custom or default settings.
    Takes optional fontsize parameter that overrides custom settings.
    Returns SSAStyle object.
    """
    custom_style = get_custom_style() if USE_CUSTOM_STYLE else None
    
    style = pysubs2.SSAStyle()
    
    if custom_style:
        try:
            # Apply all custom style properties with fallback to defaults
            style.fontname = custom_style.get("fontname", "Roboto Medium")
            style.fontsize = int(custom_style.get("fontsize", fontsize))
            
            def parse_color(color_str):
                """Helper to convert RGBA string to Color object"""
                parts = color_str.split(",")
                if len(parts) == 4:
                    return pysubs2.Color(*map(int, parts))
                return pysubs2.Color(255, 255, 255, 0)
            
            # Set color properties
            style.primarycolor = parse_color(custom_style.get("primarycolor", "255,255,255,0"))
            style.secondarycolor = parse_color(custom_style.get("secondarycolor", "0,0,255,0"))
            style.outlinecolor = parse_color(custom_style.get("outlinecolor", "19,7,2,0"))
            style.backcolor = parse_color(custom_style.get("backcolor", "0,0,0,0"))
            
            # Set various style properties
            style.bold = bool(int(custom_style.get("bold", "0")))
            style.italic = bool(int(custom_style.get("italic", "0")))
            style.underline = bool(int(custom_style.get("underline", "0")))
            style.strikeout = bool(int(custom_style.get("strikeout", "0")))
            style.scalex = float(custom_style.get("scalex", "100"))
            style.scaley = float(custom_style.get("scaley", "100"))
            style.spacing = float(custom_style.get("spacing", "0"))
            style.angle = float(custom_style.get("angle", "0"))
            style.borderstyle = int(custom_style.get("borderstyle", "1"))
            style.outline = float(custom_style.get("outline", "1.3"))
            style.shadow = float(custom_style.get("shadow", "0"))
            style.alignment = int(custom_style.get("alignment", "2"))
            style.marginl = int(custom_style.get("marginl", "20"))
            style.marginr = int(custom_style.get("marginr", "20"))
            style.marginv = int(custom_style.get("marginv", "23"))
            style.encoding = int(custom_style.get("encoding", "1"))
        except (ValueError, AttributeError) as e:
            print(f"Error applying custom style: {e}. Using defaults.")
    else:
        # Default style settings
        style.fontname = "Roboto Medium"
        style.fontsize = fontsize
        style.primarycolor = pysubs2.Color(255, 255, 255, 0)
        style.secondarycolor = pysubs2.Color(0, 0, 255, 0)
        style.outlinecolor = pysubs2.Color(19, 7, 2, 0)
        style.backcolor = pysubs2.Color(0, 0, 0, 0)
        style.bold = False
        style.italic = False
        style.underline = False
        style.strikeout = False
        style.scalex = 100
        style.scaley = 100
        style.spacing = 0
        style.angle = 0
        style.borderstyle = 1
        style.outline = 1.3
        style.shadow = 0
        style.alignment = 2
        style.marginl = 20
        style.marginr = 20
        style.marginv = 23
        style.encoding = 1
    
    return style

def set_script_info(ssa_file):
    """
    Set script metadata (header info) for output file.
    Uses custom settings if enabled, otherwise default values.
    """
    custom_script_info = get_custom_script_info() if USE_CUSTOM_SCRIPT_INFO else None
    
    if custom_script_info:
        ssa_file.info.update(custom_script_info)
    else:
        ssa_file.info.update({
            "PlayResX": "640",
            "PlayResY": "360",
            "PlayDepth": "0",
            "ScriptType": "v4.00+",
            "Collisions": "Normal",
            "ScaledBorderAndShadow": "yes"
        })

def merge_side_by_side(subs1, subs2, output_path, lang1="English", lang2="Japanese", fontsize=24):
    """
    Merge two subtitle files side-by-side (left/right layout).
    subs1: Left subtitle (SSAFile)
    subs2: Right subtitle (SSAFile)
    output_path: Path for merged file
    lang1/lang2: Language labels
    fontsize: Base font size
    """
    merged = pysubs2.SSAFile()
    set_script_info(merged)
    
    # Create base style and left/right variants
    default_style = create_default_style(fontsize)
    merged.styles["Default"] = default_style
    
    left_style = pysubs2.SSAStyle()
    left_style.__dict__.update(default_style.__dict__)
    left_style.alignment = 1  # Bottom-left
    left_style.marginl = 20
    left_style.marginr = 0
    merged.styles["Left"] = left_style
    
    right_style = pysubs2.SSAStyle()
    right_style.__dict__.update(default_style.__dict__)
    right_style.alignment = 3  # Bottom-right
    right_style.marginl = 0
    right_style.marginr = 20
    merged.styles["Right"] = right_style
    
    # Add language labels
    label_duration = 1000  # 1 second
    merged.append(pysubs2.SSAEvent(
        start=0, end=label_duration, text=lang1, style="Left"))
    merged.append(pysubs2.SSAEvent(
        start=0, end=label_duration, text=lang2, style="Right"))
    
    # Combine and sort all events
    all_events = []
    for event in subs1.events:
        event.style = "Left"
        all_events.append(event)
    
    for event in subs2.events:
        event.style = "Right"
        all_events.append(event)
    
    all_events.sort(key=lambda x: x.start)
    
    # Add sorted events to output
    for event in all_events:
        merged.append(event)
    
    # Save output file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merged.save(output_path)
    print(f"Saved: {output_path}")

def merge_consecutive(subs1, subs2, output_path, fontsize=24):
    """
    Merge two subtitle files consecutively (bottom layout).
    subs1: First subtitle (SSAFile)
    subs2: Second subtitle (SSAFile)
    output_path: Path for merged file
    fontsize: Base font size
    """
    merged = pysubs2.SSAFile()
    set_script_info(merged)
    
    # Create base style and bottom variant
    default_style = create_default_style(fontsize)
    merged.styles["Default"] = default_style
    
    bottom_style = pysubs2.SSAStyle()
    bottom_style.__dict__.update(default_style.__dict__)
    bottom_style.alignment = 2  # Bottom-center
    merged.styles["Bottom"] = bottom_style
    
    # Add all events with bottom style
    for event in subs1.events:
        event.style = "Bottom"
        merged.append(event)
    
    for event in subs2.events:
        event.style = "Bottom"
        merged.append(event)
    
    # Sort events by start time
    merged.events.sort(key=lambda x: x.start)
    
    # Save output file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merged.save(output_path)
    print(f"Saved: {output_path}")

def get_matching_pairs(folder1, folder2):
    """
    Match subtitle files from two folders automatically or via user selection.
    Returns list of (file1, file2) tuples.
    """
    files1 = natsorted([f for f in os.listdir(folder1) if f.lower().endswith(('.srt', '.ass'))])
    files2 = natsorted([f for f in os.listdir(folder2) if f.lower().endswith(('.srt', '.ass'))])
    
    if len(files1) != len(files2):
        print(f"Warning: Different number of files in folders ({len(files1)} vs {len(files2)})")
    
    pairs = []
    for i, file1 in enumerate(files1):
        print(f"\nFile {i+1}: {file1}")
        
        # Try auto-matching first
        matching_index = None
        for j, file2 in enumerate(files2):
            if file1.split('.')[0] in file2 or file2.split('.')[0] in file1:
                matching_index = j
                break
        
        if matching_index is not None and len(files2) > matching_index:
            print(f"Auto-matched with: {files2[matching_index]}")
            confirm = input("Is this correct? (Y/n): ").strip().lower()
            if confirm in ('', 'y', 'yes'):
                pairs.append((os.path.join(folder1, file1), 
                            os.path.join(folder2, files2[matching_index])))
                continue
        
        # Manual selection if auto-match fails or is rejected
        print("\nAvailable matching files:")
        for j, file2 in enumerate(files2):
            print(f"{j+1}: {file2}")
        
        while True:
            try:
                selection = input(f"Select matching file for {file1} (1-{len(files2)}): ").strip()
                if not selection:
                    continue
                selection = int(selection) - 1
                if 0 <= selection < len(files2):
                    pairs.append((os.path.join(folder1, file1), 
                                os.path.join(folder2, files2[selection])))
                    break
                else:
                    print("Invalid selection. Try again.")
            except ValueError:
                print("Please enter a number.")
    
    return pairs

def bulk_merge(folder1, folder2, output_folder, mode="side", lang1="English", lang2="Japanese", fontsize=24):
    """
    Process all matching subtitle files from two folders.
    Handles customization prompts once at start.
    """
    # Prompt for customization preferences once
    prompt_for_customization()
    
    # Get matched file pairs
    pairs = get_matching_pairs(folder1, folder2)
    
    # Get base output name
    base_name = input("\nEnter base name for all files (leave blank to use original names): ").strip()
    
    # Process each pair
    for i, (file1, file2) in enumerate(pairs):
        subs1 = load_subtitle_file(file1)
        subs2 = load_subtitle_file(file2)
        
        # Generate output filename
        if base_name:
            ep_num = str(i+1).zfill(2)  # Zero-padded episode number
            output_name = f"{base_name} - {ep_num}.ass"
        else:
            original_name = os.path.splitext(os.path.basename(file1))[0]
            output_name = f"{original_name}.ass"
        
        output_path = os.path.join(output_folder, output_name)
        
        # Merge based on selected mode
        if mode == "side":
            merge_side_by_side(subs1, subs2, output_path, lang1, lang2, fontsize)
        else:
            merge_consecutive(subs1, subs2, output_path, fontsize)

def main():
    """
    Main entry point for the script.
    Handles command line arguments and initiates processing.
    """
    # Notify about customization files if present
    if os.path.exists("default_style.txt") or os.path.exists("script_info.txt"):
        print("\nCustomization files detected in current directory!")
        print("You can customize the subtitle appearance by editing:")
        if os.path.exists("default_style.txt"):
            print("- default_style.txt (for subtitle styling)")
        if os.path.exists("script_info.txt"):
            print("- script_info.txt (for script metadata)")
        print("\nThe script will prompt to use these files when processing begins.\n")

    # Set up command line argument parser
    parser = argparse.ArgumentParser(
        description="Merge two subtitle files for language learning.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("sub1", nargs='?', help="First subtitle file or folder (.srt or .ass)")
    parser.add_argument("sub2", nargs='?', help="Second subtitle file or folder (.srt or .ass)")
    parser.add_argument("-o", "--output", default="output", 
                       help="Output file or folder path")
    parser.add_argument("-m", "--mode", choices=["side", "consecutive"], default="side",
                       help="Merge mode: side-by-side or consecutive")
    parser.add_argument("--lang1", default="English", 
                       help="Language label for first subtitle")
    parser.add_argument("--lang2", default="Japanese", 
                       help="Language label for second subtitle")
    parser.add_argument("--fontsize", type=int, default=24,
                       help="Default font size for subtitles")
    
    args = parser.parse_args()
    
    # Process based on input type (files or folders)
    if args.sub1 and args.sub2:
        if os.path.isdir(args.sub1) and os.path.isdir(args.sub2):
            bulk_merge(args.sub1, args.sub2, args.output, args.mode, args.lang1, args.lang2, args.fontsize)
        elif os.path.isfile(args.sub1) and os.path.isfile(args.sub2):
            # Reset customization prompts for single file operation
            global USE_CUSTOM_STYLE, USE_CUSTOM_SCRIPT_INFO
            USE_CUSTOM_STYLE = None
            USE_CUSTOM_SCRIPT_INFO = None
            
            subs1 = load_subtitle_file(args.sub1)
            subs2 = load_subtitle_file(args.sub2)
            
            if args.mode == "side":
                merge_side_by_side(subs1, subs2, args.output, args.lang1, args.lang2, args.fontsize)
            else:
                merge_consecutive(subs1, subs2, args.output, args.fontsize)
        else:
            print("Error: Both inputs must be either files or folders")
    else:
        print("Error: Please provide two subtitle files or folders to merge")

if __name__ == "__main__":
    main()