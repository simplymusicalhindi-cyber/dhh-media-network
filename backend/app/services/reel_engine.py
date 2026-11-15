import os
import sys
import uuid
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
from PIL import Image, ImageDraw, ImageFont

from backend.app.config import settings

class ReelEngine:
    """
    Renders high-engagement DHH vertical Reel Memes (9:16) using authentic video templates
    downloaded from @templatesays, with custom situational setup cards and audio-synced video.
    """
    def __init__(self):
        self.templates_dir = settings.DATA_DIR / "media" / "reel_templates"
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir = settings.DATA_DIR / "media" / "reels"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Locate ffmpeg & ffprobe
        custom_ffmpeg = Path("C:/Users/rusha/.faceless-shorts/bin/ffmpeg.exe")
        custom_ffprobe = Path("C:/Users/rusha/.faceless-shorts/bin/ffprobe.exe")
        if custom_ffmpeg.exists():
            self.ffmpeg_exe = str(custom_ffmpeg)
        else:
            self.ffmpeg_exe = "ffmpeg"
            
        if custom_ffprobe.exists():
            self.ffprobe_exe = str(custom_ffprobe)
        else:
            self.ffprobe_exe = "ffprobe"

    def _get_font(self, size: int, bold: bool = False):
        font_paths = [
            Path("C:/Windows/Fonts") / ("arialbd.ttf" if bold else "arial.ttf"),
            Path("C:/Windows/Fonts") / ("segoeuib.ttf" if bold else "segoeui.ttf"),
            Path("C:/Windows/Fonts") / ("calibrib.ttf" if bold else "calibri.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf")
        ]
        for p in font_paths:
            if p.exists():
                try:
                    return ImageFont.truetype(str(p), size)
                except Exception:
                    pass
        return ImageFont.load_default()

    def _wrap_text(self, text: str, draw: ImageDraw.Draw, font, max_width: int) -> List[str]:
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if (bbox[2] - bbox[0]) <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))
        return lines

    def create_reel_text_overlay(self, width: int, text: str, output_path: Path) -> Path:
        """Create a clean, dedicated top-header meme text overlay that never covers video content."""
        import re
        # Clean unrenderable 4-byte unicode emojis from video overlay to prevent missing glyph boxes (□)
        clean_text = re.sub(r'[\U00010000-\U0010ffff]', '', text).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)

        header_h = 220
        overlay = Image.new("RGBA", (width, header_h), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        font = self._get_font(36, bold=True)
        lines = self._wrap_text(clean_text, draw, font, width - 80)
        
        line_h = 46
        total_text_h = len(lines) * line_h
        start_y = max(20, (header_h - total_text_h) // 2)
        
        cy = start_y
        for line in lines:
            # 1. Subtle soft drop shadow for depth
            draw.text((width // 2 + 2, cy + 2), line, font=font, fill=(0, 0, 0, 200), anchor="ma")
            # 2. Main crisp white typography with bold black stroke for 100% visibility
            draw.text((width // 2, cy), line, font=font, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255), anchor="ma")
            cy += line_h
            
        overlay.save(str(output_path), "PNG")
        return output_path

    def render_reel_meme(
        self,
        template_filename: str,
        meme_text: str,
        custom_out_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Renders a standard 9:16 (720x1280) vertical Reel meme.
        Guarantees that the meme text sits in the dedicated top header space,
        so the underlying video and faces are NEVER hidden or obscured behind text.
        """
        tpl_path = self.templates_dir / template_filename
        if not tpl_path.exists():
            # Try searching by partial match for MP4 video
            candidates = list(self.templates_dir.glob(f"*{template_filename}*.mp4"))
            if candidates:
                tpl_path = candidates[0]
            else:
                raise FileNotFoundError(f"Template video '{template_filename}' (.mp4) not found in {self.templates_dir}")

        out_name = custom_out_name or f"reel_{uuid.uuid4().hex[:10]}.mp4"
        out_path = self.output_dir / out_name
        target_w = 720
        target_h = 1280
        
        # Probe template video dimensions
        aspect = 0.5625  # default 9:16
        try:
            probe_cmd = [self.ffprobe_exe, "-v", "error", "-show_entries", "stream=width,height", "-of", "json", str(tpl_path)]
            probe_res = subprocess.run(probe_cmd, capture_output=True, text=True)
            probe_json = json.loads(probe_res.stdout)
            streams = probe_json.get("streams", [{}])[0]
            in_w = streams.get("width", 720)
            in_h = streams.get("height", 1280)
            if in_w and in_h:
                aspect = in_w / in_h
        except Exception:
            pass

        overlay_png = self.output_dir / f"temp_ov_{uuid.uuid4().hex[:8]}.png"
        self.create_reel_text_overlay(target_w, meme_text, overlay_png)
        
        # Build layout so text NEVER overlaps or hides the video/person
        if aspect >= 0.70:
            # Landscape/square: video scaled to 720 width, centered vertically below the header
            vid_h = int(target_w / aspect)
            vid_y = max(240, (target_h - vid_h) // 2)
            filter_complex = (
                f"[0:v]scale={target_w}:-2[vid];"
                f"color=c=#0B0F17:s={target_w}x{target_h}[bg];"
                f"[bg][vid]overlay=0:{vid_y}[comp];"
                f"[comp][1:v]overlay=0:20[outv]"
            )
        else:
            # Vertical: video scaled to fit below the header area (720x1040)
            filter_complex = (
                f"[0:v]scale={target_w}:1040:force_original_aspect_ratio=decrease[vid];"
                f"color=c=#0B0F17:s={target_w}x{target_h}[bg];"
                f"[bg][vid]overlay=(W-w)/2:230[comp];"
                f"[comp][1:v]overlay=0:20[outv]"
            )

        cmd = [
            self.ffmpeg_exe,
            "-y",
            "-i", str(tpl_path),
            "-i", str(overlay_png),
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            "-shortest",
            str(out_path)
        ]
        
        res = subprocess.run(cmd, capture_output=True, text=True)
        if overlay_png.exists():
            overlay_png.unlink()
            
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {res.stderr}")
            
        return {
            "file_name": out_name,
            "file_path": str(out_path),
            "template": template_filename,
            "file_size": out_path.stat().st_size,
            "format": "MP4"
        }

    def render_autonomous_reel(self, meme_text: str, custom_out_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Dynamically selects the freshest, least-used video template from the autonomous
        template_finder catalog and renders a clean, high-impact reel.
        """
        from backend.app.services.template_finder import template_finder
        fresh_tpl = template_finder.get_fresh_template()
        tpl_path = Path(fresh_tpl["local_path"])
        res = self.render_reel_meme(tpl_path.name, meme_text, custom_out_name)
        res["template_title"] = fresh_tpl.get("title")
        res["template_source"] = fresh_tpl.get("source")
        res["template_key"] = fresh_tpl.get("template_key")
        res["github_cdn_url"] = fresh_tpl.get("github_cdn_url")
        return res

reel_engine = ReelEngine()
