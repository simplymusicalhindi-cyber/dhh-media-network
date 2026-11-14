import os
import sys
import uuid
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
        
        # Locate ffmpeg
        custom_ffmpeg = Path("C:/Users/rusha/.faceless-shorts/bin/ffmpeg.exe")
        if custom_ffmpeg.exists():
            self.ffmpeg_exe = str(custom_ffmpeg)
        else:
            self.ffmpeg_exe = "ffmpeg"

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
        """Create a crisp, modern rounded white header card for the reel meme setup."""
        card_margin = 35
        card_w = width - (card_margin * 2)
        
        dummy = Image.new("RGBA", (100, 100))
        d_draw = ImageDraw.Draw(dummy)
        font = self._get_font(38, bold=True)
        lines = self._wrap_text(text, d_draw, font, card_w - 60)
        
        line_h = 48
        card_h = max(130, len(lines) * line_h + 50)
        
        overlay = Image.new("RGBA", (width, card_h + 30), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Drop shadow
        draw.rounded_rectangle([card_margin + 3, 14, width - card_margin + 3, card_h + 14], radius=22, fill=(0, 0, 0, 140))
        # Crisp White Card with subtle border
        draw.rounded_rectangle([card_margin, 10, width - card_margin, card_h + 10], radius=22, fill=(255, 255, 255, 245), outline=(226, 232, 240, 255), width=2)
        
        # Setup Text
        cy = 28
        for line in lines:
            draw.text((width // 2, cy + line_h // 2), line, font=font, fill=(15, 23, 42, 255), anchor="mm")
            cy += line_h
            
        overlay.save(str(output_path), "PNG")
        return output_path

    def render_reel_meme(
        self,
        template_filename: str,
        meme_text: str,
        custom_out_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Overlay meme setup text onto a 9:16 template video with audio using ffmpeg."""
        tpl_path = self.templates_dir / template_filename
        if not tpl_path.exists():
            # Try searching by partial match
            candidates = list(self.templates_dir.glob(f"*{template_filename}*"))
            if candidates:
                tpl_path = candidates[0]
            else:
                raise FileNotFoundError(f"Template video '{template_filename}' not found in {self.templates_dir}")

        out_name = custom_out_name or f"reel_{uuid.uuid4().hex[:10]}.mp4"
        out_path = self.output_dir / out_name
        target_w = 720
        
        overlay_png = self.output_dir / f"temp_ov_{uuid.uuid4().hex[:8]}.png"
        self.create_reel_text_overlay(target_w, meme_text, overlay_png)
        
        filter_complex = f"[0:v]scale={target_w}:-2[v0];[v0][1:v]overlay=0:110[outv]"
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

reel_engine = ReelEngine()
