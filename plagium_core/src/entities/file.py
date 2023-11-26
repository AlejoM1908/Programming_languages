from dataclasses import dataclass
from antlr4 import ParserRuleContext

@dataclass
class File:
    name: str
    tree: ParserRuleContext
    hash: str

    def __eq__(self, other):
        if not isinstance(other, File):
            return False
        
        return self.hash == other.hash
    
    def __hash__(self):
        return self.hash