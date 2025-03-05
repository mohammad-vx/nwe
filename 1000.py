# أضف هذا الكود في بداية الملف (قبل أي استخدام للـ logging)
import sys
import logging  # إضافة استيراد وحدة logging

# إضافة وحدة pyaudioop مزيفة إلى sys.modules
class MockAudioop:
    def avg(self, *args): return 0
    def avgpp(self, *args): return 0
    def bias(self, *args): return b''
    def cross(self, *args): return 0
    def findfactor(self, *args): return 0
    def findfit(self, *args): return 0
    def findmax(self, *args): return 0
    def getsample(self, *args): return 0
    def lin2lin(self, *args): return b''
    def lin2ulaw(self, *args): return b''
    def minmax(self, *args): return 0, 0
    def mul(self, *args): return b''
    def ratecv(self, *args): return b'', None
    def reverse(self, *args): return b''
    def rms(self, *args): return 0
    def tomono(self, *args): return b''
    def tostereo(self, *args): return b''
    def ulaw2lin(self, *args): return b''
    def add(self, *args): return b''
    def adpcm2lin(self, *args): return b''
    def alaw2lin(self, *args): return b''
    def lin2adpcm(self, *args): return b''
    def lin2alaw(self, *args): return b''
    def max(self, *args): return 0

# تسجيل الوحدة المزيفة
sys.modules['pyaudioop'] = MockAudioop()

# باقي الاستيرادات
import os
import tempfile
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any, Union
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import sys
import logging
import os
import tempfile
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any, Union
try:
    import pyaudioop
except ImportError:
    # لن نستخدم الوحدة المزيفة بنفس الطريقة السابقة
    pass

# إعداد التسجيل (Logging)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# باقي الاستيرادات
from moviepy.video.io.VideoFileClip import VideoFileClip
try:
    from pydub import AudioSegment
    from pydub.silence import detect_nonsilent
    PYDUB_AVAILABLE = True
except ImportError:
    logger.warning("pydub غير متاحة، سيتم استخدام بديل للكشف عن الصمت")
    PYDUB_AVAILABLE = False

# تعريف الفئات والدوال كما هي...
@dataclass
class VideoSegment:
    start: float
    end: float
    duration: float
    peak_count: int

@dataclass
class Settings:
    video_path: str = ""
    subtitle_file: Optional[str] = None
    output_folder: str = "output"
    min_duration: float = 30.0
    max_duration: float = 90.0
    crop_x: int = 390
    crop_ratio: str = "9/16"
    silence_thresh: int = -50
    crf: int = 23
    video_bitrate: str = "1M"

@dataclass
class VideoDetails:
    duration: float
    width: int
    height: int
    fps: float


# إعداد التسجيل (Logging)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(المة) - %(message)s')
logger = logging.getLogger(__name__)

# باقي الكود كما هو...

# إعداد التسجيل (Logging)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(المة) - %(message)s')
logger = logging.getLogger(__name__)

# ==================================================
# Data Classes
# ==================================================
@dataclass
class VideoSegment:
    start: float
    end: float
    duration: float
    peak_count: int

@dataclass
class Settings:
    video_path: str = ""
    subtitle_file: Optional[str] = None
    output_folder: str = "output"
    min_duration: float = 30.0
    max_duration: float = 90.0
    crop_x: int = 390
    crop_ratio: str = "9/16"
    silence_thresh: int = -50
    crf: int = 23
    video_bitrate: str = "1M"

@dataclass
class Subtitle:
    index: int
    start: str
    end: str
    text: str = ""

@dataclass
class VideoDetails:
    duration: float
    width: int
    height: int
    fps: float

# ==================================================
# Helper Functions
# ==================================================
def get_unique_filename(output_folder: str, base_name: str, extension: str = "mp4") -> str:
    """Generate a unique filename in the output folder."""
    counter = 1
    while True:
        output_path = os.path.join(output_folder, f"{base_name}_{counter}.{extension}")
        if not os.path.exists(output_path):
            return output_path
        counter += 1

def print_section_header(title: str) -> None:
    """Print a formatted section header to the log."""
    logger.info("\n" + "=" * 50)
    logger.info(f"  {title}")
    logger.info("=" * 50)

def format_time(seconds: float) -> str:
    """تنسيق الثواني كـ HH:MM:SS."""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

# تنفيذ الخاصية 3: تعديل مقطع موجود
def edit_existing_segment() -> None:
    """Edit an existing processed video segment."""
    processed_videos = load_processed_videos()
    video_info = show_processed_videos_menu(processed_videos)
    if not video_info:
        return

    video_path = video_info['video_path']
    start_time = video_info['start_time']
    end_time = video_info['end_time']
    subtitle_file = video_info.get('subtitle_file')
    crop_x = video_info.get('crop_x', 390)
    crop_ratio = video_info.get('crop_ratio', "9/16")
    crf = video_info.get('crf', 23)
    video_bitrate = video_info.get('video_bitrate', "1M")

    # Get video details for duration checks
    video_details = get_video_details(video_path)
    if not video_details:
        return

    # Track if any changes were made
    changes_made = False
    
    # Time adjustment options
    print_section_header("Time Adjustment Options")
    logger.info("1. Add time to video")
    logger.info("2. Cut time from video")
    logger.info("3. No time adjustments")
    
    time_choice = input("\nYour choice (1-3): ").strip()
    
    if time_choice in ['1', '2']:
        changes_made = True
        if time_choice == '1':
            print("\nAdd time from:")
            logger.info("1. Beginning")
            logger.info("2. End")
            logger.info("3. Both")
            
            add_choice = input("\nYour choice (1-3): ").strip()
            
            if add_choice in ['1', '3']:
                while True:
                    try:
                        time_to_add = float(input("\nTime to add at beginning (seconds): "))
                        if start_time - time_to_add >= 0:
                            start_time -= time_to_add
                            break
                        else:
                            logger.warning("Cannot add more time than available at beginning.")
                    except ValueError:
                        logger.warning("Please enter a valid number.")
            
            if add_choice in ['2', '3']:
                while True:
                    try:
                        time_to_add = float(input("\nTime to add at end (seconds): "))
                        if end_time + time_to_add <= video_details.duration:
                            end_time += time_to_add
                            break
                        else:
                            logger.warning("Cannot add more time than available at end.")
                    except ValueError:
                        logger.warning("Please enter a valid number.")
        
        else:  # Cut time
            print("\nCut time from:")
            logger.info("1. Beginning")
            logger.info("2. End")
            logger.info("3. Both")
            logger.info("4. Middle")
            
            cut_choice = input("\nYour choice (1-4): ").strip()
            
            if cut_choice in ['1', '3']:
                while True:
                    try:
                        time_to_cut = float(input("\nTime to cut from beginning (seconds): "))
                        if time_to_cut < (end_time - start_time):
                            start_time += time_to_cut
                            break
                        else:
                            logger.warning("Cannot cut more time than segment duration.")
                    except ValueError:
                        logger.warning("Please enter a valid number.")
            
            if cut_choice in ['2', '3']:
                while True:
                    try:
                        time_to_cut = float(input("\nTime to cut from end (seconds): "))
                        if time_to_cut < (end_time - start_time):
                            end_time -= time_to_cut
                            break
                        else:
                            logger.warning("Cannot cut more time than segment duration.")
                    except ValueError:
                        logger.warning("Please enter a valid number.")
            
            if cut_choice == '4':
                while True:
                    try:
                        cut_start = float(input("\nStart time of cut (seconds from segment start): "))
                        cut_end = float(input("End time of cut (seconds from segment start): "))
                        if 0 <= cut_start < cut_end <= (end_time - start_time):
                            new_duration = (end_time - start_time) - (cut_end - cut_start)
                            if new_duration >= 1:  # Minimum 1 second duration
                                end_time = start_time + new_duration
                                break
                        logger.warning("Invalid cut times. Please ensure proper range.")
                    except ValueError:
                        logger.warning("Please enter valid numbers.")

    # Crop settings
    print_section_header("Video Settings")
    edit_video = input("Edit video crop settings? (1/y or 0/n): ").lower() in ['1', 'y']
    if edit_video:
        new_crop_x = input(f"Crop X (default: {crop_x}, press Enter to keep): ").strip()
        if new_crop_x and new_crop_x != str(crop_x):
            try:
                crop_x = int(new_crop_x)
                changes_made = True
            except ValueError:
                logger.warning("Invalid input. Keeping current value.")
        
        new_crop_ratio = input(f"Crop ratio (default: {crop_ratio}, press Enter to keep): ").strip()
        if new_crop_ratio and new_crop_ratio != crop_ratio:
            crop_ratio = new_crop_ratio
            changes_made = True

    # Subtitle settings
    add_subtitles = input("Edit/Add subtitles? (1/y or 0/n): ").lower() in ['1', 'y']
    if add_subtitles:
        changes_made = True

    # Only process if changes were made
    if changes_made:
        segments = [VideoSegment(
            start=start_time,
            end=end_time,
            duration=end_time - start_time,
            peak_count=1
        )]

        process_selected_segments(video_path, segments, Settings(
            video_path=video_path,
            subtitle_file=subtitle_file,
            output_folder=os.path.dirname(video_info['output_path']),
            crop_x=crop_x,
            crop_ratio=crop_ratio,
            crf=crf,
            video_bitrate=video_bitrate
        ), edit_video, add_subtitles)
    else:
        logger.info("No changes were made. Skipping video processing.")

def parse_time_input(time_input: str) -> float:
    """Parse time input in either HH:MM:SS format or seconds."""
    if ':' in time_input:
        h, m, s = map(int, time_input.split(':'))
        return h * 3600 + m * 60 + s
    return float(time_input)

# ==================================================
# SRT Processing Functions
# ==================================================
def parse_srt(subtitle_file: str) -> List[Subtitle]:
    """Parse an SRT file into a list of Subtitle objects."""
    subtitles = []
    try:
        with open(subtitle_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        logger.error(f"Subtitle file not found: {subtitle_file}")
        return []

    current_subtitle = None
    for line in lines:
        line = line.strip()
        if line.isdigit():
            if current_subtitle:
                subtitles.append(current_subtitle)
            current_subtitle = Subtitle(index=int(line), start="", end="", text="")
        elif '-->' in line and current_subtitle:
            start, end = line.split(' --> ')
            current_subtitle.start = start.replace(',', '.')
            current_subtitle.end = end.replace(',', '.')
        elif line and current_subtitle:
            current_subtitle.text += line + " "
    
    if current_subtitle:
        subtitles.append(current_subtitle)
    
    return subtitles

def time_to_seconds(time_str: str) -> float:
    """Convert SRT time format to seconds."""
    hh, mm, ss = time_str.split(':')
    ss, ms = ss.split('.')
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000

def seconds_to_srt_time(seconds: float) -> str:
    """Convert seconds to SRT time format."""
    ms = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    hh = seconds // 3600
    mm = (seconds % 3600) // 60
    ss = seconds % 60
    return f"{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}"

def filter_subtitles(subtitles: List[Subtitle], start_time: float, end_time: float) -> List[Subtitle]:
    """Filter subtitles to match a specific time range and adjust timings."""
    filtered = []
    for sub in subtitles:
        sub_start = time_to_seconds(sub.start)
        sub_end = time_to_seconds(sub.end)
        if sub_start >= start_time - 3 and sub_end <= end_time:
            adjusted_sub = Subtitle(
                index=sub.index,
                start=seconds_to_srt_time(sub_start - start_time),
                end=seconds_to_srt_time(sub_end - start_time),
                text=sub.text
            )
            filtered.append(adjusted_sub)
    return filtered

def write_srt(subtitles: List[Subtitle], output_file: str) -> None:
    """Write subtitles to an SRT file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        for i, sub in enumerate(subtitles):
            file.write(f"{i + 1}\n")
            file.write(f"{sub.start.replace('.', ',')} --> {sub.end.replace('.', ',')}\n")
            file.write(f"{sub.text.strip()}\n\n")

def edit_subtitles(subtitle_file: str, start_time: Optional[float] = None, end_time: Optional[float] = None) -> Optional[str]:
    """Interactive subtitle editor."""
    subtitles = parse_srt(subtitle_file)
    if start_time is not None and end_time is not None:
        working_subtitles = filter_subtitles(subtitles, start_time, end_time)
    else:
        working_subtitles = subtitles.copy()
    
    if not working_subtitles:
        logger.warning("No subtitles found in the specified time range.")
        return None

    print_section_header("Subtitle Editor")
    logger.info("Instructions: Enter subtitle number (e.g., 1), 'save', or 'back'")
    
    temp_srt = tempfile.NamedTemporaryFile(suffix='.srt', delete=False).name
    
    while True:
        logger.info("\nCurrent Subtitles:")
        for i, sub in enumerate(working_subtitles):
            logger.info(f"{i + 1}. [{sub.start} --> {sub.end}] {sub.text.strip()}")

        choice = input("\nEnter subtitle number, 'save', or 'back': ").strip().lower()
        
        if choice == 'back':
            logger.info("Discarding changes...")
            os.remove(temp_srt)
            return None
        elif choice == 'save':
            write_srt(working_subtitles, temp_srt)
            logger.info(f"Subtitles saved to: {temp_srt}")
            return temp_srt
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(working_subtitles):
                subtitle = working_subtitles[choice_num - 1]
                logger.info(f"\nEditing subtitle #{choice_num}: {subtitle.text.strip()}")
                
                new_text = input("New text (Enter to keep): ").strip()
                if new_text:
                    subtitle.text = new_text
                
                edit_timing = input("Edit timing? (1/y or 0/n): ").lower() in ['1', 'y']
                if edit_timing:
                    new_start = input(f"New start time [{subtitle.start}]: ").strip()
                    if new_start:
                        subtitle.start = new_start
                    new_end = input(f"New end time [{subtitle.end}]: ").strip()
                    if new_end:
                        subtitle.end = new_end
                logger.info("Subtitle updated.")
            else:
                logger.warning(f"Invalid number. Use 1 to {len(working_subtitles)}.")
        except ValueError:
            logger.warning("Invalid input. Use a number, 'save', or 'back'.")

# ==================================================
# Video Processing Functions
# ==================================================
def check_ffmpeg() -> None:
    """Check if FFmpeg is installed and available."""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("FFmpeg not installed or not found. Please install it.")
        sys.exit(1)

def get_video_details(video_path: str) -> Optional[VideoDetails]:
    """Get basic details about a video file."""
    try:
        with VideoFileClip(video_path) as video:
            return VideoDetails(
                duration=video.duration,
                width=video.size[0],
                height=video.size[1],
                fps=video.fps
            )
    except Exception as e:
        logger.error(f"Error getting video details: {e}")
        return None

def detect_audio_peaks(audio_segment: AudioSegment, silence_thresh: int = -50, min_silence_len: int = 500) -> List[Tuple[float, float]]:
    """Detect non-silent periods in audio."""
    nonsilent_periods = detect_nonsilent(audio_segment, silence_thresh=silence_thresh, min_silence_len=min_silence_len)
    return [(start / 1000, end / 1000) for (start, end) in nonsilent_periods]

def analyze_video_alternative(video_path: str, min_duration: float = 30, max_duration: float = 90, silence_thresh: int = -50) -> List[VideoSegment]:
    """تحليل الفيديو باستخدام FFmpeg لإيجاد المقاطع بناءً على مستوى الصوت."""
    logger.info(f"تحليل الفيديو باستخدام FFmpeg: {video_path}")
    
    # التأكد من وجود الفيديو
    if not os.path.exists(video_path):
        logger.error(f"خطأ: ملف الفيديو غير موجود في {video_path}")
        return []
    
    # استخراج معلومات مدة الفيديو
    try:
        with VideoFileClip(video_path) as video:
            video_duration = video.duration
    except Exception as e:
        logger.error(f"خطأ في استخراج معلومات الفيديو: {e}")
        return []
    
    # إنشاء مقاطع بناءً على تقسيم الفيديو إلى أجزاء متساوية
    segments = []
    
    # تقسيم الفيديو إلى مقاطع بطول min_duration إلى max_duration
    current_time = 0
    segment_id = 1
    
    logger.info("تقسيم الفيديو إلى مقاطع...")
    
    while current_time < video_duration:
        segment_end = min(current_time + max_duration, video_duration)
        segment_duration = segment_end - current_time
        
        if segment_duration >= min_duration:
            # تقدير مستوى نشاط الصوت (افتراضي لأننا لا نستطيع تحليله بدقة)
            peak_count = int(segment_duration / 10)  # افتراض قمة واحدة كل 10 ثوانٍ تقريباً
            
            segments.append(VideoSegment(
                start=current_time,
                end=segment_end,
                duration=segment_duration,
                peak_count=peak_count
            ))
            logger.info(f"تم اكتشاف مقطع {segment_id}: {format_time(current_time)} - {format_time(segment_end)} (مدة: {segment_duration:.1f}س)")
            segment_id += 1
        
        current_time = segment_end
    
    # ترتيب المقاطع حسب المدة (أطول المقاطع أولاً)
    segments.sort(key=lambda x: x.duration, reverse=True)
    return segments

def process_video_segment(
    video_path: str, 
    start_time: float, 
    end_time: float, 
    output_path: str, 
    subtitle_file: Optional[str] = None, 
    crop_x: int = 390, 
    crop_ratio: str = "9/16", 
    crf: int = 23, 
    video_bitrate: str = "1M"
) -> bool:
    """Process a video segment with optional subtitles and cropping."""
    if not os.path.exists(video_path):
        logger.error(f"Error: Video file not found at {video_path}")
        return False

    # Process subtitles if available
    temp_srt = None
    if subtitle_file and os.path.exists(subtitle_file):
        subtitles = parse_srt(subtitle_file)
        filtered_subtitles = filter_subtitles(subtitles, start_time, end_time)
        if filtered_subtitles:
            temp_srt = tempfile.NamedTemporaryFile(suffix='.srt', delete=False).name
            write_srt(filtered_subtitles, temp_srt)
        else:
            logger.info("No valid subtitles for this segment.")

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Build FFmpeg command
    command = [
        'ffmpeg',
        '-ss', str(start_time),
        '-i', video_path,
        '-t', str(end_time - start_time),
        '-c:v', 'libx264',
        '-crf', str(crf),
        '-b:v', video_bitrate,
        '-c:a', 'aac',
        '-b:a', '128k',
        '-progress', 'pipe:1',
        '-nostats',
        '-y'
    ]

    # Add filters for cropping and subtitles
    filters = [f"crop=ih*{crop_ratio}:ih:{crop_x}:0"]
    if temp_srt:
        temp_srt_escaped = os.path.abspath(temp_srt).replace('\\', '/').replace(':', '\\:')
        filters.append(f"subtitles='{temp_srt_escaped}':force_style='FontName=Vazirmatn Medium,Fontsize=16,PrimaryColour=&H00FFFF&,Alignment=2,MarginV=50'")
    
    if filters:
        command.extend(['-vf', ','.join(filters)])

    command.append(output_path)

    # Execute FFmpeg command
    logger.info("Executing: " + " ".join(command))
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8')
    for line in process.stdout:
        if "progress" in line or "frame" in line:
            logger.info(line.strip())

    return_code = process.wait()
    
    # Clean up temporary files
    if temp_srt and os.path.exists(temp_srt):
        os.remove(temp_srt)

    if return_code == 0:
        logger.info(f"Video saved as {output_path}!")
        return True
    else:
        logger.error("Error during processing.")
        return False

# ==================================================
# Interactive Interface Functions
# ==================================================
def show_menu() -> str:
    """Display the main menu and get user choice."""
    print_section_header("Main Menu")
    logger.info("1. Analyze video for segments")
    logger.info("2. Create custom segment")
    logger.info("3. Edit existing segment")
    logger.info("4. Settings")
    logger.info("5. Exit")
    return input("\nChoice (1-5): ").strip()

def show_settings_menu(settings: Settings) -> str:
    """Display the settings menu and get user choice."""
    print_section_header("Settings")
    logger.info(f"1. Output folder: {settings.output_folder}")
    logger.info(f"2. Min segment duration: {settings.min_duration}s")
    logger.info(f"3. Max segment duration: {settings.max_duration}s")
    logger.info(f"4. Crop X: {settings.crop_x}")
    logger.info(f"5. Crop ratio: {settings.crop_ratio}")
    logger.info(f"6. Silence threshold: {settings.silence_thresh} dB")
    logger.info(f"7. Video quality (CRF): {settings.crf}")
    logger.info(f"8. Video bitrate: {settings.video_bitrate}")
    logger.info("9. Back")
    return input("\nChoice (1-9): ").strip()

def parse_segment_selection(input_str: str, max_segments: int) -> List[int]:
    """Parse segment selection like '1-2', '1,3,5' into a list of indices."""
    selected = set()
    parts = input_str.replace(' ', '').split(',')
    for part in parts:
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                if 1 <= start <= end <= max_segments:
                    selected.update(range(start - 1, end))
            except ValueError:
                logger.warning(f"Invalid range: {part}")
        else:
            try:
                num = int(part)
                if 1 <= num <= max_segments:
                    selected.add(num - 1)
            except ValueError:
                logger.warning(f"Invalid number: {part}")
    return list(selected)

def select_segment(segments: List[VideoSegment]) -> Optional[List[VideoSegment]]:
    """Allow user to select one or more segments from a list."""
    if not segments:
        logger.warning("No segments available.")
        return None
    
    print_section_header("Available Segments")
    for i, segment in enumerate(segments):
        logger.info(f"{i+1}. {format_time(segment.start)} - {format_time(segment.end)} "
                    f"(Duration: {segment.duration:.1f}s, Activity: {segment.peak_count})")
    
    logger.info(f"{len(segments)+1}. Back")
    
    choice = input(f"\nSelect segments (e.g., '1-3', '1,4', or 'back'): ").strip().lower()
    if choice == 'back':
        return None
    
    selected_indices = parse_segment_selection(choice, len(segments))
    if not selected_indices:
        logger.warning("No valid segments selected.")
        return None
    
    return [segments[i] for i in selected_indices]

def get_custom_segment_times(video_details: VideoDetails) -> Tuple[Optional[float], Optional[float]]:
    """Get custom start and end times from user input."""
    if not video_details:
        logger.error("Video details not available.")
        return None, None
    
    logger.info(f"\nVideo duration: {format_time(video_details.duration)}")
    
    while True:
        try:
            start_input = input("\nStart time (HH:MM:SS or seconds): ")
            start_time = parse_time_input(start_input)
            
            end_input = input("End time (HH:MM:SS or seconds): ")
            end_time = parse_time_input(end_input)
            
            if start_time >= end_time:
                logger.error("Start time must be before end time.")
            elif start_time < 0:
                logger.error("Start time cannot be negative.")
            elif end_time > video_details.duration:
                logger.error(f"End time exceeds video duration ({video_details.duration}s).")
            else:
                return start_time, end_time
        except ValueError:
            logger.error("Invalid format. Use HH:MM:SS or seconds.")

def process_selected_segments(
    video_path: str, 
    segments: List[VideoSegment], 
    settings: Settings, 
    edit_video: bool = False, 
    add_subtitles: bool = False
) -> None:
    """Process selected segments with options to edit video and add subtitles."""
    subtitle_file = settings.subtitle_file if add_subtitles else None
    crop_x, crop_ratio = settings.crop_x, settings.crop_ratio

    if edit_video:
        use_custom_crop = input("Edit crop settings? (1/y or 0/n): ").lower() in ['1', 'y']
        if use_custom_crop:
            try:
                crop_x = int(input(f"Crop X (default: {settings.crop_x}): ") or settings.crop_x)
                crop_ratio = input(f"Crop ratio (default: {settings.crop_ratio}): ") or settings.crop_ratio
            except ValueError:
                logger.warning("Invalid input. Using defaults.")
                crop_x, crop_ratio = settings.crop_x, settings.crop_ratio

    if add_subtitles and subtitle_file and os.path.exists(subtitle_file):
        edit_subs = input("Edit subtitles? (1/y or 0/n): ").lower() in ['1', 'y']
        if edit_subs:
            for segment in segments:
                temp_srt = edit_subtitles(subtitle_file, segment.start, segment.end)
                if temp_srt:
                    subtitle_file = temp_srt
                    break  # Assuming one edit applies to all segments for simplicity

    for segment in segments:
        output_filename = f"segment_{format_time(segment.start).replace(':', '')}_to_{format_time(segment.end).replace(':', '')}.mp4"
        output_path = os.path.join(settings.output_folder, output_filename)
        logger.info(f"Processing {format_time(segment.start)} to {format_time(segment.end)}...")
        process_video_segment(
            video_path, 
            segment.start, 
            segment.end, 
            output_path, 
            subtitle_file, 
            crop_x, 
            crop_ratio,
            settings.crf,
            settings.video_bitrate
        )

    # Ask if the user wants to edit the processed segments
    edit_processed = input("Do you want to edit the processed segments? (1/y or 0/n): ").lower() in ['1', 'y']
    if edit_processed:
        for segment in segments:
            output_filename = f"segment_{format_time(segment.start).replace(':', '')}_to_{format_time(segment.end).replace(':', '')}.mp4"
            output_path = os.path.join(settings.output_folder, output_filename)
            edit_existing_segment(output_path, settings)

def create_custom_segment(video_path: str, settings: Settings) -> None:
    """Create a custom segment by manually specifying start and end times."""
    video_details = get_video_details(video_path)
    if not video_details:
        return
    
    start_time, end_time = get_custom_segment_times(video_details)
    if start_time is None or end_time is None:
        return
    
    segments = [VideoSegment(
        start=start_time, 
        end=end_time, 
        duration=end_time - start_time, 
        peak_count=1
    )]
    
    edit_video = input("Edit video (crop)? (1/y or 0/n): ").lower() in ['1', 'y']
    add_subtitles = input("Add subtitles? (1/y or 0/n): ").lower() in ['1', 'y']
    
    process_selected_segments(video_path, segments, settings, edit_video, add_subtitles)

def analyze_video_for_segments(video_path: str, min_duration: float = 30, max_duration: float = 90, silence_thresh: int = -50) -> List[VideoSegment]:
    """تحليل الفيديو وإيجاد المقاطع المحتملة بناءً على نشاط الصوت."""
    logger.info(f"تحليل الفيديو: {video_path}")
    
    # التحقق إذا كانت pydub متاحة
    if not PYDUB_AVAILABLE:
        return analyze_video_alternative(video_path, min_duration, max_duration, silence_thresh)
    
    try:
        # نحاول استخدام pydub للتحليل
        audio = AudioSegment.from_file(video_path)
    except Exception as e:
        logger.error(f"خطأ في استخراج الصوت من الفيديو: {e}")
        logger.info("استخدام الطريقة البديلة للتحليل...")
        return analyze_video_alternative(video_path, min_duration, max_duration, silence_thresh)
    
    try:
        logger.info("اكتشاف مقاطع الصوت...")
        peak_times = detect_nonsilent(audio, silence_thresh=silence_thresh, min_silence_len=500)
        
        # تحويل الأوقات من مللي ثانية إلى ثوانٍ
        peak_times = [(start / 1000, end / 1000) for (start, end) in peak_times]
        
        if not peak_times:
            logger.warning("لم يتم اكتشاف أي مقاطع صوتية. استخدام الطريقة البديلة...")
            return analyze_video_alternative(video_path, min_duration, max_duration, silence_thresh)
            
        segments = []
        current_start = 0
        current_end = 0
        current_peaks = []

        for peak in peak_times:
            if (peak[1] - current_start) > max_duration:
                if (current_end - current_start) >= min_duration:
                    segments.append(VideoSegment(
                        start=current_start,
                        end=current_end,
                        duration=current_end - current_start,
                        peak_count=len(current_peaks)
                    ))
                current_start = peak[0]
                current_end = peak[1]
                current_peaks = [peak]
            else:
                current_end = peak[1]
                current_peaks.append(peak)

        if (current_end - current_start) >= min_duration:
            segments.append(VideoSegment(
                start=current_start,
                end=current_end,
                duration=current_end - current_start,
                peak_count=len(current_peaks)
            ))

        # ترتيب المقاطع حسب مستوى النشاط
        segments.sort(key=lambda x: x.peak_count, reverse=True)
        
        if not segments:
            logger.warning("لم يتم العثور على مقاطع مناسبة. استخدام الطريقة البديلة...")
            return analyze_video_alternative(video_path, min_duration, max_duration, silence_thresh)
            
        return segments
        
    except Exception as e:
        logger.error(f"خطأ في تحليل الصوت: {e}")
        logger.info("استخدام الطريقة البديلة للتحليل...")
        return analyze_video_alternative(video_path, min_duration, max_duration, silence_thresh)

def analyze_and_select_segment(video_path: str, settings: Settings) -> None:
    """Analyze video for segments and allow user to select segments."""
    segments = analyze_video_for_segments(video_path, settings.min_duration, settings.max_duration, settings.silence_thresh)
    if not segments:
        logger.warning("No segments found.")
        return
    
    selected_segments = select_segment(segments)
    if not selected_segments:
        return
    
    edit_video = input("Edit video (crop)? (1/y or 0/n): ").lower() in ['1', 'y']
    add_subtitles = input("Add subtitles? (1/y or 0/n): ").lower() in ['1', 'y']
    
    process_selected_segments(video_path, selected_segments, settings, edit_video, add_subtitles)

# ==================================================
# Main Function
# ==================================================
import json

def save_processed_video_info(video_info: Dict[str, Any], file_path: str = "processed_videos.json") -> None:
    """Save processed video information to a JSON file."""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            data = []

        data.append(video_info)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Error saving processed video info: {e}")

def load_processed_videos(file_path: str = "processed_videos.json") -> List[Dict[str, Any]]:
    """Load processed video information from a JSON file."""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return []
    except Exception as e:
        logger.error(f"Error loading processed video info: {e}")
        return []

def show_processed_videos_menu(processed_videos: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Display the processed videos menu and get user choice."""
    if not processed_videos:
        logger.warning("No processed videos available.")
        return None

    print_section_header("Processed Videos")
    for i, video in enumerate(processed_videos):
        logger.info(f"{i + 1}. {video['output_path']} (Start: {format_time(video['start_time'])}, End: {format_time(video['end_time'])})")

    choice = input("\nSelect a video to edit (1-{}): ".format(len(processed_videos))).strip()
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(processed_videos):
            return processed_videos[choice_num - 1]
        else:
            logger.warning("Invalid choice.")
            return None
    except ValueError:
        logger.warning("Invalid input.")
        return None

def main() -> None:
    """Main application function."""
    check_ffmpeg()
    
    settings = Settings(
        video_path=r"C:\Users\MOO\Downloads\Video\Victoria's Secret Angels vs. The Bachelors (Full Episode) - Celebrity Family Feud.mp4",
        subtitle_file=r"D:\Dd\[Arabic] Victoria's Secret Angels vs. The Bachelors (Full Episode) _ Celebrity Family Feud [DownSub.com].srt",
        output_folder=r"D:\output1\output",
        min_duration=30,
        max_duration=360,
        crop_x=390,
        crop_ratio="9/16",
        silence_thresh=-50,
        crf=23,
        video_bitrate="1M"
    )
    
    # Handle command line arguments
    if len(sys.argv) >= 2:
        settings.output_folder = sys.argv[1]
    
    # Create output folder if it doesn't exist
    if not os.path.exists(settings.output_folder):
        logger.info(f"Creating output folder: {settings.output_folder}")
        os.makedirs(settings.output_folder)
    
    # Validate video path
    if not os.path.exists(settings.video_path):
        video_path = input("Enter video file path: ")
        if os.path.exists(video_path):
            settings.video_path = video_path
        else:
            logger.error(f"Video file not found: {video_path}")
            return
    
    # Validate subtitle path
    if not os.path.exists(settings.subtitle_file or ""):
        use_subtitles = input("Subtitle file not found. Specify another? (1/y or 0/n): ").lower() in ['1', 'y']
        if use_subtitles:
            subtitle_path = input("Enter subtitle file path: ")
            if os.path.exists(subtitle_path):
                settings.subtitle_file = subtitle_path
            else:
                logger.warning(f"Subtitle file not found: {subtitle_path}")
                settings.subtitle_file = None
        else:
            settings.subtitle_file = None
    
    # Main application loop
    while True:
        choice = show_menu()
        
        if choice == '1':
            analyze_and_select_segment(settings.video_path, settings)
        
        elif choice == '2':
            create_custom_segment(settings.video_path, settings)
        
        elif choice == '3':
            edit_existing_segment()
        
        elif choice == '4':
            while True:
                settings_choice = show_settings_menu(settings)
                
                if settings_choice == '1':
                    new_folder = input(f"New output folder (current: {settings.output_folder}): ")
                    if new_folder:
                        settings.output_folder = new_folder
                        if not os.path.exists(settings.output_folder):
                            os.makedirs(settings.output_folder)
                
                elif settings_choice == '2':
                    try:
                        settings.min_duration = float(input(f"New min duration (current: {settings.min_duration}): "))
                    except ValueError:
                        logger.warning("Invalid input.")
                
                elif settings_choice == '3':
                    try:
                        settings.max_duration = float(input(f"New max duration (current: {settings.max_duration}): "))
                    except ValueError:
                        logger.warning("Invalid input.")
                
                elif settings_choice == '4':
                    try:
                        settings.crop_x = int(input(f"New crop X (current: {settings.crop_x}): "))
                    except ValueError:
                        logger.warning("Invalid input.")
                
                elif settings_choice == '5':
                    new_ratio = input(f"New crop ratio (current: {settings.crop_ratio}): ")
                    if new_ratio:
                        settings.crop_ratio = new_ratio
                
                elif settings_choice == '6':
                    try:
                        settings.silence_thresh = int(input(f"New silence threshold (current: {settings.silence_thresh}): "))
                    except ValueError:
                        logger.warning("Invalid input.")
                
                elif settings_choice == '7':
                    try:
                        settings.crf = int(input(f"New video quality/CRF (current: {settings.crf}, lower is better): "))
                    except ValueError:
                        logger.warning("Invalid input.")
                
                elif settings_choice == '8':
                    new_bitrate = input(f"New video bitrate (current: {settings.video_bitrate}): ")
                    if new_bitrate:
                        settings.video_bitrate = new_bitrate
                
                elif settings_choice == '9':
                    break
                
                else:
                    logger.warning("Invalid choice (1-9).")
        
        elif choice == '5':
            logger.info("Exiting.")
            break
        
        else:
            logger.warning("Invalid choice (1-5).")

if __name__ == "__main__":
    main()