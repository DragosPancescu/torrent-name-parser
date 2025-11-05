from dataclasses import dataclass, field, fields, MISSING


@dataclass
class TorrentMetadata:
    """Class for encapsulating torrent name info"""

    season: int = None
    episode: int = None
    year: int = None

    resolution: str = None
    quality: str = None
    codec: str = None
    audio: str = None
    container: str = None

    title: str = None
    region: str = None
    website: str = None
    language: str = None
    sbs: str = None

    size: str = None
    group: str = None

    extended: bool = False
    hardcoded: bool = False
    proper: bool = False
    repack: bool = False
    widescreen: bool = False
    three_d: bool = False
    unrated: bool = False
    
    excess: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        obj_args = {}
        for f in fields(cls):
            name = f.name
            if name in data: 
                obj_args[name] = data[name] 
            elif f.default is not MISSING: 
                obj_args[name] = f.default 
            elif f.default_factory is not MISSING: 
                obj_args[name] = f.default_factory() 
            else: obj_args[name] = None # fallback for safety
        return cls(**obj_args)
