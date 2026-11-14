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

        # Watermark
        font_watermark = self._get_font(28)
        draw.text((width // 2 - 160, 1820), "@desihiphop_vibes", font=font_watermark, fill="#64748B")

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

story_engine = StoryEngine()
