import os
import uuid
import random
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFont
from backend.app.config import settings

class MemeEngine:
    def __init__(self):
        self.output_dir = settings.MEDIA_DIR / "memes"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _get_font(self, size: int, bold: bool = False):
        """Safely load a standard TrueType font on Windows and Linux (Docker/Render)."""
        font_paths = [
            # Windows fonts
            Path("C:/Windows/Fonts") / ("arialbd.ttf" if bold else "arial.ttf"),
            Path("C:/Windows/Fonts") / ("segoeuib.ttf" if bold else "segoeui.ttf"),
            Path("C:/Windows/Fonts") / ("calibrib.ttf" if bold else "calibri.ttf"),
            Path("C:/Windows/Fonts") / "tahoma.ttf",
            # Linux (Debian / Ubuntu / Docker / Render) fonts
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
            Path("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf"),
        ]
        for p in font_paths:
            try:
                if p.exists():
                    return ImageFont.truetype(str(p), size)
            except Exception:
                continue
        try:
            return ImageFont.load_default()
        except Exception:
            return None

    def _get_serif_font(self, size: int, bold: bool = False, italic: bool = False):
        """Safely load authentic newspaper serif fonts (Georgia, Times New Roman, DejaVuSerif)."""
        names = []
        if bold and italic:
            names = ["georgiaz.ttf", "timesbi.ttf"]
        elif bold:
            names = ["georgiab.ttf", "timesbd.ttf", "arialbd.ttf"]
        elif italic:
            names = ["georgiai.ttf", "timesi.ttf", "ariali.ttf"]
        else:
            names = ["georgia.ttf", "times.ttf", "arial.ttf"]
        
        font_paths = [
            Path("C:/Windows/Fonts") / n for n in names
        ] + [
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),
            Path("/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"),
            Path("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf")
        ]
        for p in font_paths:
            try:
                if p.exists():
                    return ImageFont.truetype(str(p), size)
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

    def create_newspaper_cutting_meme(
        self,
        headline: str,
        subtext: str,
        story_body: Optional[str] = None,
        witness_quote: Optional[str] = None,
        edition_tag: str = "DELHI / MUMBAI PRESS CLIPPING",
        source_tag: str = "@azpadhai",
        source_image_path: Optional[str] = None,
        photo_caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """Render an ultra-realistic vintage/print newspaper clipping meme with real source photos (1080x1080)."""
        width, height = 1080, 1080
        # Dark studio desk surface
        img = Image.new("RGB", (width, height), color="#16171B")
        draw = ImageDraw.Draw(img)

        # Desk wood/slate grain lines
        for y in range(0, height, 4):
            draw.line([(0, y), (width, y)], fill="#191A20", width=1)

        # Paper Drop Shadow
        px1, py1, px2, py2 = 50, 40, width - 50, height - 40
        draw.rectangle([px1 + 10, py1 + 14, px2 + 10, py2 + 14], fill="#0A0A0C")

        # Newsprint paper base
        draw.rectangle([px1, py1, px2, py2], fill="#F4EFEA")

        # Newsprint subtle aging fibers
        for y in range(py1 + 2, py2 - 2, 6):
            draw.line([(px1, y), (px2, y)], fill="#ECE5DD", width=1)

        # Masking tape on top-left and top-right corners
        draw.rectangle([px1 + 30, py1 - 10, px1 + 140, py1 + 25], fill="#D6C8AC")
        draw.rectangle([px2 - 140, py1 - 10, px2 - 30, py1 + 25], fill="#D6C8AC")

        # Scissor cutout dashed line at top
        font_cut = self._get_serif_font(16)
        draw.text(
            (width // 2, py1 + 12),
            "- - - - - - - - - - - - - - - - [ ✂ CLIPPED FROM DESI RAP PRESS ARCHIVES ] - - - - - - - - - - - - - - - -",
            font=font_cut,
            fill="#8C827A",
            anchor="mm"
        )

        # Newspaper Masthead
        font_top = self._get_serif_font(18, bold=True)
        draw.text((width // 2, py1 + 42), "★ THE OFFICIAL DESI HIP-HOP CHRONICLE ★", font=font_top, fill="#2B2825", anchor="mm")

        font_mast = self._get_serif_font(56, bold=True)
        draw.text((width // 2, py1 + 90), "THE DHH DISPATCH", font=font_mast, fill="#111111", anchor="mm")

        # Double black divider rules
        draw.line([(px1 + 30, py1 + 130), (px2 - 30, py1 + 130)], fill="#1A1A1A", width=3)
        draw.line([(px1 + 30, py1 + 136), (px2 - 30, py1 + 136)], fill="#1A1A1A", width=1)

        # Dateline / Issue info
        font_info = self._get_serif_font(18, bold=True)
        draw.text((px1 + 35, py1 + 150), "VOL. VIII • NO. 404", font=font_info, fill="#44403C")
        draw.text((width // 2, py1 + 150), edition_tag.upper(), font=font_info, fill="#44403C", anchor="mm")
        draw.text((px2 - 35, py1 + 150), "PRICE: 1 RE-SHARE", font=font_info, fill="#44403C", anchor="ra")

        draw.line([(px1 + 30, py1 + 172), (px2 - 30, py1 + 172)], fill="#1A1A1A", width=2)

        # Red ink stamp in top-right corner
        stamp_x1, stamp_y1, stamp_x2, stamp_y2 = px2 - 270, py1 + 185, px2 - 35, py1 + 225
        draw.rectangle([stamp_x1, stamp_y1, stamp_x2, stamp_y2], outline="#B91C1C", width=3)
        font_stamp = self._get_serif_font(20, bold=True)
        draw.text(((stamp_x1 + stamp_x2) // 2, stamp_y1 + 20), "⚡ BREAKING NEWS", font=font_stamp, fill="#B91C1C", anchor="mm")

        # Lead Headline (large serif bold)
        font_hl = self._get_serif_font(42, bold=True)
        hl_lines = self._wrap_text(headline, draw, font_hl, 660)
        hy = py1 + 185
        for l in hl_lines[:3]:
            draw.text((px1 + 35, hy), l, font=font_hl, fill="#0F0E0D")
            hy += 48

        # Subheadline in italics
        font_sub = self._get_serif_font(24, italic=True)
        s_lines = self._wrap_text(f'"{subtext}"', draw, font_sub, 900)
        draw.text((px1 + 35, hy + 8), s_lines[0] if s_lines else subtext, font=font_sub, fill="#333333")

        # Byline
        draw.text((px1 + 35, hy + 42), "BY SPECIAL CORRESPONDENT IN DELHI • DHH CULTURAL DESK", font=self._get_serif_font(18, bold=True), fill="#78716C")
        draw.line([(px1 + 30, hy + 72), (px2 - 30, hy + 72)], fill="#1A1A1A", width=1)

        # Press Photo Box
        img_box_y = hy + 82
        box_h = 240
        box_w = px2 - px1 - 60

        # Automatic real source photo embedding
        photo_placed = False
        resolved_photo_path = source_image_path
        detected_caption = photo_caption

        if not resolved_photo_path or not Path(resolved_photo_path).exists():
            full_check = f"{headline} {subtext} {story_body or ''}".lower()
            artists_dir = settings.DATA_DIR / "media" / "artists"
            if "seedhe maut" in full_check or "tbsm" in full_check or "calm" in full_check or "encore" in full_check:
                p = artists_dir / "seedhe_maut.jpg"
                if p.exists():
                    resolved_photo_path = str(p)
                    detected_caption = detected_caption or "PRESS PHOTO: Seedhe Maut performing live at packed arena in Delhi NCR. (DHH ARCHIVE)"
            elif "hanumankind" in full_check or "kalmi" in full_check or "big dawgs" in full_check:
                p = artists_dir / "hanumankind.jpg"
                if p.exists():
                    resolved_photo_path = str(p)
                    detected_caption = detected_caption or "PRESS PHOTO: Hanumankind during international festival headline tour. (DHH ARCHIVE)"
            elif "divine" in full_check or "gully gang" in full_check or "59" in full_check:
                p = artists_dir / "divine.jpg"
                if p.exists():
                    resolved_photo_path = str(p)
                    detected_caption = detected_caption or "PRESS PHOTO: DIVINE representing Mumbai 59 street rap movement. (DHH ARCHIVE)"
            elif "stan" in full_check or "p-town" in full_check:
                p = artists_dir / "mc_stan.jpg"
                if p.exists():
                    resolved_photo_path = str(p)
                    detected_caption = detected_caption or "PRESS PHOTO: MC Stan performing P-Town 808 trap anthems. (DHH ARCHIVE)"
            elif "emiway" in full_check or "bantai" in full_check:
                p = artists_dir / "emiway.jpg"
                if p.exists():
                    resolved_photo_path = str(p)
                    detected_caption = detected_caption or "PRESS PHOTO: Emiway Bantai during independent album launch. (DHH ARCHIVE)"
            elif "raftaar" in full_check or "kalamkaar" in full_check or "raa" in full_check:
                p = artists_dir / "raftaar.jpg"
                if p.exists():
                    resolved_photo_path = str(p)
                    detected_caption = detected_caption or "PRESS PHOTO: Raftaar discussing DHH scene developments. (DHH ARCHIVE)"
            elif "prabh" in full_check or "tilak nagar" in full_check:
                p = artists_dir / "prabh_deep.jpg"
                if p.exists():
                    resolved_photo_path = str(p)
                    detected_caption = detected_caption or "PRESS PHOTO: Prabh Deep headlining live showcase in Delhi. (DHH ARCHIVE)"
            elif "brodha" in full_check or "bengaluru" in full_check:
                p = artists_dir / "brodha_v.jpg"
                if p.exists():
                    resolved_photo_path = str(p)
                    detected_caption = detected_caption or "PRESS PHOTO: Brodha V representing South Indian lyricism. (DHH ARCHIVE)"

        if resolved_photo_path and Path(resolved_photo_path).exists():
            try:
                from PIL import ImageOps, ImageEnhance
                with Image.open(resolved_photo_path) as p_img:
                    fitted = ImageOps.fit(p_img, (box_w, box_h), method=Image.Resampling.LANCZOS, centering=(0.5, 0.3))
                    # Authentic newsprint print photo treatment
                    enhancer = ImageEnhance.Color(fitted)
                    vintage = enhancer.enhance(0.75)
                    contrast = ImageEnhance.Contrast(vintage)
                    final_photo = contrast.enhance(1.2)
                    img.paste(final_photo, (px1 + 30, img_box_y))
                    draw.rectangle([px1 + 30, img_box_y, px2 - 30, img_box_y + box_h], outline="#2B2825", width=2)
                    photo_placed = True
            except Exception:
                photo_placed = False

        if not photo_placed:
            # Fallback graphic inside photo box
            draw.rectangle([px1 + 30, img_box_y, px2 - 30, img_box_y + box_h], fill="#1E2024", outline="#4B5563", width=2)
            draw.ellipse([width // 2 - 60, img_box_y + 35, width // 2 + 60, img_box_y + 155], fill="#2D3139", outline="#60A5FA", width=3)
            font_mic = self._get_serif_font(48, bold=True)
            draw.text((width // 2, img_box_y + 90), "🎙️", font=font_mic, fill="#FFFFFF", anchor="mm")
            font_box_tag = self._get_serif_font(22, bold=True)
            draw.text((width // 2, img_box_y + 180), "[ SCENE EVIDENCE: RECORDING BOOTH ARCHIVE ]", font=font_box_tag, fill="#FBBF24", anchor="mm")

        # Photo Caption
        caption_text = detected_caption or "FILE PHOTO: Certified DHH live performance archive. (PRESS BUREAU)"
        font_cap = self._get_serif_font(18, italic=True)
        draw.text((px1 + 35, img_box_y + box_h + 8), caption_text, font=font_cap, fill="#57534E")

        # Two Columns Newspaper Layout
        col_y = img_box_y + box_h + 38
        col_w = (px2 - px1 - 90) // 2
        mid_x = px1 + 30 + col_w + 15

        # Vertical dividing hairline
        draw.line([(mid_x, col_y), (mid_x, height - 120)], fill="#A8A29E", width=1)

        # Left Column text
        font_body = self._get_serif_font(20)
        default_story = story_body or "The Desi Hip-Hop underground scene experienced unprecedented activity as artists unveiled major upcoming drops. Scene commentators report heavy 808 bass frequencies disturbing normal routines. Production teams confirm the records carry zero compromises."
        l_lines = self._wrap_text(default_story, draw, font_body, col_w - 20)
        ly = col_y
        for l in l_lines[:5]:
            draw.text((px1 + 30, ly), l, font=font_body, fill="#1C1917")
            ly += 26

        # Right Column text
        font_box_h = self._get_serif_font(20, bold=True)
        draw.text((mid_x + 15, col_y), "COMMUNITY WITNESS REPORTS:", font=font_box_h, fill="#0F0E0D")
        default_quote = witness_quote or '"Bhai ne ek line mein poora existential crisis describe kar diya," stated one listener. Engineers noted FL Studio crashed under the sub-bass.'
        r_lines = self._wrap_text(default_quote, draw, font_body, col_w - 20)
        ry = col_y + 30
        for l in r_lines[:4]:
            draw.text((mid_x + 15, ry), l, font=font_body, fill="#1C1917")
            ry += 26

        # Newspaper bottom footer
        draw.line([(px1 + 30, height - 110), (px2 - 30, height - 110)], fill="#1A1A1A", width=2)
        # Barcode
        for bx in range(px1 + 35, px1 + 180, 5):
            bw = 2 if bx % 10 == 0 else 1
            draw.line([(bx, height - 95), (bx, height - 55)], fill="#1A1A1A", width=bw)
        font_barcode = self._get_serif_font(14)
        draw.text((px1 + 195, height - 75), "ARCHIVE NO: DHH-2026-X9 • VERIFIED CLIPPING", font=font_barcode, fill="#57534E")
        draw.text((px2 - 35, height - 75), f"PRESERVED & CURATED BY {source_tag}", font=self._get_serif_font(18, bold=True), fill="#111111", anchor="ra")

        file_id = f"newspaper_{uuid.uuid4().hex[:10]}.png"
        file_path = self.output_dir / file_id
        img.save(str(file_path), "PNG", quality=95)

        return {
            "file_name": file_id,
            "file_path": str(file_path),
            "width": width,
            "height": height,
            "format": "PNG",
            "template": "NEWSPAPER_CUTTING"
        }

    def create_breaking_news_meme(
        self,
        headline: str,
        subtext: str,
        news_tag: str = "DHH RADAR",
        breaking_ticker: Optional[str] = None,
        source_tag: str = "@azpadhai"
    ) -> Dict[str, Any]:
        """Render a high-impact 'Breaking News / Rap Radar Alert' meme card (1080x1080)."""
        width, height = 1080, 1080
        img = Image.new("RGB", (width, height), color="#080B11")
        draw = ImageDraw.Draw(img)

        # 1. Dark vignette background with subtle radial glow
        cx, cy = width // 2, height // 2
        for r in range(540, 0, -12):
            val = int(22 * (1 - r / 540))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(val, val + 2, val + 8))

        # 2. Top Header Bar with Breaking Alert
        draw.rectangle([0, 0, width, 110], fill="#0F172A")
        # Pulsing Red Alert Pill
        draw.rounded_rectangle([40, 25, 410, 85], radius=14, fill="#DC2626")
        draw.ellipse([55, 45, 75, 65], fill="#FFFFFF")
        font_pill = self._get_font(26, bold=True)
        draw.text((90, 42), "BREAKING NEWS 🚨", font=font_pill, fill="#FFFFFF")

        # Live Indicator & Tag
        font_subhead = self._get_font(22, bold=True)
        draw.text((430, 45), f"● LIVE INTEL • {news_tag.upper()}", font=font_subhead, fill="#EF4444")
        draw.text((width - 50, 42), source_tag, font=font_pill, fill="#94A3B8", anchor="ra")

        # 3. Central Broadcast Visual Frame (1000x580)
        card_x1, card_y1, card_x2, card_y2 = 40, 130, width - 40, 720
        draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=24, fill="#131B2E", outline="#334155", width=3)

        # Audio Equalizer Bars / Graphic at top of card
        eq_x = card_x1 + 45
        eq_y = card_y1 + 35
        bar_heights = [24, 45, 60, 35, 75, 50, 85, 40, 65, 30, 70, 55, 80, 45, 60, 30]
        for i, bh in enumerate(bar_heights):
            color = "#F59E0B" if i % 2 == 0 else "#38BDF8"
            draw.rounded_rectangle([eq_x + i * 16, eq_y + (85 - bh), eq_x + i * 16 + 10, eq_y + 85], radius=4, fill=color)

        font_badge = self._get_font(22, bold=True)
        draw.rounded_rectangle([card_x2 - 270, card_y1 + 35, card_x2 - 40, card_y1 + 75], radius=10, fill="#1E293B", outline="#475569")
        draw.text((card_x2 - 155, card_y1 + 45), "SCENE DISPATCH", font=font_badge, fill="#FBBF24", anchor="mm")

        # Headline (Large, impactful, wrapped)
        font_hl = self._get_font(44, bold=True)
        hl_lines = self._wrap_text(headline, draw, font_hl, 900)
        curr_y = card_y1 + 150
        for l in hl_lines:
            draw.text((card_x1 + 45, curr_y), l, font=font_hl, fill="#F8FAFC")
            curr_y += 58

        curr_y += 20
        # Subtext / Context
        font_st = self._get_font(32)
        st_lines = self._wrap_text(subtext, draw, font_st, 900)
        for l in st_lines:
            draw.text((card_x1 + 45, curr_y), l, font=font_st, fill="#94A3B8")
            curr_y += 44

        # 4. Impact Callout Card (Bottom of frame)
        callout_y1, callout_y2 = 745, 935
        draw.rounded_rectangle([40, callout_y1, width - 40, callout_y2], radius=18, fill="#1E1B4B", outline="#6366F1", width=2)
        font_co_tag = self._get_font(20, bold=True)
        draw.rounded_rectangle([60, callout_y1 + 20, 260, callout_y1 + 55], radius=8, fill="#6366F1")
        draw.text((160, callout_y1 + 30), "COMMUNITY SENTIMENT", font=font_co_tag, fill="#FFFFFF", anchor="mm")
        font_co = self._get_font(30, bold=True)
        draw.text((60, callout_y1 + 80), "💬 DHH Audience: 'Bars aur production dono top notch hain!'", font=font_co, fill="#E0E7FF")
        draw.text((60, callout_y1 + 125), "👉 Tag that one friend who needs to hear this news! 👇", font=self._get_font(26), fill="#FACC15")

        # 5. Bottom Scrolling News Ticker
        ticker_y = height - 100
        draw.rectangle([0, ticker_y, width, height], fill="#FACC15")
        font_ticker = self._get_font(24, bold=True)
        t_text = breaking_ticker or "⚡ TICKER: Hanumankind 'Big Dawgs' still playing worldwide • Seedhe Maut drops cryptic story • Producer waiting for stems..."
        draw.text((40, ticker_y + 35), t_text[:90], font=font_ticker, fill="#000000")

        file_id = f"news_{uuid.uuid4().hex[:10]}.png"
        file_path = self.output_dir / file_id
        img.save(str(file_path), "PNG", quality=95)

        return {
            "file_name": file_id,
            "file_path": str(file_path),
            "width": width,
            "height": height,
            "format": "PNG",
            "template": "BREAKING_NEWS"
        }

    def create_scorecard_meme(
        self,
        artist: str,
        track_title: str,
        scores: Optional[Dict[str, float]] = None,
        verdict: str = "CERTIFIED BANGER 🏆",
        commentary: str = "Bars, cadence and 808 distortion perfectly engineered.",
        source_tag: str = "@azpadhai"
    ) -> Dict[str, Any]:
        """Render an official DHH Music Critic Scorecard & Track Audit meme (1080x1080)."""
        width, height = 1080, 1080
        img = Image.new("RGB", (width, height), color="#0B0F19")
        draw = ImageDraw.Draw(img)

        # 1. Subtle Carbon Grid
        for y in range(0, height, 40):
            draw.line([(0, y), (width, y)], fill="#111827", width=1)
        for x in range(0, width, 40):
            draw.line([(x, 0), (x, height)], fill="#111827", width=1)

        # 2. Header Box
        draw.rounded_rectangle([40, 40, width - 40, 200], radius=20, fill="#161F30", outline="#374151", width=2)
        font_tag = self._get_font(20, bold=True)
        draw.rounded_rectangle([70, 60, 380, 95], radius=8, fill="#0284C7")
        draw.text((225, 70), "DHH TRACK AUDIT & CRITIC", font=font_tag, fill="#FFFFFF", anchor="mm")
        draw.text((width - 70, 70), source_tag, font=font_tag, fill="#9CA3AF", anchor="ra")

        font_track = self._get_font(42, bold=True)
        draw.text((70, 115), f'"{track_title}"', font=font_track, fill="#F8FAFC")
        font_art = self._get_font(28)
        draw.text((70, 160), f"Artist: {artist} • Verified Scene Analysis", font=font_art, fill="#38BDF8")

        # Vinyl Record Icon graphic on top right
        icon_cx, icon_cy = width - 130, 140
        draw.ellipse([icon_cx - 45, icon_cy - 45, icon_cx + 45, icon_cy + 45], fill="#111827", outline="#F59E0B", width=3)
        draw.ellipse([icon_cx - 15, icon_cy - 15, icon_cx + 15, icon_cy + 15], fill="#EF4444")
        draw.ellipse([icon_cx - 5, icon_cy - 5, icon_cx + 5, icon_cy + 5], fill="#FFFFFF")

        # 3. Rating Meter Bars
        default_meters = [
            ("Flow & Rhyme Schemes", 9.7, "#06B6D4"),
            ("808 Bass & Sub Punch", 9.5, "#F59E0B"),
            ("Car Speaker Survival", 10.0, "#10B981"),
            ("Replay Value at 2 AM", 9.8, "#8B5CF6")
        ]
        
        meter_data = []
        if scores:
            colors = ["#06B6D4", "#F59E0B", "#10B981", "#8B5CF6"]
            for i, (k, v) in enumerate(scores.items()):
                color = colors[i % len(colors)]
                meter_data.append((k, float(v), color))
        else:
            meter_data = default_meters

        bar_start_y = 230
        font_label = self._get_font(24, bold=True)
        font_val = self._get_font(26, bold=True)

        for i, (label, score_val, color) in enumerate(meter_data[:4]):
            y = bar_start_y + i * 105
            # Label
            draw.text((70, y), f"{i+1}. {label.upper()}", font=font_label, fill="#E2E8F0")
            # Score
            draw.text((width - 70, y), f"{score_val:.1f} / 10", font=font_val, fill=color, anchor="ra")
            
            # Bar background
            bar_y = y + 36
            draw.rounded_rectangle([70, bar_y, width - 70, bar_y + 18], radius=9, fill="#1F2937")
            # Filled bar
            fill_w = int((width - 140) * (min(10.0, score_val) / 10.0))
            draw.rounded_rectangle([70, bar_y, 70 + fill_w, bar_y + 18], radius=9, fill=color)

        # 4. Final Verdict Box
        verdict_y = 675
        draw.rounded_rectangle([40, verdict_y, width - 40, verdict_y + 175], radius=20, fill="#1E1B4B", outline="#F59E0B", width=3)
        font_v_title = self._get_font(22, bold=True)
        draw.text((70, verdict_y + 25), "OFFICIAL VERDICT:", font=font_v_title, fill="#F59E0B")
        font_v_big = self._get_font(38, bold=True)
        draw.text((70, verdict_y + 60), verdict.upper(), font=font_v_big, fill="#F8FAFC")
        
        font_c = self._get_font(28)
        c_lines = self._wrap_text(f'"{commentary}"', draw, font_c, 900)
        cy = verdict_y + 115
        for l in c_lines[:2]:
            draw.text((70, cy), l, font=font_c, fill="#A78BFA")
            cy += 38

        # 5. Footer Call to Action
        draw.rounded_rectangle([40, 880, width - 40, 1025], radius=16, fill="#111827")
        font_cta = self._get_font(28, bold=True)
        draw.text((width // 2, 925), "Do you agree with this rating? Drop your score below 👇", font=font_cta, fill="#FFFFFF", anchor="mm")
        draw.text((width // 2, 975), f"Follow {source_tag} for daily honest DHH track breakdowns", font=self._get_font(24), fill="#94A3B8", anchor="mm")

        file_id = f"score_{uuid.uuid4().hex[:10]}.png"
        file_path = self.output_dir / file_id
        img.save(str(file_path), "PNG", quality=95)

        return {
            "file_name": file_id,
            "file_path": str(file_path),
            "width": width,
            "height": height,
            "format": "PNG",
            "template": "SCORECARD"
        }

    def create_desi_cult_meme(
        self,
        setup: str,
        punchline: str,
        cult_character: str = "BABU_BHAIYA",
        dialogue: Optional[str] = None,
        source_tag: str = "@azpadhai"
    ) -> Dict[str, Any]:
        """Render a classic Bollywood/Desi Cult reaction meme adapted for DHH (1080x1080)."""
        width, height = 1080, 1080
        img = Image.new("RGB", (width, height), color="#0F172A")
        draw = ImageDraw.Draw(img)

        # Header Bar
        draw.rectangle([0, 0, width, 100], fill="#020617")
        draw.text((50, 32), "🎬 DESI CULT CLASSIC • DHH MEME", font=self._get_font(32, bold=True), fill="#FBBF24")
        draw.text((width - 50, 32), source_tag, font=self._get_font(28, bold=True), fill="#94A3B8", anchor="ra")

        # Top Panel: Situation / Expectation
        top_y1, top_y2 = 130, 480
        draw.rounded_rectangle([40, top_y1, width - 40, top_y2], radius=20, fill="#1E293B", outline="#475569", width=2)
        draw.rounded_rectangle([65, top_y1 + 25, 380, top_y1 + 75], radius=10, fill="#EF4444")
        font_badge = self._get_font(24, bold=True)
        draw.text((80, top_y1 + 38), "SITUATION IN DHH", font=font_badge, fill="#FFFFFF")

        font_text = self._get_font(38, bold=True)
        top_lines = self._wrap_text(setup, draw, font_text, 900)
        ty = top_y1 + 110
        for l in top_lines:
            draw.text((70, ty), l, font=font_text, fill="#F8FAFC")
            ty += 54

        # Bottom Panel: Cult Reaction (e.g. Babu Bhaiya)
        bot_y1, bot_y2 = 510, 940
        draw.rounded_rectangle([40, bot_y1, width - 40, bot_y2], radius=20, fill="#0F172A", outline="#F59E0B", width=3)
        draw.rounded_rectangle([65, bot_y1 + 25, 420, bot_y1 + 75], radius=10, fill="#10B981")
        draw.text((80, bot_y1 + 38), "DESI AUDIENCE REACTION", font=font_badge, fill="#FFFFFF")

        # Stylized Babu Bhaiya visual representation
        char_cx, char_cy = 180, bot_y1 + 230
        draw.ellipse([char_cx - 90, char_cy - 90, char_cx + 90, char_cy + 90], fill="#F3A683")
        # Thick Babu Bhaiya specs
        draw.rounded_rectangle([char_cx - 80, char_cy - 30, char_cx - 10, char_cy + 20], radius=12, fill="#FFFFFF", outline="#000000", width=6)
        draw.rounded_rectangle([char_cx + 10, char_cy - 30, char_cx + 80, char_cy + 20], radius=12, fill="#FFFFFF", outline="#000000", width=6)
        draw.line([(char_cx - 10, char_cy - 5), (char_cx + 10, char_cy - 5)], fill="#000000", width=6)
        # Funny eyes
        draw.ellipse([char_cx - 50, char_cy - 12, char_cx - 38, char_cy + 2], fill="#000000")
        draw.ellipse([char_cx + 38, char_cy - 12, char_cx + 50, char_cy + 2], fill="#000000")
        # Red Tilak
        draw.rectangle([char_cx - 6, char_cy - 70, char_cx + 6, char_cy - 40], fill="#DC2626")
        # Shouting mouth
        draw.ellipse([char_cx - 28, char_cy + 35, char_cx + 28, char_cy + 75], fill="#881337")
        # Dhoti/Kurta Collar
        draw.polygon([(char_cx - 80, char_cy + 85), (char_cx + 80, char_cy + 85), (char_cx, char_cy + 130)], fill="#FFFFFF")

        # Speech Bubble on right
        bubble_x1, bubble_y1, bubble_x2, bubble_y2 = 310, bot_y1 + 105, width - 65, bot_y2 - 35
        draw.rounded_rectangle([bubble_x1, bubble_y1, bubble_x2, bubble_y2], radius=18, fill="#FEF08A", outline="#CA8A04", width=2)
        # Speech pointer
        draw.polygon([(bubble_x1, bubble_y1 + 75), (bubble_x1 - 25, bubble_y1 + 95), (bubble_x1, bubble_y1 + 115)], fill="#FEF08A")

        diag = dialogue or "Arey baba! Ek line samajh mein nahi aayi lekin vibe poori hard hai! 💀"
        font_diag = self._get_font(34, bold=True)
        diag_lines = self._wrap_text(diag, draw, font_diag, 630)
        dy = bubble_y1 + 35
        for l in diag_lines:
            draw.text((bubble_x1 + 30, dy), l, font=font_diag, fill="#000000")
            dy += 48

        # Footer
        draw.rectangle([0, 970, width, height], fill="#020617")
        font_foot = self._get_font(26, bold=True)
        draw.text((width // 2, 1025), f"👉 {punchline}", font=font_foot, fill="#FBBF24", anchor="mm")

        file_id = f"cult_{uuid.uuid4().hex[:10]}.png"
        file_path = self.output_dir / file_id
        img.save(str(file_path), "PNG", quality=95)

        return {
            "file_name": file_id,
            "file_path": str(file_path),
            "width": width,
            "height": height,
            "format": "PNG",
            "template": "DESI_CULT"
        }

    def create_dm_chat_meme(
        self,
        sender_name: str,
        messages: list[dict],
        punchline: str,
        source_tag: str = "@azpadhai"
    ) -> Dict[str, Any]:
        """Render a realistic Dark Mode DM conversation meme (1080x1080)."""
        width, height = 1080, 1080
        img = Image.new("RGB", (width, height), color="#090D16")
        draw = ImageDraw.Draw(img)

        # Header: Chat Top Bar
        draw.rectangle([0, 0, width, 120], fill="#161B26")
        # Avatar
        draw.ellipse([50, 25, 120, 95], fill="#7C3AED")
        draw.text((85, 45), sender_name[:2].upper(), font=self._get_font(28, bold=True), fill="#FFFFFF", anchor="mm")

        font_name = self._get_font(32, bold=True)
        draw.text((140, 42), sender_name, font=font_name, fill="#F8FAFC")
        draw.text((140, 80), "Active in Studio • 4 AM", font=self._get_font(22), fill="#22C55E")

        # Action icons
        draw.text((width - 180, 45), "📞", font=self._get_font(30), fill="#94A3B8")
        draw.text((width - 120, 45), "📹", font=self._get_font(30), fill="#94A3B8")
        draw.text((width - 60, 45), "ℹ️", font=self._get_font(30), fill="#94A3B8")

        # Chat Bubble Area
        curr_y = 150
        font_msg = self._get_font(30)
        font_time = self._get_font(20)

        for msg in messages:
            is_me = (msg.get("sender", "them").lower() == "me")
            text = msg.get("text", "")
            time_str = msg.get("time", "")

            lines = self._wrap_text(text, draw, font_msg, 620)
            box_h = max(58, len(lines) * 42 + 36)
            box_w = 660

            if is_me:
                bx1 = width - box_w - 50
                bx2 = width - 50
                fill_color = "#6366F1"
                text_color = "#FFFFFF"
            else:
                bx1 = 50
                bx2 = 50 + box_w
                fill_color = "#27272A"
                text_color = "#F4F4F5"

            draw.rounded_rectangle([bx1, curr_y, bx2, curr_y + box_h], radius=18, fill=fill_color)
            
            ty = curr_y + 16
            for l in lines:
                draw.text((bx1 + 25, ty), l, font=font_msg, fill=text_color)
                ty += 42

            if time_str:
                draw.text((bx2 - 20, curr_y + box_h - 18), time_str, font=font_time, fill="#D1D5DB" if is_me else "#9CA3AF", anchor="ra")

            curr_y += box_h + 20

        # Read receipt
        draw.text((width - 50, curr_y), "✓✓ Seen • No reply", font=self._get_font(22), fill="#64748B", anchor="ra")

        # Bottom Punchline Bar
        p_y1 = height - 160
        draw.rounded_rectangle([40, p_y1, width - 40, height - 40], radius=18, fill="#1E1B4B", outline="#A855F7", width=2)
        font_p = self._get_font(30, bold=True)
        draw.text((width // 2, p_y1 + 42), f"💀 {punchline}", font=font_p, fill="#FACC15", anchor="mm")
        draw.text((width // 2, p_y1 + 84), f"Follow {source_tag} for authentic DHH culture & memes", font=self._get_font(24), fill="#E2E8F0", anchor="mm")

        file_id = f"dm_{uuid.uuid4().hex[:10]}.png"
        file_path = self.output_dir / file_id
        img.save(str(file_path), "PNG", quality=95)

        return {
            "file_name": file_id,
            "file_path": str(file_path),
            "width": width,
            "height": height,
            "format": "PNG",
            "template": "DM_CHAT"
        }

    def create_remixed_meme(
        self,
        topic: str,
        original_meme_text: str,
        fresh_spin: str,
        punchline: str,
        source_tag: str = "@azpadhai"
    ) -> Dict[str, Any]:
        """Render a remixed & regenerated community meme with @azpadhai visual branding (1080x1080)."""
        width, height = 1080, 1080
        img = Image.new("RGB", (width, height), color="#0F172A")
        draw = ImageDraw.Draw(img)

        # Header Bar
        draw.rectangle([0, 0, width, 110], fill="#020617")
        draw.text((50, 35), "⚡ COMMUNITY MEME REMIX • DHH 2026", font=self._get_font(32, bold=True), fill="#38BDF8")
        draw.text((width - 50, 35), source_tag, font=self._get_font(28, bold=True), fill="#94A3B8", anchor="ra")

        # Topic Badge
        draw.rounded_rectangle([50, 130, 520, 180], radius=12, fill="#7C3AED")
        draw.text((70, 142), f"RE: {topic.upper()[:28]}", font=self._get_font(24, bold=True), fill="#FFFFFF")

        # Top Card: The Classic Meme Trope
        draw.rounded_rectangle([40, 200, width - 40, 520], radius=20, fill="#1E293B", outline="#475569", width=2)
        draw.rounded_rectangle([60, 220, 350, 265], radius=10, fill="#64748B")
        draw.text((75, 232), "THE CLASSIC DHH TROPE", font=self._get_font(22, bold=True), fill="#FFFFFF")
        
        font_txt = self._get_font(36, bold=True)
        top_lines = self._wrap_text(original_meme_text, draw, font_txt, 900)
        ty = 290
        for l in top_lines:
            draw.text((70, ty), l, font=font_txt, fill="#CBD5E1")
            ty += 50

        # Bottom Card: Fresh 2026 Scene Reality
        draw.rounded_rectangle([40, 545, width - 40, 870], radius=20, fill="#1E1B4B", outline="#38BDF8", width=3)
        draw.rounded_rectangle([60, 565, 370, 610], radius=10, fill="#0284C7")
        draw.text((75, 577), "FRESH 2026 SCENE TWIST", font=self._get_font(22, bold=True), fill="#FFFFFF")

        bot_lines = self._wrap_text(fresh_spin, draw, font_txt, 900)
        by = 635
        for l in bot_lines:
            draw.text((70, by), l, font=font_txt, fill="#F8FAFC")
            by += 50

        # Footer Punchline
        draw.rectangle([0, 895, width, height], fill="#020617")
        font_p = self._get_font(32, bold=True)
        draw.text((width // 2, 940), f"🔥 {punchline}", font=font_p, fill="#FACC15", anchor="mm")
        draw.text((width // 2, 985), f"Regenerated & Curated by {source_tag} • Desi Hip-Hop Media", font=self._get_font(24), fill="#94A3B8", anchor="mm")

        file_id = f"remix_{uuid.uuid4().hex[:10]}.png"
        file_path = self.output_dir / file_id
        img.save(str(file_path), "PNG", quality=95)

        return {
            "file_name": file_id,
            "file_path": str(file_path),
            "width": width,
            "height": height,
            "format": "PNG",
            "template": "MEME_REMIX"
        }

    def create_tweet_card_meme(
        self,
        hook: str,
        content_text: str,
        punchline: Optional[str] = None,
        category: str = "DHH_MEME"
    ) -> Dict[str, Any]:
        """Render a sleek, high-engagement Twitter/X style dark theme meme card (1080x1080)."""
        width, height = 1080, 1080
        img = Image.new("RGB", (width, height), color="#0F172A")
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
        draw.text((190, 145), "@azpadhai • 1h ago", font=font_handle, fill="#94A3B8")

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
        """Render a 2-panel comparison meme (1080x1080)."""
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

        # Album front cover
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

        # 4. Song Details
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
        parts = [p.strip() for p in content_text.split("\n\n") if p.strip()]

        if "news" in cat_lower or "newspaper" in cat_lower or "radar" in cat_lower or "alert" in cat_lower or "breaking" in cat_lower:
            return self.create_newspaper_cutting_meme(
                headline=hook,
                subtext=parts[0] if parts else content_text,
                story_body=parts[1] if len(parts) > 1 else content_text,
                witness_quote=punchline,
                edition_tag="DELHI / MUMBAI PRESS ARCHIVE"
            )
        elif "scorecard" in cat_lower or "review" in cat_lower or "audit" in cat_lower or "critic" in cat_lower:
            track = hook.replace("Track Review:", "").replace("Audit:", "").strip()
            return self.create_scorecard_meme(
                artist="DHH Heavyweight",
                track_title=track[:40],
                scores={
                    "Flow & Rhyme Schemes": 9.7,
                    "808 Bass & Sub Punch": 9.5,
                    "Car Speaker Survival": 10.0,
                    "Replay Value at 2 AM": 9.8
                },
                verdict="CERTIFIED BANGER 🏆",
                commentary=punchline or (parts[0] if parts else "Pure cultural fire")
            )
        elif "cult" in cat_lower or "hera_pheri" in cat_lower or "bollywood" in cat_lower or "desi" in cat_lower:
            setup = parts[0] if parts else hook
            p_line = punchline or (parts[1] if len(parts) > 1 else "Bhai vibe alag hai")
            return self.create_desi_cult_meme(
                setup=setup,
                punchline=p_line,
                cult_character="BABU_BHAIYA",
                dialogue=f"Arey baba! {p_line}"
            )
        elif "chat" in cat_lower or "dm" in cat_lower or "whatsapp" in cat_lower or "producer" in cat_lower:
            msgs = [
                {"sender": "them", "text": parts[0] if parts else "Bhai beat export ho gayi? Aaj raat vocal record karni hai.", "time": "11:42 PM"},
                {"sender": "me", "text": "Haan bhai bas 2 min, mastering chain lag rahi hai.", "time": "11:45 PM"},
                {"sender": "them", "text": "Bhai 3 ghante ho gaye... studio time khatam ho raha hai.", "time": "2:50 AM"},
                {"sender": "me", "text": parts[1] if len(parts) > 1 else "Bhai FL Studio crash ho gaya aur backup corrupt hai 💀", "time": "3:14 AM"}
            ]
            return self.create_dm_chat_meme(
                sender_name="Delhi Producer 🎹",
                messages=msgs,
                punchline=punchline or "Every single studio session in DHH history 💀"
            )
        elif "remix" in cat_lower:
            return self.create_remixed_meme(
                topic=hook[:30],
                original_meme_text=parts[0] if parts else hook,
                fresh_spin=parts[1] if len(parts) > 1 else "The 2026 scene reality hits even harder.",
                punchline=punchline or "Regenerated for @azpadhai audience"
            )
        elif "release" in cat_lower or "track" in cat_lower or "spotify" in cat_lower:
            lyrics = parts[0] if parts else content_text
            p_line = punchline or (parts[1] if len(parts) > 1 else "Every single time in DHH 💀")
            return self.create_spotify_player_meme(
                song_title=hook[:40],
                artist="Desi Hip-Hop Cult • Verified Banger",
                lyrics_quote=lyrics[:140],
                punchline=p_line[:100]
            )
        elif "war" in cat_lower or "battle" in cat_lower or "drake" in cat_lower:
            top = parts[0] if parts else hook
            bottom = parts[1] if len(parts) > 1 else (punchline or content_text)
            return self.create_drake_reaction_meme(
                reject_text=top[:120],
                approve_text=bottom[:120],
                category=category
            )
        else:
            # Randomly select between the diverse visual styles for rich daily variety
            choices = ["news", "scorecard", "cult", "chat", "spotify", "drake"]
            selected = random.choice(choices)
            # Re-call with selected category
            return self.create_human_meme(hook, content_text, punchline, category=f"DHH_{selected.upper()}")

meme_engine = MemeEngine()
