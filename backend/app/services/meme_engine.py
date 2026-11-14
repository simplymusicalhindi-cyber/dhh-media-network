import os
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFont
from backend.app.config import settings

class MemeEngine:
    def __init__(self):
        self.output_dir = settings.MEDIA_DIR / "memes"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _get_font(self, size: int, bold: bool = False):
        """Safely load a standard TrueType font on Windows, with fallback to default."""
        font_names = [
            "arialbd.ttf" if bold else "arial.ttf",
            "segoeuib.ttf" if bold else "segoeui.ttf",
            "calibrib.ttf" if bold else "calibri.ttf",
            "tahoma.ttf",
        ]
        for name in font_names:
            try:
                # Common Windows fonts directory
                win_font_path = Path("C:/Windows/Fonts") / name
                if win_font_path.exists():
                    return ImageFont.truetype(str(win_font_path), size)
            except Exception:
                continue
        try:
            return ImageFont.load_default()
        except Exception:
            return None

    def _wrap_text(self, text: str, draw: ImageDraw.Draw, font, max_width: int) -> list[str]:
        """Wrap text into lines that fit within max_width."""
        lines = []
        for paragraph in text.split("\n"):
            words = paragraph.split()
            if not words:
                lines.append("")
                continue
            current_line = []
            for word in words:
                test_line = " ".join(current_line + [word])
                bbox = draw.textbbox((0, 0), test_line, font=font)
                width = bbox[2] - bbox[0]
                if width <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(" ".join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
            if current_line:
                lines.append(" ".join(current_line))
        return lines

    def create_tweet_card_meme(
        self,
        hook: str,
        content_text: str,
        punchline: Optional[str] = None,
        category: str = "DHH_MEME"
    ) -> Dict[str, Any]:
        """Render a sleek, high-engagement Twitter/X style dark theme meme card (1080x1080)."""
        width, height = 1080, 1080
        img = Image.new("RGB", (width, height), color="#0F172A")  # Dark slate
        draw = ImageDraw.Draw(img)

        # Draw subtle gradient/glow background
        for y in range(height):
            r = int(15 + (y / height) * 10)
            g = int(23 + (y / height) * 15)
            b = int(42 + (y / height) * 30)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Outer card box
        card_margin = 60
        card_bbox = [card_margin, card_margin, width - card_margin, height - card_margin]
        draw.rounded_rectangle(card_bbox, radius=28, fill="#1E293B", outline="#334155", width=3)

        # Profile avatar circle
        avatar_x, avatar_y, avatar_r = 120, 130, 45
        draw.ellipse([avatar_x - avatar_r, avatar_y - avatar_r, avatar_x + avatar_r, avatar_y + avatar_r], fill="#8B5CF6")
        
        # Avatar initial
        font_avatar = self._get_font(42, bold=True)
        draw.text((avatar_x - 18, avatar_y - 25), "DHH", font=font_avatar, fill="#FFFFFF")

        # Profile Name and Handle
        font_name = self._get_font(36, bold=True)
        font_handle = self._get_font(28)
        draw.text((190, 100), "Desi Hip Hop Cult", font=font_name, fill="#F8FAFC")
        
        # Verified Badge
        draw.text((510, 102), "✓", font=font_name, fill="#38BDF8")
        draw.text((190, 145), "@desihiphop_vibes • 1h ago", font=font_handle, fill="#94A3B8")

        # Category pill badge
        font_badge = self._get_font(22, bold=True)
        badge_text = category.replace("_", " ").upper()
        draw.rounded_rectangle([750, 105, 960, 145], radius=12, fill="#7C3AED")
        draw.text((770, 115), badge_text, font=font_badge, fill="#FFFFFF")

        # Separator line
        draw.line([(card_margin + 30, 210), (width - card_margin - 30, 210)], fill="#334155", width=2)

        # Hook / Title
        font_hook = self._get_font(46, bold=True)
        hook_lines = self._wrap_text(hook, draw, font_hook, 840)
        curr_y = 250
        for line in hook_lines:
            draw.text((card_margin + 50, curr_y), line, font=font_hook, fill="#38BDF8")
            curr_y += 60

        curr_y += 30

        # Main Body Text
        font_body = self._get_font(42)
        body_lines = self._wrap_text(content_text, draw, font_body, 840)
        for line in body_lines:
            draw.text((card_margin + 50, curr_y), line, font=font_body, fill="#F1F5F9")
            curr_y += 55

        # Punchline box if present
        if punchline:
            curr_y += 40
            draw.rounded_rectangle(
                [card_margin + 40, curr_y, width - card_margin - 40, curr_y + 160],
                radius=18,
                fill="#0F172A",
                outline="#A855F7",
                width=2
            )
            font_punch = self._get_font(38, bold=True)
            punch_lines = self._wrap_text(f"💡 {punchline}", draw, font_punch, 800)
            p_y = curr_y + 35
            for line in punch_lines:
                draw.text((card_margin + 65, p_y), line, font=font_punch, fill="#E2E8F0")
                p_y += 50

        # Footer Metrics
        footer_y = height - card_margin - 70
        draw.line([(card_margin + 30, footer_y - 20), (width - card_margin - 30, footer_y - 20)], fill="#334155", width=2)
        font_footer = self._get_font(26)
        draw.text((card_margin + 50, footer_y), "💬 1.2K   🔁 4.8K   ❤️ 28.4K   📌 DHH Scene", font=font_footer, fill="#94A3B8")
        draw.text((width - card_margin - 240, footer_y), "instagram.com", font=font_footer, fill="#64748B")

        # Save image
        file_id = f"meme_{uuid.uuid4().hex[:10]}.png"
        file_path = self.output_dir / file_id
        img.save(str(file_path), "PNG", quality=95)

        return {
            "file_name": file_id,
            "file_path": str(file_path),
            "width": width,
            "height": height,
            "format": "PNG",
            "template": "TWEET_CARD_STYLE"
        }

    def create_split_comparison_meme(
        self,
        title: str,
        top_situation: str,
        bottom_situation: str,
        punchline: str
    ) -> Dict[str, Any]:
        """Render a 2-panel comparison meme (1080x1350 vertical or 1080x1080)."""
        width, height = 1080, 1080
        img = Image.new("RGB", (width, height), color="#090D16")
        draw = ImageDraw.Draw(img)

        # Header Bar
        draw.rectangle([(0, 0), (width, 110)], fill="#1E1B4B")
        font_header = self._get_font(40, bold=True)
        draw.text((50, 35), title.upper(), font=font_header, fill="#A78BFA")

        # Top Panel
        draw.rounded_rectangle([40, 140, width - 40, 520], radius=20, fill="#1E293B", outline="#475569", width=2)
        draw.rounded_rectangle([60, 160, 360, 210], radius=10, fill="#EF4444")
        font_badge = self._get_font(26, bold=True)
        draw.text((80, 172), "EXPECTATION / PLAN", font=font_badge, fill="#FFFFFF")

        font_panel = self._get_font(42)
        top_lines = self._wrap_text(top_situation, draw, font_panel, 920)
        ty = 240
        for l in top_lines:
            draw.text((70, ty), l, font=font_panel, fill="#F8FAFC")
            ty += 54

        # Bottom Panel
        draw.rounded_rectangle([40, 550, width - 40, 930], radius=20, fill="#1E293B", outline="#475569", width=2)
        draw.rounded_rectangle([60, 570, 360, 620], radius=10, fill="#10B981")
        draw.text((80, 582), "REALITY IN DHH", font=font_badge, fill="#FFFFFF")

        bot_lines = self._wrap_text(bottom_situation, draw, font_panel, 920)
        by = 650
        for l in bot_lines:
            draw.text((70, by), l, font=font_panel, fill="#F8FAFC")
            by += 54

        # Footer Punchline
        draw.rectangle([(0, 960), (width, height)], fill="#0F172A")
        font_punch = self._get_font(34, bold=True)
        draw.text((50, 995), f"💀 {punchline}", font=font_punch, fill="#FBBF24")

        file_id = f"split_{uuid.uuid4().hex[:10]}.png"
        file_path = self.output_dir / file_id
        img.save(str(file_path), "PNG", quality=95)

        return {
            "file_name": file_id,
            "file_path": str(file_path),
            "width": width,
            "height": height,
            "format": "PNG",
            "template": "SPLIT_COMPARISON"
        }

meme_engine = MemeEngine()
