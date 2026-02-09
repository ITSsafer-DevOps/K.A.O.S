"""
K.A.O.S. Unit Tests - Analyzer Module
Tests for command analysis and risk assessment engine
"""

import unittest
from backend.src.brain.app.core.analyzer import (
    CommandAnalyzer,
    RiskLevel,
    ToolType,
)


class TestCommandAnalyzer(unittest.TestCase):
    """Test suite for CommandAnalyzer class"""

    def setUp(self):
        """Initialize test fixtures"""
        self.analyzer = CommandAnalyzer()

    def test_destructive_pattern_detection(self):
        """Test detection of destructive patterns"""
        test_cases = [
            ("rm -rf /", True),
            ("mkfs.ext4 /dev/sda1", True),
            ("dd if=/dev/zero of=/dev/sda", True),
            ("chmod 777 /", True),
            ("nmap -sV localhost", False),
            ("echo hello", False),
        ]

        for command, expected in test_cases:
            result = self.analyzer.check_destructive(command)
            self.assertEqual(
                result,
                expected,
                f"Destructive check failed for: {command}",
            )

    def test_risk_level_classification(self):
        """Test risk level assessment"""
        test_cases = [
            ("echo hello", RiskLevel.SAFE),
            ("nmap -sV localhost", RiskLevel.MEDIUM),
            ("sqlmap -u http://target.com", RiskLevel.HIGH),
            ("rm -rf /", RiskLevel.CRITICAL),
        ]

        for command, expected_level in test_cases:
            result = self.analyzer.rate_risk(command)
            self.assertEqual(
                result,
                expected_level,
                f"Risk classification failed for: {command}",
            )

    def test_tool_type_mapping(self):
        """Test tool type identification"""
        test_cases = [
            ("scan the network", ToolType.NMAP),
            ("map the targets", ToolType.NMAP),
            ("inject sql payload", ToolType.SQLMAP),
            ("hello there", ToolType.CONVERSATION),
            ("unknown command", ToolType.UNKNOWN),
        ]

        for command, expected_type in test_cases:
            result = self.analyzer.identify_tool(command)
            self.assertEqual(
                result,
                expected_type,
                f"Tool mapping failed for: {command}",
            )


if __name__ == "__main__":
    unittest.main()
