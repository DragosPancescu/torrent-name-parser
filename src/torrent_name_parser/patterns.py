def join_patterns_list(patterns: list[str]) -> str:
    return r"(" + "|".join(patterns) + r")"

quality_patterns = [
    r"(?:PPV\.)?[HP]DTV",
    r"(?:HD)?CAM",
    r"B[DR]Rip",
    r"(?:HD-?)?TS",
    r"(?:PPV )?WEB-?DL(?: DVDRip)?",
    r"HDRip",
    r"HDTVRip",
    r"DVDRip",
    r"DVDRIP",
    r"CamRip",
    r"W[EB]BRip",
    r"BluRay",
    r"DvDScr",
    r"hdtv",
    r"telesync",
]

audio_patterns = [
    r"MP3",
    r"DD5\.?1",
    r"DDP5\.?1",
    r"Dual[\- ]Audio",
    r"LiNE",
    r"DTS",
    r"AAC[.-]LC",
    r"AAC(?:\.?2\.0)?",
    r"AAC5.1",
    r"AC3(?:[.-]5\.1)?",
]

PATTERNS = {
    "season": [r"(s?([0-9]{1,2}))[ex]"],
    "episode": [r"([ex]([0-9]{2})(?:[^0-9]|$))"],
    "year": [r"((?<!^)[\[\(]?((?:19[0-9]|20[0-9])[0-9])[\]\)]?)"],
    "month": [r"[\[\(]?(?:19[0-9]|20[01])[0-9][\]\)]?[\.|\s]?(\d{2})[\.|\s]?\d{2}"],
    "day": [r"[\[\(]?(?:19[0-9]|20[01])[0-9][\]\)]?[\.|\s]?\d{2}[\.|\s]?(\d{2})"],
    "resolution": [r"([0-9]{3,4}p)"],
    "quality": [join_patterns_list(quality_patterns)],
    "codec": [r"(xvid|[hx]\.?26[45])"],
    "audio": [join_patterns_list(audio_patterns)],
    "group": [r"(- ?([^-]+(?:-={[^-]+-?$)?))$"],
    "region": [r"R[0-9]"],
    "extended": [r"(EXTENDED(:?.CUT)?)"],
    "hardcoded": [r"HC"],
    "proper": [r"PROPER"],
    "repack": [r"REPACK"],
    "container": [r"(MKV|AVI|MP4)"],
    "widescreen": [r"WS"],
    "website": [r"^(\[ ?([^\]]+?) ?\])", r"^((?:www\.)?[\w-]+\.[\w]{2,4})\s+-\s*"],
    "language": [r"(rus\.eng|ita\.eng)"],
    "sbs": [r"(?:Half-)?SBS"],
    "unrated": [r"UNRATED"],
    "size": [r"(\d+(?:\.\d+)?(?:GB|MB))"],
    "three_d": [r"3D"],
}

TYPES = {
    "season": "integer",
    "episode": "integer",
    "year": "integer",
    "month": "integer",
    "day": "integer",
    "extended": "boolean",
    "hardcoded": "boolean",
    "proper": "boolean",
    "repack": "boolean",
    "widescreen": "boolean",
    "unrated": "boolean",
    "three_d": "boolean",
}
