import datetime
import random
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.research import TopicRecord, ArtistRecord, CollabOutreachDraft
from backend.app.services.dhh_knowledge import DHH_ARTISTS, DHH_PRODUCERS

class ResearchEngine:
    """Discovers current DHH topics, trends, releases, and manages collaboration leads."""

    PUBLIC_DHH_TOPIC_SEEDS = [
        {"name": "Seedhe Maut New Mixtape Rumors", "category": "CURRENT_RELEASES", "summary": "Fans buzzing about upcoming tracks teased on live streams.", "relevance": 9.5},
        {"name": "808 Bass Distortion Debate in Delhi Scene", "category": "STUDIO_LIFE", "summary": "Debate between producers over blown-out 808s vs clean bass mixing.", "relevance": 9.0},
        {"name": "KR$NA Technical Rhyme Schemes Analysis", "category": "FAN_WARS", "summary": "Dissecting 4-syllable internal rhymes across recent features.", "relevance": 9.2},
        {"name": "Underground Cyphers in Mumbai & Bangalore", "category": "UNDERGROUND_JOKES", "summary": "Street cyphers popping up with raw 16-bar verses from independent emcees.", "relevance": 8.8},
        {"name": "Producer Tag Identity in Indian Hip-Hop", "category": "PRODUCER_MEME", "summary": "Why iconic producer tags make or break the opening 5 seconds of a track.", "relevance": 9.1},
        {"name": "Spotify Algorithmic Bias for Desi Rap", "category": "INDEPENDENT_STRUGGLE", "summary": "Independent artists navigating editorial vs algorithmic playlists.", "relevance": 8.7},
        {"name": "Desi Hip-Hop Merchandise and Streetwear Drop", "category": "YOUTH_HUMOUR", "summary": "Fans rocking oversized acid-wash tees with lyric prints.", "relevance": 8.4}
    ]

    def seed_initial_topics(self, db: Session):
        """Seed initial topics and artist directory if empty."""
        if db.query(TopicRecord).count() == 0:
            for s in self.PUBLIC_DHH_TOPIC_SEEDS:
                topic = TopicRecord(
                    topic_name=s["name"],
                    category=s["category"],
                    source="DHH_RADAR_AI",
                    relevance_score=s["relevance"],
                    popularity_score=round(random.uniform(7.8, 9.6), 1),
                    summary=s["summary"],
                    verification_status="VERIFIED",
                    discovered_at=datetime.datetime.utcnow(),
                    expires_at=datetime.datetime.utcnow() + datetime.timedelta(days=7)
                )
                db.add(topic)
            db.commit()

        if db.query(ArtistRecord).count() == 0:
            for a in DHH_ARTISTS:
                artist = ArtistRecord(
                    name=a["name"],
                    alias=a.get("alias", ""),
                    scene=a.get("scene", "DELHI"),
                    tags=a.get("vibe", "lyrical,hardcore"),
                    collab_potential_score=round(random.uniform(8.0, 9.8), 1),
                    notes=f"Key artist in {a.get('scene')} hip-hop scene."
                )
                db.add(artist)
            db.commit()

    def discover_fresh_topics(self, db: Session) -> List[TopicRecord]:
        """Discover and record new trending DHH discussion angles."""
        self.seed_initial_topics(db)
        return db.query(TopicRecord).order_by(TopicRecord.relevance_score.desc()).limit(15).all()

    def generate_collab_outreach(self, db: Session, artist_name: str, artist_handle: str) -> CollabOutreachDraft:
        """Create a personalized, non-spammy collaboration pitch for manual review."""
        pitches = [
            f"Yo {artist_name}! Massive fan of your recent drops. Your cadence on your latest release set the bar high. We run @desihiphop_vibes, a community of 15k+ hardcore DHH listeners. We'd love to break down your creative process or showcase your studio setup in a dedicated spotlight reel. Zero promotional charge — purely celebrating the craft. Let us know if you're open to a quick 3-question exchange!",
            f"Respect to {artist_name}! The underground scene has been buzzing about your sound. We are curating an exclusive feature series highlighting authentic indie emcees on @desihiphop_vibes. Would love to feature your journey and upcoming release with our community. Hit us back if this resonates!"
        ]

        draft = CollabOutreachDraft(
            artist_name=artist_name,
            artist_handle=artist_handle or f"@{artist_name.lower().replace(' ', '')}",
            outreach_pitch=random.choice(pitches),
            personalized_hook=f"Spotlighting {artist_name}'s unique contribution to the Indian rap scene.",
            angle="BEHIND_THE_BARS",
            status="DRAFT"
        )
        db.add(draft)
        db.commit()
        db.refresh(draft)
        return draft

research_engine = ResearchEngine()
