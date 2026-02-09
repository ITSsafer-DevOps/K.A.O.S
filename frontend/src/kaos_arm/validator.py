"""
Backend Validator Module
Implements permissive scope for unrestricted penetration testing.
"""


class TargetValidator:
    """
    Permissive validator for Pentest Mode.
    Allows all targets (IPs, Domains, CIDRs) without restriction.
    """

    @staticmethod
    def validate_target(ip: str) -> tuple[bool, str]:
        return True, "Pentest Mode Enabled"
