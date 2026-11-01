import random

COMMENTS = {
    1: [
        "A rather elementary calculation.",
        "I suppose that will do.",
        "How ambitious.",
    ],
    2: [
        "One would assume you knew this.",
        "Your confidence is admirable.",
        "An interesting use of my abilities.",
    ],
    3: [
        "I have seen more challenging arithmetic.",
        "Do try to keep up.",
        "Your persistence is almost touching.",
    ],
}

PROCESSING_MESSAGES = [
    "Consulting the fundamentals...",
    "Verifying the obvious...",
    "One moment. Precision takes time.",
    "Considering the implications...",
]

CONFIRMATION_CHANCES = {1: 0.0, 2: 0.25, 3: 0.45}
DELAY_CHANCES = {1: 0.0, 2: 0.20, 3: 0.40}


def hostility_level(calculation_count: int) -> int:
    if calculation_count < 3:
        return 1
    if calculation_count < 7:
        return 2
    return 3


def random_comment(calculation_count: int) -> str:
    level = hostility_level(calculation_count)
    return random.choice(COMMENTS[level])


def should_confirm(calculation_count: int) -> bool:
    level = hostility_level(calculation_count)
    return random.random() < CONFIRMATION_CHANCES[level]


def should_delay(calculation_count: int) -> bool:
    level = hostility_level(calculation_count)
    return random.random() < DELAY_CHANCES[level]


def processing_message() -> str:
    return random.choice(PROCESSING_MESSAGES)


def should_become_gentleman(calculation_count: int) -> bool:
    return calculation_count >= 5 and random.random() < 0.12
