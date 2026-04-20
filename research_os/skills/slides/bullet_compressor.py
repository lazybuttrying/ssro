def compress_bullets(sentences: list[str], max_items: int = 3) -> list[str]:
    bullets = []
    for sentence in sentences[:max_items]:
        text = str(sentence).strip()
        if len(text) > 100:
            text = text[:97] + "..."
        bullets.append(text)
    return bullets
