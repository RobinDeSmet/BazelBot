class GenerationFailedError(Exception):
    """Error thrown when generation with LLM fails."""


class QuotaExceededError(Exception):
    """Error thrown when gemini quota is exceeded."""


class BazelCouldNotBeGeneratedError(Exception):
    """Error thrown when bazel could be generated."""


class BazelCouldCouldNotBeGeneratedError(Exception):
    """Error thrown when bazel context could be generated."""


class ImageCouldNotBeGeneratedError(Exception):
    """Error thrown when image could be generated."""
