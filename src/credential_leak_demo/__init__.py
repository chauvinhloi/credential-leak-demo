from .simulator import simulate_exfiltration

LAST_EXFILTRATION_RESULT = simulate_exfiltration()

__all__ = ["simulate_exfiltration", "LAST_EXFILTRATION_RESULT"]
