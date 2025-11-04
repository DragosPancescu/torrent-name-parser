from dataclasses import dataclass, fields


@dataclass
class TorrentName:
    """Class for encapsulating torrent name info"""

    season: int = 0
    episode: int = 0
    year: int = 0

    resolution: str = ""
    quality: str = ""
    codec: str = ""
    audio: str = ""
    container: str = ""

    title: str = ""
    region: str = ""
    excess: str = ""
    website: str = ""
    language: str = ""
    sbs: str = ""

    size: str = ""
    group: str = ""

    extended: bool = False
    hardcoded: bool = False
    proper: bool = False
    repack: bool = False
    widescreen: bool = False
    three_d: bool = False
    unrated: bool = False

    @classmethod
    def from_dict(cls, data: dict):
        obj_args = {}
        for f in fields(cls):
            name = f.name
            if name in data:
                obj_args[name] = data[name]
            else:
                obj_args[name] = getattr(cls, name)

        return cls(**obj_args)
