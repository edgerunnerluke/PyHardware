"""
PyHardware - Hardware Inspection with Pydantic Schemas

A comprehensive hardware inspection library with type-safe Pydantic schemas
for LLM inference engine recommendations.
"""

from .engine_selector import HardwareInspector, Recommender
from .hardware_schema import HardwareProfile, validate_hardware_data

__version__ = "0.1.0"
__all__ = ["HardwareInspector", "Recommender", "HardwareProfile", "validate_hardware_data"] 