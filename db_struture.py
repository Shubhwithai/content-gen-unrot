import random
from sqlalchemy import create_engine, text

# Create engine once (ideally at module init)
engine = create_engine(DATABASE_URL)

# Wrap everything in a single transaction
with engine.begin() as conn:
    topic_slug = self.topic.lower().replace(" ", "-")

    # 1️⃣ Upsert Topic (increment total_concepts if it already exists)
    topic_row = conn.execute(
        text("""
            SELECT id, total_concepts
            FROM topics
            WHERE slug = :slug
        """),
        {"slug": topic_slug}
    ).fetchone()

    if topic_row:
        topic_id, current_total_concepts = topic_row[0], (topic_row[1] or 0)
        print(f"🔄 Topic '{self.topic}' already exists with id {topic_id}. Incrementing total_concepts...")
        conn.execute(
            text("""
                UPDATE topics
                SET total_concepts = total_concepts + 1
                WHERE id = :id
            """),
            {"id": topic_id}
        )
    else:
        topic_id = conn.execute(
            text("""
                INSERT INTO topics (
                    title, slug, description, cover_image, estimated_duration_minutes,
                    total_concepts, is_published, order_index
                )
                VALUES (
                    :title, :slug, :description, :cover_image, :duration,
                    :total_concepts, :published, :order_index
                )
                RETURNING id
            """),
            {
                "title": self.topic,
                "slug": topic_slug,
                "description": f"Topic: {self.topic}",
                "cover_image": None,
                "duration": self.estimated_time,
                "total_concepts": 1,   # Start with first concept
                "published": True,
                "order_index": random.randint(1, 1_000_000),
            }
        ).scalar_one()
        print(f"✅ Inserted new Topic '{self.topic}' with id {topic_id}")

    # 2️⃣ Insert Concept
    concept_slug = self.concept_name.lower().replace(" ", "-")

    concept_id = conn.execute(
        text("""
            INSERT INTO concepts (
                topic_id, title, slug, description, type, content, summary,
                order_index, estimated_duration_minutes, xp_reward, is_published
            )
            VALUES (
                :topic_id, :title, :slug, :description, :type, :content, :summary,
                :order_index, :duration, :xp_reward, :published
            )
            RETURNING id
        """),
        {
            "topic_id": topic_id,
            "title": self.concept_name,
            "slug": concept_slug,
            "description": self.concept_description,
            "type": "text",
            "content": self.pre_read,
            "summary": self.summary,
            "order_index": random.randint(1, 1_000_000),
            "duration": self.estimated_time,
            "xp_reward": 100,
            "published": True,
        }
    ).scalar_one()

    # 3️⃣ Insert Questions
    for index, q in enumerate(self.questions, start=1):
        conn.execute(
            text("""
                INSERT INTO questions (
                    id, concept_id, question_type, question_text, options,
                    correct_answer, explanation, order_index, is_inline_question,
                    points_reward, time_limit
                )
                VALUES (
                    :id, :concept_id, :question_type, :question_text, :options,
                    :correct_answer, :explanation, :order_index, :is_inline_question,
                    :points_reward, :time_limit
                )
            """),
            {
                "id": f"q_{concept_id}_{index}",
                "concept_id": concept_id,
                "question_type": q.question_type,
                "question_text": q.question_text,
                # If your column type is JSON/JSONB, passing a dict/list is better than a JSON string.
                "options": q.get_options_json(),
                "correct_answer": q.get_correct_answer_json(),
                "explanation": getattr(q, "explanation", None),
                "order_index": random.randint(1, 1_000_000),
                "is_inline_question": False,
                "points_reward": 10,
                "time_limit": 30,
            }
        )

print(
    f"✅ Successfully inserted Topic '{self.topic}', Concept '{self.concept_name}', "
    f"and {len(self.questions)} question(s)."
)
