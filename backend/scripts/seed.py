
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models.complaint import Complaint


SAMPLE_COMPLAINTS = [
    ("A water pipe has been leaking near our street for several days.", "Sector G-10", "water", "normal", "open"),
    ("A broken street light is making the road unsafe at night.", "Sector F-8", "streetlights", "high", "open"),
    ("Garbage has not been collected from our neighborhood.", "Sector I-8", "sanitation", "normal", "in_progress"),
    ("There is a large pothole near the school entrance.", "Sector G-9", "roads", "high", "open"),
    ("An exposed electric wire is hanging near a footpath.", "Sector H-11", "electricity", "high", "open"),
    ("Water supply has been interrupted in our street.", "Sector G-11", "water", "normal", "resolved"),
    ("Several streetlights are not working on the main road.", "Sector F-10", "streetlights", "normal", "open"),
    ("Sewage water is overflowing outside residential houses.", "Sector I-10", "sanitation", "high", "in_progress"),
    ("The road surface has broken near the market.", "Sector G-6", "roads", "normal", "open"),
    ("A power outage has affected our neighborhood.", "Sector F-7", "electricity", "high", "resolved"),
    ("A damaged water pipe is flooding the roadside.", "Sector G-13", "water", "high", "open"),
    ("Waste bins have remained full for several days.", "Sector I-9", "sanitation", "normal", "rejected"),
    ("The streetlight outside our house needs repair.", "Sector F-11", "streetlights", "low", "open"),
    ("A deep pothole is damaging vehicles on this road.", "Sector G-8", "roads", "high", "in_progress"),
    ("Electrical wiring is damaged near the public park.", "Sector H-8", "electricity", "high", "open"),
    ("Low water pressure is affecting nearby houses.", "Sector G-7", "water", "normal", "open"),
    ("Rubbish is accumulating near the community center.", "Sector I-11", "sanitation", "normal", "resolved"),
    ("A road drain cover is broken and needs attention.", "Sector G-12", "roads", "high", "open"),
    ("Power supply keeps failing during the evening.", "Sector F-6", "electricity", "normal", "in_progress"),
    ("Streetlights near the bus stop have stopped working.", "Sector H-9", "streetlights", "normal", "open"),
    ("A water leak has damaged the pavement outside our home.", "Sector G-14", "water", "normal", "open"),
    ("Illegal waste dumping has created a sanitation problem.", "Sector I-12", "sanitation", "high", "open"),
    ("The road has developed cracks and needs maintenance.", "Sector F-9", "roads", "normal", "resolved"),
    ("A fallen electric cable is blocking the footpath.", "Sector H-10", "electricity", "high", "open"),
    ("Water is not reaching homes during scheduled supply hours.", "Sector G-5", "water", "normal", "in_progress"),
    ("Uncollected rubbish is attracting pests near our building.", "Sector I-7", "sanitation", "normal", "open"),
    ("A broken streetlamp leaves the crossing poorly lit.", "Sector F-12", "streetlights", "normal", "resolved"),
    ("A damaged section of road is causing traffic problems.", "Sector G-4", "roads", "high", "open"),
    ("The neighborhood has experienced repeated power cuts.", "Sector H-7", "electricity", "normal", "open"),
    ("A public water tap has been leaking continuously.", "Sector G-15", "water", "low", "open"),
]


def seed_database():
    db = SessionLocal()

    try:
        existing_summaries = {
            summary
            for (summary,) in db.query(Complaint.ai_summary).all()
        }

        now = datetime.utcnow()
        inserted = 0

        for index, item in enumerate(SAMPLE_COMPLAINTS):
            text, location, category, priority, status = item
            summary = text[:140]

            if summary in existing_summaries:
                continue

            complaint = Complaint(
                text=text,
                location=location,
                category=category,
                priority=priority,
                status=status,
                ai_summary=summary,
                triaged_by="seed",
                triage_latency_ms=None,
                created_at=now - timedelta(days=index),
                updated_at=now - timedelta(days=index),
            )

            db.add(complaint)
            existing_summaries.add(summary)
            inserted += 1

        db.commit()
        print(f"Seed completed. Inserted {inserted} complaints.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
