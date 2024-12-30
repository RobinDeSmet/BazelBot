import hashlib


def generate_content_hash(content: str) -> str:
    """Generate the content hash for a bazel

    Args:
        content (str): Content to be hashed

    Returns:
        str: The hashed content
    """
    # Generate content hash
    return hashlib.sha256(content.encode("utf-8")).hexdigest()
