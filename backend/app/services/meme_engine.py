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

    def create_spotify_player_meme(
        self,
        song_title: str,
        artist: str,
        lyrics_quote: str,
        punchline: str
    ) -> Dict[str, Any]:
        """Render an ultra-realistic Dark Mode Spotify Music Player Meme with vinyl record & lyrics card (1080x1080)."""
        width, height = 1080, 1080
        img = Image.new("RGB", (width, height), color="#0c0e14")
        draw = ImageDraw.Draw(img)

        # 1. Dark radial glow backdrop
        cx, cy = width // 2, 380
        for r in range(450, 0, -8):
            alpha = int(45 * (1 - r / 450))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(alpha // 2, alpha // 4, alpha))

        # 2. Spotify Top Header
        font_sub = self._get_font(24, bold=True)
        draw.text((width // 2, 50), "PLAYING FROM PLAYLIST", font=font_sub, fill="#8E8E93", anchor="mm")
        font_header = self._get_font(28, bold=True)
        draw.text((width // 2, 85), "Desi Hip-Hop Bangers • DHH Cult", font=font_header, fill="#FFFFFF", anchor="mm")

        # 3. Album Art Card (420x420) with drop shadow and vinyl peek
        card_x, card_y, card_w = 330, 130, 420
        # Vinyl record peeking out behind album
        draw.ellipse([card_x + 120, card_y + 10, card_x + 120 + 400, card_y + 410], fill="#111111", outline="#222222", width=4)
        for vr in range(180, 40, -30):
            draw.ellipse([card_x + 320 - vr, card_y + 210 - vr, card_x + 320 + vr, card_y + 210 + vr], outline="#1c1c1c", width=1)
        # Vinyl center sticker
        draw.ellipse([card_x + 320 - 45, card_y + 210 - 45, card_x + 320 + 45, card_y + 210 + 45], fill="#EF4444")
        draw.ellipse([card_x + 320 - 10, card_y + 210 - 10, card_x + 320 + 10, card_y + 210 + 10], fill="#0c0e14")

        # Album front cover (Vibrant rap aesthetic art)
        draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_w], radius=16, fill="#18181B", outline="#27272A", width=3)
        draw.rectangle([card_x + 10, card_y + 10, card_x + card_w - 10, card_y + card_w - 10], fill="#1E1B4B")
        draw.ellipse([card_x + 60, card_y + 60, card_x + 360, card_y + 360], fill="#4338CA")
        draw.polygon([(card_x + 210, card_y + 70), (card_x + 90, card_y + 350), (card_x + 330, card_y + 350)], fill="#7C3AED")
        font_cover = self._get_font(56, bold=True)
        draw.text((card_x + card_w // 2, card_y + card_w // 2 - 20), "DHH", font=font_cover, fill="#FACC15", anchor="mm")
        font_cover_sub = self._get_font(26, bold=True)
        draw.text((card_x + card_w // 2, card_y + card_w // 2 + 40), "OFFICIAL BARS", font=font_cover_sub, fill="#FFFFFF", anchor="mm")

        # Parental Advisory sticker
        draw.rectangle([card_x + 20, card_y + card_w - 55, card_x + 160, card_y + card_w - 20], fill="#FFFFFF")
        font_pa = self._get_font(12, bold=True)
        draw.text((card_x + 90, card_y + card_w - 38), "PARENTAL ADVISORY", font=font_pa, fill="#000000", anchor="mm")

        # 4. Song Details (Title + Artist + Heart)
        font_title = self._get_font(42, bold=True)
        draw.text((100, 580), song_title, font=font_title, fill="#FFFFFF")
        font_artist = self._get_font(32)
        draw.text((100, 630), artist, font=font_artist, fill="#A1A1AA")
        font_heart = self._get_font(40)
        draw.text((950, 595), "💚", font=font_heart, fill="#22C55E", anchor="mm")

        # 5. Playback Scrubber Bar
        scrub_x1, scrub_y, scrub_x2 = 100, 680, 980
        draw.rounded_rectangle([scrub_x1, scrub_y, scrub_x2, scrub_y + 8], radius=4, fill="#3F3F46")
        fill_x = scrub_x1 + int((scrub_x2 - scrub_x1) * 0.48)
        draw.rounded_rectangle([scrub_x1, scrub_y, fill_x, scrub_y + 8], radius=4, fill="#22C55E")
        draw.ellipse([fill_x - 10, scrub_y - 6, fill_x + 10, scrub_y + 14], fill="#FFFFFF")
        font_time = self._get_font(22)
        draw.text((scrub_x1, scrub_y + 16), "1:38", font=font_time, fill="#A1A1AA")
        draw.text((scrub_x2, scrub_y + 16), "3:15", font=font_time, fill="#A1A1AA", anchor="ra")

        # 6. Player Control Icons
        cx = width // 2
        controls_y = 750
        font_ctrl = self._get_font(36)
        draw.text((cx - 240, controls_y), "🔀", font=font_ctrl, fill="#A1A1AA", anchor="mm")
        draw.text((cx - 120, controls_y), "⏮", font=font_ctrl, fill="#FFFFFF", anchor="mm")
        draw.ellipse([cx - 45, controls_y - 45, cx + 45, controls_y + 45], fill="#FFFFFF")
        draw.text((cx, controls_y), "⏸", font=self._get_font(42), fill="#000000", anchor="mm")
        draw.text((cx + 120, controls_y), "⏭", font=font_ctrl, fill="#FFFFFF", anchor="mm")
        draw.text((cx + 240, controls_y), "🔁", font=font_ctrl, fill="#A1A1AA", anchor="mm")

        # 7. Relatable Lyrics / Meme Highlight Card
        box_x1, box_y1, box_x2, box_y2 = 70, 820, 1010, 1030
        draw.rounded_rectangle([box_x1, box_y1, box_x2, box_y2], radius=24, fill="#18181B", outline="#22C55E", width=2)

        font_lyric_tag = self._get_font(20, bold=True)
        draw.rounded_rectangle([box_x1 + 30, box_y1 + 20, box_x1 + 140, box_y1 + 52], radius=10, fill="#22C55E")
        draw.text((box_x1 + 85, box_y1 + 36), "LYRICS", font=font_lyric_tag, fill="#000000", anchor="mm")

        font_lyric = self._get_font(32, bold=True)
        l_lines = self._wrap_text(f'"{lyrics_quote}"', draw, font_lyric, 860)
        cur_ly = box_y1 + 75
        for l in l_lines:
            draw.text((box_x1 + 35, cur_ly), l, font=font_lyric, fill="#F4F4F5")
            cur_ly += 42

        font_reaction = self._get_font(28)
        draw.text((box_x1 + 35, cur_ly + 10), f"👉 {punchline}", font=font_reaction, fill="#FACC15")

        file_id = f"spotify_{uuid.uuid4().hex[:10]}.png"
        file_path = self.output_dir / file_id
        img.save(str(file_path), "PNG", quality=95)

        return {
            "file_name": file_id,
            "file_path": str(file_path),
            "width": width,
            "height": height,
            "format": "PNG",
            "template": "SPOTIFY_PLAYER"
        }

    def create_drake_reaction_meme(
        self,
        reject_text: str,
        approve_text: str,
        category: str = "DHH_MEME"
    ) -> Dict[str, Any]:
        """Render a classic 2-panel character reaction meme with rejection and approval panels (1080x1080)."""
        width, height = 1080, 1080
        img = Image.new("RGB", (width, height), color="#0F172A")
        draw = ImageDraw.Draw(img)

        # Header Bar
        draw.rectangle([0, 0, width, 100], fill="#020617")
        draw.text((50, 32), f"🔥 DESI HIP-HOP REALITY • {category.upper()}", font=self._get_font(32, bold=True), fill="#38BDF8")
        draw.text((width - 60, 32), "@azpadhai", font=self._get_font(28, bold=True), fill="#94A3B8", anchor="ra")

        panel_w = 400
        panel_h = 450
        spacing = 20
        top_y = 120
        bot_y = 590

        # TOP LEFT: Drake Rejecting (Red vibe)
        draw.rectangle([20, top_y, 20 + panel_w, top_y + panel_h], fill="#311018")
        face_cx, face_cy = 20 + panel_w // 2, top_y + 180
        draw.ellipse([face_cx - 90, face_cy - 100, face_cx + 90, face_cy + 100], fill="#F3A683")
        draw.rectangle([face_cx - 100, face_cy - 120, face_cx + 60, face_cy - 70], fill="#1E293B")
        draw.polygon([(face_cx - 140, face_cy - 70), (face_cx - 90, face_cy - 100), (face_cx - 90, face_cy - 70)], fill="#1E293B")
        draw.rectangle([face_cx - 85, face_cy - 50, face_cx - 15, face_cy - 10], fill="#000000")
        draw.rectangle([face_cx - 5, face_cy - 50, face_cx + 65, face_cy - 10], fill="#000000")
        draw.arc([face_cx - 70, face_cy + 10, face_cx + 70, face_cy + 85], 0, 180, fill="#2D3748", width=18)
        draw.arc([face_cx - 30, face_cy + 40, face_cx + 30, face_cy + 60], 180, 360, fill="#881337", width=6)
        draw.rounded_rectangle([face_cx - 150, face_cy + 50, face_cx - 70, face_cy + 150], radius=15, fill="#F3A683")
        draw.rectangle([face_cx - 140, face_cy + 40, face_cx - 80, face_cy + 70], fill="#F3A683")
        # Stamp
        draw.ellipse([20 + panel_w - 90, top_y + 20, 20 + panel_w - 20, top_y + 90], fill="#EF4444")
        draw.text((20 + panel_w - 55, top_y + 55), "✕", font=self._get_font(46, bold=True), fill="#FFFFFF", anchor="mm")
        draw.text((20 + panel_w // 2, top_y + panel_h - 40), "NAH BHAI ❌", font=self._get_font(34, bold=True), fill="#FDA4AF", anchor="mm")

        # TOP RIGHT: Reject Statement
        draw.rounded_rectangle([20 + panel_w + spacing, top_y, width - 20, top_y + panel_h], radius=20, fill="#1E293B", outline="#475569", width=2)
        font_txt = self._get_font(38, bold=True)
        top_lines = self._wrap_text(reject_text, draw, font_txt, 560)
        ty = top_y + (panel_h - len(top_lines) * 55) // 2
        for line in top_lines:
            draw.text((20 + panel_w + spacing + 40, ty), line, font=font_txt, fill="#CBD5E1")
            ty += 55

        # BOTTOM LEFT: Drake Approving (Green vibe)
        draw.rectangle([20, bot_y, 20 + panel_w, bot_y + panel_h], fill="#062817")
        bface_cx, bface_cy = 20 + panel_w // 2, bot_y + 180
        draw.ellipse([bface_cx - 90, bface_cy - 100, bface_cx + 90, bface_cy + 100], fill="#F3A683")
        draw.rectangle([bface_cx - 95, bface_cy - 120, bface_cx + 95, bface_cy - 70], fill="#1E293B")
        draw.polygon([(bface_cx - 120, bface_cy - 70), (bface_cx + 120, bface_cy - 70), (bface_cx + 80, bface_cy - 90), (bface_cx - 80, bface_cy - 90)], fill="#334155")
        draw.rectangle([bface_cx - 75, bface_cy - 50, bface_cx - 10, bface_cy - 10], fill="#000000")
        draw.rectangle([bface_cx + 10, bface_cy - 50, bface_cx + 75, bface_cy - 10], fill="#000000")
        draw.arc([bface_cx - 70, bface_cy + 10, bface_cx + 70, bface_cy + 85], 0, 180, fill="#2D3748", width=18)
        draw.chord([bface_cx - 40, bface_cy + 30, bface_cx + 40, bface_cy + 75], 0, 180, fill="#FFFFFF")
        draw.rounded_rectangle([bface_cx + 60, bface_cy + 60, bface_cx + 160, bface_cy + 110], radius=15, fill="#F3A683")
        draw.rectangle([bface_cx + 130, bface_cy + 40, bface_cx + 160, bface_cy + 110], fill="#F3A683")
        # Stamp
        draw.ellipse([20 + panel_w - 90, bot_y + 20, 20 + panel_w - 20, bot_y + 90], fill="#22C55E")
        draw.text((20 + panel_w - 55, bot_y + 55), "✓", font=self._get_font(46, bold=True), fill="#FFFFFF", anchor="mm")
        draw.text((20 + panel_w // 2, bot_y + panel_h - 40), "YES SIR! 🔥", font=self._get_font(34, bold=True), fill="#86EFAC", anchor="mm")

        # BOTTOM RIGHT: Approve Statement
        draw.rounded_rectangle([20 + panel_w + spacing, bot_y, width - 20, bot_y + panel_h], radius=20, fill="#1E293B", outline="#22C55E", width=3)
        bot_lines = self._wrap_text(approve_text, draw, font_txt, 560)
        by = bot_y + (panel_h - len(bot_lines) * 55) // 2
        for line in bot_lines:
            draw.text((20 + panel_w + spacing + 40, by), line, font=font_txt, fill="#F8FAFC")
            by += 55

        file_id = f"drake_{uuid.uuid4().hex[:10]}.png"
        file_path = self.output_dir / file_id
        img.save(str(file_path), "PNG", quality=95)

        return {
            "file_name": file_id,
            "file_path": str(file_path),
            "width": width,
            "height": height,
            "format": "PNG",
            "template": "DRAKE_REACTION"
        }

    def create_human_meme(
        self,
        hook: str,
        content_text: str,
        punchline: Optional[str] = None,
        category: str = "DHH_MEME"
    ) -> Dict[str, Any]:
        """Dynamically select and render an authentic visual meme template instead of plain AI text cards."""
        cat_lower = category.lower()
        if "release" in cat_lower or "track" in cat_lower or "producer" in cat_lower or "studio" in cat_lower:
            parts = content_text.split("\n\n")
            lyrics = parts[0] if parts else content_text
            p_line = punchline or (parts[1] if len(parts) > 1 else "Every single time in DHH 💀")
            return self.create_spotify_player_meme(
                song_title=hook[:40],
                artist="Desi Hip-Hop Cult • Verified Banger",
                lyrics_quote=lyrics[:140],
                punchline=p_line[:100]
            )
        elif "war" in cat_lower or "battle" in cat_lower or "struggle" in cat_lower or "comparison" in cat_lower:
            parts = content_text.split("\n\n")
            top = parts[0] if parts else hook
            bottom = parts[1] if len(parts) > 1 else (punchline or content_text)
            return self.create_drake_reaction_meme(
                reject_text=top[:120],
                approve_text=bottom[:120],
                category=category
            )
        else:
            return self.create_split_comparison_meme(
                title=hook[:40],
                top_situation=content_text.split("\n\n")[0][:120],
                bottom_situation=punchline or content_text[:120],
                punchline="Real Desi Hip-Hop hours"
            )

meme_engine = MemeEngine()
