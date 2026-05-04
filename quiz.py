
import json
import random
import time


def load_questions(filename="questions.json"):
    """Load quiz questions from a JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: '{filename}' not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error: '{filename}' is not valid JSON ({e}).")
        return []


def choose_category(questions):
    """Let the user pick a category (or all). Returns filtered list."""
    categories = sorted({q["category"] for q in questions})
    print("\nAvailable categories:")
    print("0. All categories")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    while True:
        try:
            choice = int(input("\nChoose a category (number): ").strip())
            if choice == 0:
                return questions
            if 1 <= choice <= len(categories):
                selected = categories[choice - 1]
                return [q for q in questions if q["category"] == selected]
            raise ValueError
        except ValueError:
            print("⚠️  Invalid choice. Please enter a valid number.")


def ask_question(q):
    """Display one question and return True if the user answers correctly."""
    print("\n" + q["question"])
    for key, value in q["choices"].items():
        print(f"  {key}. {value}")

    while True:
        try:
            answer = input("Your answer (A/B/C/D): ").strip().upper()
            if answer not in q["choices"]:
                raise ValueError("Invalid choice. Please enter A, B, C, or D.")
            return answer == q["answer"]
        except ValueError as e:
            print(f"⚠️  {e}")


def run_quiz(questions):
    """Run the quiz: shuffle, time each question, score, give feedback."""
    if not questions:
        print("No questions to ask. Exiting.")
        return

    random.shuffle(questions)
    score = 0
    total = len(questions)
    time_limit = 15  # seconds per question

    print(f"\n🎯 Starting quiz! {total} questions, {time_limit}s each.\n")

    for idx, q in enumerate(questions, 1):
        print(f"--- Question {idx}/{total} ---")
        start = time.time()
        correct = ask_question(q)
        elapsed = time.time() - start

        if elapsed > time_limit:
            print(f"⏰ Time's up! ({elapsed:.1f}s) No points awarded.")
        elif correct:
            print(f"✅ Correct! ({elapsed:.1f}s)")
            score += 1
        else:
            print(f"❌ Wrong! Correct answer was: {q['answer']}. {q['choices'][q['answer']]}")

    print("\n--- Quiz Finished ---")
    print(f"Your score: {score}/{total}")

    ratio = score / total
    if ratio == 1:
        print("🎉 Excellent!")
    elif ratio >= 0.5:
        print("👍 Good job!")
    else:
        print("💡 Try Again!")


if __name__ == "__main__":
    questions = load_questions()
    if questions:
        filtered = choose_category(questions)
        run_quiz(filtered)
