from app.db.session import SessionLocal
from app.models.training_question import TrainingQuestion
from app.services.embedding_service import embed


def seed_training_questions():
    db = SessionLocal()

    data = [
        TrainingQuestion(
            question="Do you have a room on July 5 for 2 people?", intent="check_availability", embedding=embed("Do you have a room on July 5 for 2 people?")),
        TrainingQuestion(question="Is there a double room available next weekend?", intent="check_availability", embedding=embed("Is there a double room available next weekend?")),
        TrainingQuestion(question="Any availability for 2 guests on July 5th?", intent="check_availability", embedding=embed("Any availability for 2 guests on July 5th?")),
        TrainingQuestion(question="Can I book a room for two people?", intent="check_availability", embedding=embed("Can I book a room for two people?")),
        TrainingQuestion(question="Do you have free rooms next week?", intent="check_availability", embedding=embed("Do you have free rooms next week?")),
        TrainingQuestion(question="What is the price per night?", intent="ask_price", embedding=embed("What is the price per night?")),
        TrainingQuestion(question="How much does a room cost?", intent="ask_price", embedding=embed("How much does a room cost?")),
        TrainingQuestion(question="Price for one night stay?", intent="ask_price", embedding=embed("Price for one night stay?")),
        TrainingQuestion(question="What do you charge per room?", intent="ask_price", embedding=embed("What do you charge per room?")),
        TrainingQuestion(question="Do you have WiFi?", intent="ask_wifi", embedding=embed("Do you have WiFi?")),
        TrainingQuestion(question="Is internet included?", intent="ask_wifi", embedding=embed("Is internet included?")),
        TrainingQuestion(question="How good is the WiFi?", intent="ask_wifi", embedding=embed("How good is the WiFi?")),
    ]

    db.add_all(data)
    db.commit()
    db.close()


if __name__ == "__main__":
    seed_training_questions()
    print("Seed completed")

# python -m app.seed.seed_training_questions