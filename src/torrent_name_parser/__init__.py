from .parse import TNP as _TNP

# Singleton instance for convenience
tnp = _TNP()

def parse(name: str) -> dict:
    """
    Parse a torrent-like filename and return structured metadata.

    Args:
        name (str): The torrent filename to parse.

    Returns:
        dict: Parsed fields like title, season, episode, quality.
    """
    return tnp.parse(name)

# Expose the class too in case users want full control
TNP = _TNP

__all__ = ["parse", "tnp", "TNP"]
