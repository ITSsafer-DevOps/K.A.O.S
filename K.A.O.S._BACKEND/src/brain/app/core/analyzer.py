"""
K.A.O.S. Hybrid Engine - Command Analyzer
Implements Regex Heuristics and Risk Assessment.
"""
import re
from enum import Enum
from typing import Dict, Any

class RiskLevel(Enum):
    SAFE = "SAFE"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ToolType(Enum):
    NMAP = "nmap"
    SQLMAP = "sqlmap"
    METASPLOIT = "metasploit"
    CONVERSATION = "conversation"
    SYSTEM = "system"
    UNKNOWN = "unknown"

class CommandAnalyzer:
    
    DESTRUCTIVE_PATTERNS = [
        r"rm\s+-rf",
        r"mkfs",
        r":\(\)\{\s*:\|:\s*&\s*\};:",  # Fork bomb
        r"dd\s+if=/dev/zero",
        r"chmod\s+777\s+/"
    ]

    INTENT_MAP = {
        "scan": ToolType.NMAP,
        "map": ToolType.NMAP,
        "inject": ToolType.SQLMAP,
        "hello": ToolType.CONVERSATION,
        "hi": ToolType.CONVERSATION,
        "ahoj": ToolType.CONVERSATION
    }

    @staticmethod
    def check_destructive(command: str) -> bool:
        for pattern in CommandAnalyzer.DESTRUCTIVE_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def analyze(command: str) -> Dict[str, Any]:
        command_lower = command.lower()
        
        # 1. Safety Check
        if CommandAnalyzer.check_destructive(command):
            return {
                "risk": RiskLevel.CRITICAL.value,
                "tool_type": ToolType.SYSTEM.value,
                "reasoning": "Destructive command pattern detected.",
                "allowed": False
            }

        # 2. Fast-Path Intent Detection
        tool_type = ToolType.UNKNOWN
        for keyword, tool in CommandAnalyzer.INTENT_MAP.items():
            if keyword in command_lower:
                tool_type = tool
                break

        # 3. Construct Analysis
        return {
            "risk": RiskLevel.SAFE.value if tool_type != ToolType.UNKNOWN else RiskLevel.MEDIUM.value,
            "tool_type": tool_type.value,
            "reasoning": f"Heuristic analysis identified {tool_type.value} intent.",
            "allowed": True
        }
