from __future__ import annotations

from .parse import TNP as _TNP
from .models import TorrentMetadata

# Singleton instance for convenience
tnp = _TNP()

# Simple parse usage on demand
def parse(name: str, as_dict: bool = False, ignore_none: bool = False) -> TorrentMetadata | dict:
    """Parse a torrent-like filename and return structured metadata.

    Args:
        name (str): The torrent filename to parse.
        as_dict (bool, optional): If the output should be in dictionary form or a TorrentMetadata object
        ignore_none (bool, optional): Flag to ignore (or not) the fields with None values

    Returns:
        TorrentMetadata | dict: Parsed fields and values
    """
    
    return tnp.parse(name, as_dict, ignore_none)

# Expose the class too in case users want full control
TNP = _TNP

__all__ = ["parse", "tnp", "TNP"]