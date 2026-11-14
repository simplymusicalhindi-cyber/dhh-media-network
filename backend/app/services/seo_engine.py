import random
from typing import Dict, Any, List
from backend.app.models.seo import BioProfileRecommendation

class SEOEngine:
    PRIMARY_DHH_KEYWORDS = [
        "Desi Hip Hop", "DHH", "Indian Hip Hop", "Indian Rap", "Desi Rap",
        "Hip Hop Memes", "Underground Hip Hop", "Indian Rappers",
        "Desi Hip Hop Community", "Indian Music Culture", "TBSM", "Seedhe Maut",
        "KR$NA", "Divine", "MC Stan", "Gully Gang", "Kalamkaar"
    ]

    HASHTAG_CLUSTERS = {
        "PRODUCER": ["#DHHBeats", "#BeatmakersOfIndia", "#FLStudioIndia", "#DesiHipHop", "#MusicProducerLife"],
        "UNDERGROUND": ["#UndergroundHipHop", "#IndianRapScene", "#DesiHipHop", "#IndieArtistsIndia", "#RawBars"],
        "MAINSTREAM_DHH": ["#DHH", "#IndianHipHop", "#DesiHipHop", "#SeedheMaut", "#KR$NA"],
        "MEMES_HUMOR": ["#DHHMemes", "#IndianRapMemes", "#DesiMemes", "#RelatableHipHop", "#HipHopIndia"],
        "STUDIO_LIFE": ["#StudioStruggles", "#AudioEngineeringIndia", "#VocalMix", "#DHH", "#ProducerLife"]
    }

    def generate_optimized_caption(self, hook: str, body: str, cta: str, category: str = "MEMES_HUMOR") -> Dict[str, Any]:
        """Construct high-retention Instagram caption optimized for Instagram Search & Explore."""
        # Clean hook for the first 125 characters (visible before '...more')
        opening_hook = hook.strip()
        if len(opening_hook) > 115:
            opening_hook = opening_hook[:112] + "..."

        # Select 4-5 relevant hashtags
        cluster_key = "MEMES_HUMOR"
        for k in self.HASHTAG_CLUSTERS.keys():
            if k.lower() in category.lower():
                cluster_key = k
                break
        selected_hashtags = " ".join(self.HASHTAG_CLUSTERS[cluster_key])

        full_caption = f"{opening_hook}\n\n{body.strip()}\n\n{cta.strip()}\n\n.\n.\n{selected_hashtags}"

        return {
            "caption": full_caption,
            "opening_hook": opening_hook,
            "hashtags": selected_hashtags,
            "seo_score": 9.2,
            "keywords": [k for k in self.PRIMARY_DHH_KEYWORDS if k.lower() in full_caption.lower()]
        }

    def generate_bio_recommendations(self) -> List[Dict[str, Any]]:
        """Generate high-converting Instagram profile bios for the page."""
        return [
            {
                "username_suggestion": "desihiphop_vibes",
                "display_name": "DHH Media Network | Desi Hip Hop News & Memes",
                "bio_text": "⚡ The unfiltered heartbeat of Indian Hip-Hop.\n🎤 Relatable memes, producer pain & underground bars.\n🎧 Daily DHH breakdowns & underground spotlights.\n👇 Stream fresh heat & join the community!",
                "category": "Musician/Band / Media News Company",
                "cta": "Submit your music / memes via DM",
                "strategy_notes": "Contains high-intent search keywords: 'Desi Hip Hop', 'DHH', 'Underground bars'"
            },
            {
                "username_suggestion": "dhh_bars_daily",
                "display_name": "DHH BARS & MEMES 🇮🇳",
                "bio_text": "Terko Bhi Sab Milega 🚀\n🔥 Best Desi Hip Hop memes on the internet\n🎹 FL Studio crashes, 808 glides & lyrical breakdowns\n📩 DM for underground artist features",
                "category": "Entertainment Website",
                "cta": "Check today's story poll!",
                "strategy_notes": "Humor-first angle with TBSM cultural reference."
            }
        ]

seo_engine = SEOEngine()
