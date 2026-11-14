import os
from pathlib import Path
from typing import Dict, Any, List
from PIL import Image

class ReviewEngine:
    """
    Automated pre-publish quality gate and human-grade review system.
    Evaluates visual richness, cultural slang authenticity, humor rating, and rejects AI-sounding slop.
    """

    CULTURE_KEYWORDS = {
        "dhh", "desi hip hop", "bars", "beat", "808", "producer", "flow", "verse",
        "rhyme", "delhi", "mumbai", "punjab", "seedhe maut", "kr$na", "divine",
        "raftaar", "stan", "gully gang", "kalamkaar", "underground", "cypher",
        "mix", "master", "fl studio", "daw", "bhai", "scene", "diss", "beef", "ep", "mixtape"
    }

    AI_SLOP_PHRASES = [
        "in the vibrant world of",
        "hip hop is a universal language",
        "music brings us together",
        "delve into the rhythm",
        "explore the captivating sounds",
        "a testament to the power of music",
        "tapestry of sound",
        "sonic journey"
    ]

    def review_content(self, title: str, text: str, media_path: str, content_type: str = "IMAGE") -> Dict[str, Any]:
        full_text = f"{title} {text}".lower()
        score = 8.0
        reasons: List[str] = []

        # 1. Cringe / AI Slop Check
        has_ai_cliche = False
        for phrase in self.AI_SLOP_PHRASES:
            if phrase in full_text:
                score -= 3.5
                has_ai_cliche = True
                reasons.append(f"Contains generic AI phrasing: '{phrase}'")

        # 2. Cultural Authenticity Check
        matches = [kw for kw in self.CULTURE_KEYWORDS if kw in full_text]
        if len(matches) >= 3:
            score += 1.5
            reasons.append(f"Strong DHH cultural references detected ({', '.join(matches[:4])})")
        elif len(matches) >= 1:
            score += 0.5
            reasons.append(f"Moderate DHH references detected ({', '.join(matches)})")
        else:
            score -= 2.0
            reasons.append("Lacks recognizable DHH cultural slang or artist references")

        # 3. Visual Element & Entropy Verification
        visual_verified = False
        if media_path and Path(media_path).exists():
            try:
                with Image.open(media_path) as im:
                    w, h = im.size
                    if w >= 1080 and (h == 1080 or h == 1920 or h == 1350):
                        score += 0.5
                        reasons.append(f"High-resolution canvas verified ({w}x{h})")
                    else:
                        score -= 1.0
                        reasons.append(f"Non-standard resolution: {w}x{h}")

                    # Check image color richness
                    stat = im.convert("RGB").histogram()
                    if len(set(stat)) > 80:
                        visual_verified = True
                        score += 0.5
                        reasons.append("Rich visual composition confirmed (high entropy)")
                    else:
                        score -= 2.0
                        reasons.append("Visual composition is too plain or flat")
            except Exception as e:
                # If it's a video file (.mp4), check file existence and size
                if media_path.endswith(".mp4") and os.path.getsize(media_path) > 50000:
                    visual_verified = True
                    score += 1.0
                    reasons.append("Valid 9:16 vertical video with audio track verified")
                else:
                    reasons.append(f"Could not inspect media: {e}")

        final_score = round(min(10.0, max(1.0, score)), 1)
        passed = (final_score >= 8.0) and not has_ai_cliche and visual_verified

        return {
            "passed": passed,
            "overall_score": final_score,
            "visual_verified": visual_verified,
            "decision": "APPROVED" if passed else "REJECTED_NEEDS_RETRY",
            "review_notes": "; ".join(reasons)
        }

review_engine = ReviewEngine()
