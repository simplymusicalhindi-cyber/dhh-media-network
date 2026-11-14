import os
import subprocess
import uuid
import math
import struct
import wave
from pathlib import Path
from typing import Dict, Any, List, Optional
from PIL import Image, ImageDraw, ImageFont
from backend.app.config import settings

class ReelsEngine:
    def __init__(self):
        self.output_dir = settings.MEDIA_DIR / "reels"
        self.cover_dir = settings.MEDIA_DIR / "covers"
        self.audio_dir = settings.MEDIA_DIR / "audio"
        self.temp_dir = settings.MEDIA_DIR / "temp"

        for p in [self.output_dir, self.cover_dir, self.audio_dir, self.temp_dir]:
            p.mkdir(parents=True, exist_ok=True)

    def _get_font(self, size: int, bold: bool = False):
        font_names = [
            "arialbd.ttf" if bold else "arial.ttf",
            "segoeuib.ttf" if bold else "segoeui.ttf",
            "calibrib.ttf" if bold else "calibri.ttf"
        ]
        for name in font_names:
            try:
                win_font_path = Path("C:/Windows/Fonts") / name
                if win_font_path.exists():
                    return ImageFont.truetype(str(win_font_path), size)
            except Exception:
                continue
        try:
            return ImageFont.load_default()
        except Exception:
            return None

    def _wrap_text(self, text: str, draw: ImageDraw.Draw, font, max_width: int) -> List[str]:
        lines = []
        for p in text.split("\n"):
            words = p.split()
            if not words:
                lines.append("")
                continue
            cur = []
            for w in words:
                test = " ".join(cur + [w])
                bbox = draw.textbbox((0, 0), test, font=font)
                if (bbox[2] - bbox[0]) <= max_width:
                    cur.append(w)
                else:
                    if cur:
                        lines.append(" ".join(cur))
                        cur = [w]
                    else:
                        lines.append(w)
            if cur:
                lines.append(" ".join(cur))
        return lines

    def ensure_dhh_beat_audio(self, duration_sec: int = 12) -> str:
        """Synthesize a clean, royalty-free 808 DHH trap beat wav file if not already existing."""
        audio_path = self.audio_dir / f"dhh_trap_beat_{duration_sec}s.wav"
        if audio_path.exists():
            return str(audio_path)

        sample_rate = 44100
        bpm = 130
        seconds_per_beat = 60.0 / bpm
        total_samples = int(sample_rate * duration_sec)

        # Generate audio buffer
        audio_data = []

        for i in range(total_samples):
            t = i / sample_rate
            beat_time = t % seconds_per_beat

            # 1. 808 Sub Kick (on beat 1 and 3 of every bar)
            bar_time = t % (seconds_per_beat * 4)
            kick_val = 0.0
            if bar_time < 0.35:
                # Frequency drops from 120Hz to 45Hz
                freq = 120.0 * math.exp(-bar_time * 8.0) + 45.0
                env = math.exp(-bar_time * 7.0)
                kick_val = math.sin(2.0 * math.pi * freq * bar_time) * env * 0.7
            elif (bar_time > seconds_per_beat * 2) and (bar_time < seconds_per_beat * 2 + 0.35):
                rel_t = bar_time - (seconds_per_beat * 2)
                freq = 110.0 * math.exp(-rel_t * 8.0) + 42.0
                env = math.exp(-rel_t * 7.0)
                kick_val = math.sin(2.0 * math.pi * freq * rel_t) * env * 0.65

            # 2. Snare / Clap (on beat 2 and 4)
            snare_val = 0.0
            if (bar_time > seconds_per_beat and bar_time < seconds_per_beat + 0.2):
                rel_t = bar_time - seconds_per_beat
                noise = ((math.sin(i * 123.456) * 10000) % 2) - 1.0
                snare_val = (math.sin(2.0 * math.pi * 220.0 * rel_t) * 0.3 + noise * 0.7) * math.exp(-rel_t * 18.0) * 0.5
            elif (bar_time > seconds_per_beat * 3 and bar_time < seconds_per_beat * 3 + 0.2):
                rel_t = bar_time - seconds_per_beat * 3
                noise = ((math.sin(i * 123.456) * 10000) % 2) - 1.0
                snare_val = (math.sin(2.0 * math.pi * 220.0 * rel_t) * 0.3 + noise * 0.7) * math.exp(-rel_t * 18.0) * 0.5

            # 3. Trap Hi-Hats (8th notes)
            hat_time = t % (seconds_per_beat / 2)
            hat_val = 0.0
            if hat_time < 0.05:
                noise = ((math.sin(i * 987.654) * 10000) % 2) - 1.0
                hat_val = noise * math.exp(-hat_time * 80.0) * 0.25

            # Combined sample with soft clipping
            sample = kick_val + snare_val + hat_val
            sample = max(-0.95, min(0.95, sample))
            audio_data.append(int(sample * 32767.0))

        # Write WAV file
        with wave.open(str(audio_path), "w") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            raw_bytes = struct.pack(f"<{len(audio_data)}h", *audio_data)
            wav_file.writeframes(raw_bytes)

        return str(audio_path)

    def generate_cover_thumbnail(self, title: str, hook: str) -> str:
        """Create a high-CTR 9:16 (1080x1920) cover image for Reels."""
        width, height = 1080, 1920
        img = Image.new("RGB", (width, height), color="#0A0B10")
        draw = ImageDraw.Draw(img)

        # Background gradient & accent glow
        for y in range(height):
            ratio = y / height
            r = int(12 + ratio * 35)
            g = int(10 + ratio * 15)
            b = int(28 + ratio * 50)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Center card (Feed 1:1 view safe zone is between y=420 and y=1500)
        feed_safe_top = 500
        draw.rounded_rectangle([60, feed_safe_top, width - 60, feed_safe_top + 800], radius=36, fill="#131B2E", outline="#6366F1", width=4)

        # Header Pill
        draw.rounded_rectangle([100, feed_safe_top + 40, 520, feed_safe_top + 105], radius=16, fill="#7C3AED")
        font_pill = self._get_font(28, bold=True)
        draw.text((125, feed_safe_top + 55), "DESI HIP-HOP EXCLUSIVE", font=font_pill, fill="#FFFFFF")

        # Main Big Hook
        font_hook = self._get_font(56, bold=True)
        lines = self._wrap_text(hook, draw, font_hook, 840)
        hy = feed_safe_top + 160
        for l in lines:
            draw.text((100, hy), l, font=font_hook, fill="#FACC15")
            hy += 75

        # Subtitle / Context
        font_title = self._get_font(42)
        sub_lines = self._wrap_text(title, draw, font_title, 840)
        hy += 30
        for l in sub_lines:
            draw.text((100, hy), l, font=font_title, fill="#E2E8F0")
            hy += 55

        # Branding (Clean, no handle watermarks)
        font_brand = self._get_font(32, bold=True)
        draw.text((width // 2, feed_safe_top + 720), "⚡ DESI HIP HOP REELS", font=font_brand, fill="#A5B4FC", anchor="mm")

        cover_id = f"cover_{uuid.uuid4().hex[:10]}.png"
        cover_path = self.cover_dir / cover_id
        img.save(str(cover_path), "PNG", quality=95)
        return str(cover_path)

    def render_reel(
        self,
        title: str,
        hook: str,
        scenes: List[Dict[str, Any]],
        punchline: str
    ) -> Dict[str, Any]:
        """
        Render a 1080x1920 9:16 vertical Reel using FFmpeg.
        Renders scene slides with safe text padding, animated progression, and authentic 808 audio.
        """
        total_duration = sum(s.get("duration", 3) for s in scenes) + 3.0  # +3s for punchline
        reel_id = uuid.uuid4().hex[:10]
        output_video_path = self.output_dir / f"reel_{reel_id}.mp4"

        # 1. Generate scene slide images
        slide_paths = []
        width, height = 1080, 1920

        # Create scenes
        for idx, scene in enumerate(scenes):
            img = Image.new("RGB", (width, height), color="#0F111A")
            draw = ImageDraw.Draw(img)

            # Gradient background
            for y in range(height):
                ratio = y / height
                r = int(14 + ratio * 20 + idx * 8)
                g = int(14 + ratio * 15)
                b = int(28 + ratio * 40)
                draw.line([(0, y), (width, y)], fill=(min(255, r), min(255, g), min(255, b)))

            # Safe area indicators (Instagram top padding ~250px, bottom padding ~380px)
            # Top Topic Header
            draw.rounded_rectangle([70, 260, width - 70, 350], radius=20, fill="#1E1B4B", outline="#4F46E5", width=2)
            font_top = self._get_font(34, bold=True)
            draw.text((100, 285), f"🔥 {title.upper()}", font=font_top, fill="#C7D2FE")

            # Main Slide Card in Safe Vertical Area (between 450 and 1350)
            draw.rounded_rectangle([60, 480, width - 60, 1320], radius=32, fill="#1E293B", outline="#334155", width=3)

            # Slide Badge
            draw.rounded_rectangle([90, 520, 360, 580], radius=14, fill="#0EA5E9")
            font_badge = self._get_font(28, bold=True)
            draw.text((110, 535), f"PART {idx + 1} OF {len(scenes)}", font=font_badge, fill="#FFFFFF")

            # Scene Text
            font_scene = self._get_font(48, bold=True)
            scene_lines = self._wrap_text(scene.get("text", ""), draw, font_scene, 860)
            sy = 650
            for l in scene_lines:
                draw.text((95, sy), l, font=font_scene, fill="#F8FAFC")
                sy += 65

            # Progress Dots
            dot_start_x = width // 2 - (len(scenes) * 25)
            for d in range(len(scenes)):
                color = "#38BDF8" if d == idx else "#475569"
                draw.ellipse([dot_start_x + (d * 50), 1240, dot_start_x + (d * 50) + 24, 1264], fill=color)

            # Bottom Safe CTA (Above Instagram bottom description/audio ticker)
            draw.rounded_rectangle([70, 1420, width - 70, 1530], radius=24, fill="#111827", outline="#6366F1", width=2)
            font_cta = self._get_font(32, bold=True)
            draw.text((100, 1455), "👀 Watch till the end for the real tea", font=font_cta, fill="#E0E7FF")

            slide_file = self.temp_dir / f"slide_{reel_id}_{idx}.png"
            img.save(str(slide_file), "PNG")
            slide_paths.append((str(slide_file), scene.get("duration", 3)))

        # 2. Create Final Punchline Slide
        punch_img = Image.new("RGB", (width, height), color="#0B0914")
        p_draw = ImageDraw.Draw(punch_img)
        for y in range(height):
            ratio = y / height
            p_draw.line([(0, y), (width, y)], fill=(int(20 + ratio * 35), int(10 + ratio * 10), int(35 + ratio * 50)))

        p_draw.rounded_rectangle([60, 480, width - 60, 1320], radius=32, fill="#18181B", outline="#F59E0B", width=4)
        p_draw.rounded_rectangle([90, 520, 360, 580], radius=14, fill="#F59E0B")
        font_b = self._get_font(28, bold=True)
        p_draw.text((110, 535), "FINAL VERDICT 💀", font=font_b, fill="#000000")

        font_p = self._get_font(50, bold=True)
        p_lines = self._wrap_text(punchline, p_draw, font_p, 860)
        py = 680
        for l in p_lines:
            p_draw.text((95, py), l, font=font_p, fill="#FDE047")
            py += 70

        p_draw.rounded_rectangle([70, 1420, width - 70, 1530], radius=24, fill="#7C3AED")
        p_draw.text((100, 1455), "👇 Tag that one DHH fan in comments!", font=self._get_font(34, bold=True), fill="#FFFFFF")

        final_slide_file = self.temp_dir / f"slide_{reel_id}_final.png"
        punch_img.save(str(final_slide_file), "PNG")
        slide_paths.append((str(final_slide_file), 3.0))

        # 3. Build FFmpeg concat file for slides
        concat_txt_path = self.temp_dir / f"concat_{reel_id}.txt"
        with open(concat_txt_path, "w", encoding="utf-8") as f:
            for s_path, s_dur in slide_paths:
                clean_path = s_path.replace("\\", "/")
                f.write(f"file '{clean_path}'\n")
                f.write(f"duration {s_dur}\n")
            # Last file must be repeated for ffmpeg concat demuxer
            last_slide_clean = slide_paths[-1][0].replace("\\", "/")
            f.write(f"file '{last_slide_clean}'\n")

        # 4. Synthesize royalty-free DHH trap beat
        audio_file = self.ensure_dhh_beat_audio(int(total_duration) + 1)

        # 5. Run FFmpeg command to assemble vertical 9:16 MP4 with H.264 video and AAC audio
        cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_txt_path),
            "-i", audio_file,
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "22",
            "-r", "30",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_video_path)
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # 6. Generate Custom Cover Thumbnail
        cover_path = self.generate_cover_thumbnail(title, hook)

        # 7. Cleanup temp slides
        try:
            concat_txt_path.unlink(missing_ok=True)
            for sp, _ in slide_paths:
                Path(sp).unlink(missing_ok=True)
        except Exception:
            pass

        if not output_video_path.exists():
            raise RuntimeError(f"FFmpeg rendering failed: {result.stderr}")

        return {
            "reel_id": reel_id,
            "video_path": str(output_video_path),
            "cover_path": cover_path,
            "duration": total_duration,
            "aspect_ratio": "9:16",
            "width": 1080,
            "height": 1920,
            "file_size": output_video_path.stat().st_size
        }

    def create_templatesays_reel(
        self,
        template_name: str,
        meme_text: str,
        custom_out_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Renders a high-engagement 9:16 vertical Reel meme from an authentic @templatesays
        video clip, overlaying a clean modern setup card while preserving audio and motion.
        """
        templates_dir = settings.DATA_DIR / "media" / "reel_templates"
        tpl_path = templates_dir / template_name
        if not tpl_path.exists():
            candidates = list(templates_dir.glob(f"*{template_name}*"))
            if candidates:
                tpl_path = candidates[0]
            else:
                raise FileNotFoundError(f"Template video '{template_name}' not found in {templates_dir}")

        out_name = custom_out_name or f"reel_meme_{uuid.uuid4().hex[:10]}.mp4"
        out_path = self.output_dir / out_name
        target_w = 720
        
        # Locate ffmpeg
        custom_ffmpeg = Path("C:/Users/rusha/.faceless-shorts/bin/ffmpeg.exe")
        ffmpeg_exe = str(custom_ffmpeg) if custom_ffmpeg.exists() else "ffmpeg"

        # Generate text card overlay
        overlay_png = self.output_dir / f"temp_ov_{uuid.uuid4().hex[:8]}.png"
        card_margin = 35
        card_w = target_w - (card_margin * 2)
        
        dummy = Image.new("RGBA", (100, 100))
        d_draw = ImageDraw.Draw(dummy)
        font = self._get_font(38, bold=True)
        lines = self._wrap_text(meme_text, d_draw, font, card_w - 60)
        
        line_h = 48
        card_h = max(130, len(lines) * line_h + 50)
        overlay = Image.new("RGBA", (target_w, card_h + 30), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        draw.rounded_rectangle([card_margin + 3, 14, target_w - card_margin + 3, card_h + 14], radius=22, fill=(0, 0, 0, 140))
        draw.rounded_rectangle([card_margin, 10, target_w - card_margin, card_h + 10], radius=22, fill=(255, 255, 255, 245), outline=(226, 232, 240, 255), width=2)
        
        cy = 28
        for line in lines:
            draw.text((target_w // 2, cy + line_h // 2), line, font=font, fill=(15, 23, 42, 255), anchor="mm")
            cy += line_h
        overlay.save(str(overlay_png), "PNG")

        filter_complex = f"[0:v]scale={target_w}:-2[v0];[v0][1:v]overlay=0:110[outv]"
        cmd = [
            ffmpeg_exe,
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
            "reel_id": out_name.replace(".mp4", ""),
            "video_path": str(out_path),
            "template": tpl_path.name,
            "aspect_ratio": "9:16",
            "file_size": out_path.stat().st_size,
            "format": "MP4"
        }

reels_engine = ReelsEngine()
