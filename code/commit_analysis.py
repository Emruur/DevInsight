from dataclasses import dataclass

@dataclass
class Developer:
    """Class for keeping track of an item in inventory."""
    name: str
    num_of_commits: int=0
    num_of_add: int=0
    num_of_delete:int= 0

@dataclass
class GitDevelpers:
    devs: dict[str, Developer]


