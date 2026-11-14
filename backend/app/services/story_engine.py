import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
from PIL import Image, ImageDraw, ImageFont
from backend.app.config import settings

class StoryEngine:
    def __init__(self):
        self.output_dir = settings.MEDIA_DIR / "stories"
        self.output_dir.mkdir(parents=True, exist_ok=True)

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

    def create_story_graphic(
        self,
        story_type: str,
        title: str,
        clue: str,
        options: List[str],
        call_to_action: str
    ) -> Dict[str, Any]:
        """Render a 1080x1920 9:16 high-impact Instagram Story image."""
        width, height = 1080, 1920
        img = Image.new("RGB", (width, height), color="#090A0F")
        draw = ImageDraw.Draw(img)

        # Gradient vertical background
        for y in range(height):
            ratio = y / height
            r = int(10 + ratio * 30)
            g = int(12 + ratio * 15)
            b = int(25 + ratio * 45)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Safe area top bar (Instagram profile & close buttons take top ~200px)
        # Header Badge
        header_y = 240
        draw.rounded_rectangle([80, header_y, width - 80, header_y + 90], radius=24, fill="#1E1B4B", outline="#4338CA", width=3)
        font_tag = self._get_font(34, bold=True)
        draw.text((120, header_y + 25), "🔥 DESI HIP-HOP DAILY STORY", font=font_tag, fill="#A5B4FC")

        # Main Question Title
        font_title = self._get_font(52, bold=True)
        title_y = header_y + 140
        lines = self._wrap_text(title, draw, font_title, 920)
        for line in lines:
            draw.text((80, title_y), line, font=font_title, fill="#F8FAFC")
            title_y += 70

        # Clue Card
        clue_card_y = title_y + 40
        draw.rounded_rectangle([70, clue_card_y, width - 70, clue_card_y + 360], radius=32, fill="#182234", outline="#3B82F6", width=3)
        font_clue = self._get_font(42)
        clue_lines = self._wrap_text(clue, draw, font_clue, 880)
        cy = clue_card_y + 45
        for cl in clue_lines:
            draw.text((105, cy), cl, font=font_clue, fill="#E2E8F0")
            cy += 58

        # Options Interactive Visual Elements
        opt_start_y = clue_card_y + 420
        font_opt = self._get_font(40, bold=True)
        for i, opt in enumerate(options):
            card_top = opt_start_y + (i * 125)
            # Distinct vibrant color for options
            card_fill = "#1E293B" if i % 2 == 0 else "#242F44"
            draw.rounded_rectangle([70, card_top, width - 70, card_top + 105], radius=24, fill=card_fill, outline="#64748B", width=2)
            draw.text((110, card_top + 28), opt, font=font_opt, fill="#FFFFFF")

        # Call to Action Safe Box (Above bottom Instagram reply bar ~ 1650px)
        cta_y = 1580
        draw.rounded_rectangle([70, cta_y, width - 70, cta_y + 130], radius=28, fill="#7C3AED", outline="#A855F7", width=2)
        font_cta = self._get_font(36, bold=True)
        draw.text((110, cta_y + 42), call_to_action, font=font_cta, fill="#FFFFFF")

        # Handle
        font_watermark = self._get_font(28, bold=True)
        draw.text((width // 2, 1820), "@Dhh_media_network", font=font_watermark, fill="#94A3B8", anchor="mm")

        file_id = f"story_{uuid.uuid4().hex[:10]}.png"
        file_path = self.output_dir / file_id
        img.save(str(file_path), "PNG", quality=95)

        return {
            "file_name": file_id,
            "file_path": str(file_path),
            "width": width,
            "height": height,
            "aspect_ratio": "9:16",
            "format": "PNG",
            "story_type": story_type
        }

    def create_funny_meme_story(
        self,
        situation_tag: str,
        hook: str,
        scenario_text: str,
        poll_question: str,
        option_a: str,
        option_b: str,
        handle: str = "@Dhh_media_network",
        embedded_image_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Render a 1080x1920 9:16 humorous DHH Instagram Story featuring real artist imagery,
        authentic Instagram Story UI elements (progress bars, profile header, poll sticker, slider),
        and interactive community engagement widgets.
        """
        from PIL import ImageOps, ImageEnhance
        width, height = 1080, 1920
        img = Image.new("RGB", (width, height), color="#090B10")
        draw = ImageDraw.Draw(img)

        # 1. Subtle Dark Studio Gradient Background
        for y in range(height):
            ratio = y / height
            r = int(10 + ratio * 24)
            g = int(12 + ratio * 16)
            b = int(22 + ratio * 38)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # 2. Instagram Story Top Progress Bar (3 segments)
        bar_y = 35
        bar_w = (width - 60 - 20) // 3
        for i in range(3):
            bx = 30 + i * (bar_w + 10)
            fill_c = "#FFFFFF" if i == 0 else "#4B5563"
            draw.rounded_rectangle([bx, bar_y, bx + bar_w, bar_y + 5], radius=3, fill=fill_c)

        # 3. Instagram Story Profile Top Header (y = 65)
        avatar_cx, avatar_cy, avatar_r = 65, 105, 30
        # Colorful Instagram Gradient Story Ring
        draw.ellipse([avatar_cx - avatar_r - 4, avatar_cy - avatar_r - 4, avatar_cx + avatar_r + 4, avatar_cy + avatar_r + 4], fill="#F43F5E")
        draw.ellipse([avatar_cx - avatar_r, avatar_cy - avatar_r, avatar_cx + avatar_r, avatar_cy + avatar_r], fill="#1E1B4B")
        font_av = self._get_font(26, bold=True)
        draw.text((avatar_cx, avatar_cy), "DHH", font=font_av, fill="#FACC15", anchor="mm")

        # Handle and Time
        font_handle = self._get_font(30, bold=True)
        draw.text((115, 90), handle, font=font_handle, fill="#FFFFFF")
        font_time = self._get_font(24)
        draw.text((115 + len(handle) * 16 + 15, 94), "14m", font=font_time, fill="#9CA3AF")

        # Close / Options Icons on right
        draw.text((width - 110, 92), "•••", font=self._get_font(28, bold=True), fill="#FFFFFF")
        draw.text((width - 55, 92), "✕", font=self._get_font(30, bold=True), fill="#FFFFFF")

        # 4. Situation Header Pill (y = 170)
        draw.rounded_rectangle([60, 165, width - 60, 235], radius=16, fill="#1E293B", outline="#475569", width=2)
        font_sit = self._get_font(28, bold=True)
        draw.text((width // 2, 200), f"🔥 {situation_tag.upper()}", font=font_sit, fill="#FBBF24", anchor="mm")

        # 5. Main Situation Punchlines
        font_hook = self._get_font(44, bold=True)
        lines_hook = self._wrap_text(hook, draw, font_hook, 940)
        curr_y = 265
        for l in lines_hook:
            draw.text((60, curr_y), l, font=font_hook, fill="#FFFFFF")
            curr_y += 56

        curr_y += 10
        font_scen = self._get_font(36)
        lines_scen = self._wrap_text(scenario_text, draw, font_scen, 940)
        for l in lines_scen:
            draw.text((60, curr_y), l, font=font_scen, fill="#94A3B8")
            curr_y += 46

        # 6. Embedded Real Photo / Meme Card (y ~ 470, height ~ 500)
        img_box_y = curr_y + 20
        box_w = width - 120
        box_h = 500
        box_x = 60

        resolved_photo = embedded_image_path
        if not resolved_photo or not Path(resolved_photo).exists():
            # Check default high-res press photos
            artists_dir = settings.DATA_DIR / "media" / "artists"
            p_sm = artists_dir / "seedhe_maut.jpg"
            if p_sm.exists():
                resolved_photo = str(p_sm)

        photo_rendered = False
        if resolved_photo and Path(resolved_photo).exists():
            try:
                with Image.open(resolved_photo) as p_img:
                    fitted = ImageOps.fit(p_img, (box_w, box_h), method=Image.Resampling.LANCZOS, centering=(0.5, 0.3))
                    enhancer = ImageEnhance.Contrast(fitted)
                    final_p = enhancer.enhance(1.15)
                    # Mask with rounded corners
                    mask = Image.new("L", (box_w, box_h), 0)
                    m_draw = ImageDraw.Draw(mask)
                    m_draw.rounded_rectangle([0, 0, box_w, box_h], radius=28, fill=255)
                    img.paste(final_p, (box_x, img_box_y), mask=mask)
                    draw.rounded_rectangle([box_x, img_box_y, box_x + box_w, img_box_y + box_h], radius=28, outline="#38BDF8", width=3)
                    photo_rendered = True
            except Exception:
                photo_rendered = False

        if not photo_rendered:
            draw.rounded_rectangle([box_x, img_box_y, box_x + box_w, img_box_y + box_h], radius=28, fill="#1E1B4B", outline="#6366F1", width=3)
            draw.text((width // 2, img_box_y + box_h // 2), "🎧 808s AT MAXIMUM VOLUME 🎧", font=self._get_font(42, bold=True), fill="#FACC15", anchor="mm")

        # 7. Native Instagram Poll Sticker (y ~ 1080)
        poll_y = img_box_y + box_h + 35
        poll_w = width - 120
        poll_h = 360
        poll_x = 60

        # Poll Card Drop Shadow
        draw.rounded_rectangle([poll_x + 4, poll_y + 8, poll_x + poll_w + 4, poll_y + poll_h + 8], radius=28, fill="#050608")
        # Poll Card Body (White/Cream Instagram Sticker style)
        draw.rounded_rectangle([poll_x, poll_y, poll_x + poll_w, poll_y + poll_h], radius=28, fill="#FFFFFF", outline="#E2E8F0", width=2)

        # Poll Header / Question
        font_q = self._get_font(38, bold=True)
        q_lines = self._wrap_text(poll_question, draw, font_q, poll_w - 60)
        qy = poll_y + 35
        for ql in q_lines[:2]:
            draw.text((width // 2, qy), ql, font=font_q, fill="#0F172A", anchor="mm")
            qy += 48

        # Option A Button
        opt_y1 = qy + 15
        draw.rounded_rectangle([poll_x + 30, opt_y1, poll_x + poll_w - 30, opt_y1 + 80], radius=18, fill="#F1F5F9", outline="#CBD5E1", width=2)
        font_opt = self._get_font(32, bold=True)
        draw.text((poll_x + 50, opt_y1 + 40), f"A. {option_a}", font=font_opt, fill="#1E293B", anchor="lm")
        draw.text((poll_x + poll_w - 55, opt_y1 + 40), "🗳️", font=self._get_font(30), anchor="mm")

        # Option B Button
        opt_y2 = opt_y1 + 95
        draw.rounded_rectangle([poll_x + 30, opt_y2, poll_x + poll_w - 30, opt_y2 + 80], radius=18, fill="#F1F5F9", outline="#CBD5E1", width=2)
        draw.text((poll_x + 50, opt_y2 + 40), f"B. {option_b}", font=font_opt, fill="#1E293B", anchor="lm")
        draw.text((poll_x + poll_w - 55, opt_y2 + 40), "🗳️", font=self._get_font(30), anchor="mm")

        # 8. Instagram Slider Sticker Widget (y ~ 1520)
        slider_y = poll_y + poll_h + 30
        draw.rounded_rectangle([60, slider_y, width - 60, slider_y + 110], radius=24, fill="#1E293B", outline="#475569", width=2)
        draw.text((95, slider_y + 35), "Vibe check right now:", font=self._get_font(30, bold=True), fill="#FFFFFF")
        # Slider track
        draw.rounded_rectangle([95, slider_y + 75, width - 150, slider_y + 87], radius=6, fill="#475569")
        draw.rounded_rectangle([95, slider_y + 75, width - 280, slider_y + 87], radius=6, fill="#EF4444")
        # Emoji Thumb
        draw.ellipse([width - 310, slider_y + 60, width - 250, slider_y + 102], fill="#EF4444")
        draw.text((width - 280, slider_y + 81), "🔥", font=self._get_font(28), anchor="mm")

        # 9. Instagram Bottom Reply Bar (Safe Zone ~ 1700 - 1820)
        bar_bot_y = height - 190
        # Pill Reply Box
        draw.rounded_rectangle([40, bar_bot_y, width - 180, bar_bot_y + 80], radius=40, fill="#161B26", outline="#374151", width=2)
        font_reply = self._get_font(28)
        draw.text((75, bar_bot_y + 40), f"Reply to {handle}...", font=font_reply, fill="#9CA3AF", anchor="lm")

        # Heart and Share icons
        draw.text((width - 130, bar_bot_y + 40), "🤍", font=self._get_font(36), anchor="mm")
        draw.text((width - 65, bar_bot_y + 40), "✈️", font=self._get_font(36), anchor="mm")

        file_id = f"funny_story_{uuid.uuid4().hex[:10]}.png"
        file_path = self.output_dir / file_id
        img.save(str(file_path), "PNG", quality=95)

        return {
            "file_name": file_id,
            "file_path": str(file_path),
            "width": width,
            "height": height,
            "aspect_ratio": "9:16",
            "format": "PNG",
            "story_type": "FUNNY_DHH_MEME_STORY"
        }

story_engine = StoryEngine()
