CONTENT_TYPE_CATEGORIES = {
    "image": "images",
    "application/pdf": "documents",
    "application/msword": "documents",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "documents",
    "video": "videos",
    "audio": "audios",
    "text": "text",
}


def get_file_category(content_type: str) -> str:
    if content_type.startswith("image/"):
        return "images"

    if content_type.startswith("video/"):
        return "videos"

    if content_type.startswith("audio/"):
        return "audios"

    if content_type.startswith("text/"):
        return "text"

    return CONTENT_TYPE_CATEGORIES.get(content_type, "others")