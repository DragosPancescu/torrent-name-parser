from .parse import TNP as _TNP
from .models import TorrentName

# Singleton instance for convenience
tnp = _TNP()

def parse(name: str, dict_output: bool = False) -> TorrentName | dict:
    """
    Parse a torrent-like filename and return structured metadata.

    Args:
        name (str): The torrent filename to parse.
        dict_output (boolean), default=False: If the output should be in dictionary form or a TorrentName object

    Returns:
        TorrentName | dict: Parsed fields and values
    """
    return tnp.parse(name, dict_output)

# Expose the class too in case users want full control
TNP = _TNP

__all__ = ["parse", "tnp", "TNP"]
