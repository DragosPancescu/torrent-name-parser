from __future__ import annotations

import re
from dataclasses import asdict

from .patterns import PATTERNS, TYPES
from .models import TorrentMetadata


class TorrentNameParser:
    def __init__(self):
        self.torrent = None
        self.excess_raw = None
        self.group_raw = None
        self.title_start = None
        self.title_end = None
        self.title_raw = None
        self.parts = None
    
    def _escape_regex(self, string):
        return re.sub(r"[\-\[\]{}()*+?.,\\\^$|#\s]", "\\$&", string)
    
    def _reset_state(self):
        """Reset runtime state to prepare for a new parse.
        """
        self.group_raw = ""
        self.title_start = 0
        self.title_end = None
        self.title_raw = None
        self.parts = asdict(TorrentMetadata())
    
    def _ignore_none_values(self):
        """Removes empty values from the parse output
        """
        keys = list(self.parts.keys())
        for key in keys:
            if self.parts[key] is None or self.parts[key] is False:
                self.parts.pop(key)
    
    def _cast_type(self, pattern_key: str, extract: str) -> bool | int | str:
        """Given the pattern key it casts the input to the mapped value in the TYPES dict
    
        Args:
            key (str): Key to search in the TYPES dict
            extract (str): Extracted text to be cast

        Returns:
            bool | int | str: Casted input to the mapped type
        """
        match_type = TYPES.get(pattern_key, "default")
        
        if match_type == "boolean":
            return True
        if match_type == "integer":
            return int(extract)
        return extract
    
    def _update_title_bounds(self, match):
        index = self.torrent["name"].find(match[0])
        if index == 0:
            self.title_start = len(match[0])
        elif self.title_end is None or index < self.title_end:
            self.title_end = index
        
    def _part(self, name, match, raw):
        if len(match) != 0:
            self._update_title_bounds(match)

        if name != "excess":
            # The instructions for adding excess
            if name == "group":
                self.group_raw = raw
            if raw is not None:
                self.excess_raw = self.excess_raw.replace(raw, "")
                
    def _extract_title(self):
        raw_title = self.torrent["name"]
        if self.title_end is not None:
            raw_title = raw_title[self.title_start : self.title_end].split("(")[0]

        clean_title = re.sub(r"^ -", "", raw_title)
        if clean_title.find(" ") == -1 and clean_title.find(".") != -1:
            clean_title = re.sub(r"\.", " ", clean_title)
        clean_title = re.sub("_", " ", clean_title)
        clean_title = re.sub(r"([\[\(_]|- )$", "", clean_title).strip()
        
        return raw_title, clean_title

    def _late(self, name, clean):
        if name == "group":
            self.parts[name] = clean
            self._part(name, [], None)
        elif name == "episodeName":
            clean = re.sub(r"[\._]", " ", clean)
            clean = re.sub(r"_+$", "", clean)
            self.parts[name] = clean.strip()
            self._part(name, [], None)

    def parse(self, name: str, as_dict: bool = False, ignore_none: bool = False) -> TorrentMetadata | dict:
        """Parse a torrent-like filename and return structured metadata.

        Args:
            name (str): The torrent filename to parse.
            as_dict (bool, optional): If the output should be in dictionary form or a TorrentMetadata object
            ignore_none (bool, optional): Flag to ignore (or not) the fields with None values

        Returns:
            TorrentMetadata | dict: Parsed fields and values
        """
        self._reset_state()
        self.torrent = {"name": name}
        self.excess_raw = name
        
        clean_name = re.sub("_", " ", self.torrent["name"])

        for key, pattern in PATTERNS.items():
            if key not in ("season", "episode", "website"):
                pattern = fr"\b{pattern}\b"

            match = re.findall(pattern, clean_name, re.I)
            if len(match) == 0:
                continue

            index = {}
            if isinstance(match[0], tuple):
                match = list(match[0])
                
            if len(match) > 1:
                index["raw"] = 0
                index["clean"] = 1
            else:
                index["raw"] = 0
                index["clean"] = 0
            
            clean = self._cast_type(key, match[index["clean"]])
                    
            if key == "group":
                if re.search(PATTERNS["codec"], clean, re.I) or re.search(PATTERNS["quality"], clean):
                    continue  # Codec and quality.
                if re.match(r"[^ ]+ [^ ]+ .+", clean):
                    key = "episodeName"
            if key == "episode":
                sub_pattern = self._escape_regex(match[index["raw"]])
                self.torrent["map"] = re.sub(
                    sub_pattern, "{episode}", self.torrent["name"]
                )
            
            # Add clean extraction to the output
            self.parts[key] = clean
            self._part(key, match, match[index["raw"]])

        # Start process for title
        raw_title, clean_title = self._extract_title()
        self.parts["title"] = clean_title
        self._part("title", [], raw_title)

        # Start process for end
        clean = re.sub(r"(^[-\. ()]+)|([-\. ]+$)", "", self.excess_raw)
        clean = re.sub(r"[\(\)\/]", " ", clean)
        match = re.split(r"\.\.+| +", clean)
        if len(match) > 0 and isinstance(match[0], tuple):
            match = list(match[0])

        clean = filter(bool, match)
        clean = [item for item in filter(lambda a: a != "-", clean)]
        clean = [item.strip("-") for item in clean]
        if len(clean) != 0:
            group_pattern = clean[-1] + self.group_raw
            if self.torrent["name"].find(group_pattern) == len(
                self.torrent["name"]
            ) - len(group_pattern):
                self._late("group", clean.pop() + self.group_raw)

            if "map" in self.torrent.keys() and len(clean) != 0:
                episode_name_pattern = "{episode}" "" + re.sub(r"_+$", "", clean[0])
                if self.torrent["map"].find(episode_name_pattern) != -1:
                    self._late("episodeName", clean.pop(0))

        if len(clean) != 0:
            if len(clean) == 1:
                clean = clean[0]
            self.parts["excess"] = clean
            self._part("excess", [], self.excess_raw)

        if not as_dict:
            return TorrentMetadata.from_dict(self.parts)
        
        if ignore_none:
            self._ignore_none_values()

        return self.parts
        
