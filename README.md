# PyHardware - Hardware Inspection with Pydantic Schemas

This project provides comprehensive hardware inspection capabilities with type-safe Pydantic schemas for LLM inference engine recommendations.

## Overview

The project consists of two main components:

1. **Hardware Inspector** (`src/pyhardware/engine_selector.py`) - Detects hardware and recommends optimal LLM inference engines
2. **Pydantic Schemas** (`src/pyhardware/hardware_schema.py`) - Type-safe data models for hardware inspection results

## Features

### Hardware Detection
- **Cross-platform support**: Linux, Windows, macOS
- **Pure Python implementation**: No external command execution
- **Comprehensive detection**:
  - CPU (model, cores, instruction sets)
  - RAM (total and available)
  - Storage type (SSD/HDD)
  - GPUs (NVIDIA, AMD, Intel, Apple)
  - NPUs (Intel, Apple, AMD)
  - Vulkan API support

### Engine Recommendations
- **TensorRT-LLM**: High-end NVIDIA GPUs (Ampere+)
- **vLLM**: NVIDIA GPUs (Turing/Volta+)
- **MLX**: Apple Silicon
- **OpenVINO**: Intel accelerators and AMX CPUs
- **llama.cpp**: AMD GPUs, high-performance CPUs, fallback

### Type-Safe Schemas
- **Complete validation**: All hardware data is validated against Pydantic schemas
- **IDE support**: Full autocomplete and type hints
- **Serialization**: Easy JSON conversion
- **Documentation**: Comprehensive field descriptions

## Getting Started for Development

If you want to work on the codebase or run scripts for development/testing **without installing the package**, follow these steps:

```bash
# Clone the repository
git clone <repository-url>
cd PyHardware

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies only (from pyproject.toml)
pip install --no-build-isolation --editable .[test]
# Or, if you only want core dependencies:
pip install --no-build-isolation --editable .
```

You can now run the code directly from the `src/pyhardware/` directory, for example:

```bash
python src/pyhardware/engine_selector.py
```

> **Note:** The `--editable .` flag is optional for pure dependency installation, but it makes the package importable in-place for development. If you do not want to install the package at all, you can manually install dependencies listed in `pyproject.toml` using pip, or use a tool like [uv](https://github.com/astral-sh/uv) or [hatch](https://hatch.pypa.io/) for dependency management.

## Installation

### From Source (Development)

```bash
# Clone the repository
git clone <repository-url>
cd PyHardware

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dependencies
pip install -e .
```

This will install the `pyhardware` package and all required dependencies as specified in `pyproject.toml`.

## Usage

### Basic Hardware Inspection

```python
from pyhardware import HardwareInspector, Recommender

# Run hardware inspection
inspector = HardwareInspector()
hardware_data = inspector.inspect_all()

# Get engine recommendation
recommender = Recommender()
recommendation = recommender.recommend(hardware_data)

# Add recommendation to data
hardware_data["recommended_engine"] = recommendation

print(f"Recommended engine: {recommendation['name']}")
print(f"Reason: {recommendation['reason']}")
```

### Using Pydantic Schemas

```python
from pyhardware import HardwareProfile, validate_hardware_data, HardwareInspector

# Run inspection and validate with schema
inspector = HardwareInspector()
raw_data = inspector.inspect_all()

# Validate and get typed object
hardware_profile = validate_hardware_data(raw_data)

# Access typed data
print(f"OS: {hardware_profile.os.platform}")
print(f"CPU: {hardware_profile.cpu.brand_raw}")
print(f"RAM: {hardware_profile.ram.total_gb} GB")

# GPU information
if hardware_profile.gpu.detected_vendor == "NVIDIA":
    for gpu in hardware_profile.gpu.nvidia:
        print(f"NVIDIA GPU: {gpu.model} ({gpu.vram_gb} GB)")
        print(f"Compute Capability: {gpu.compute_capability}")

# Serialize to JSON
json_data = hardware_profile.model_dump_json(indent=2)
```

### Schema Validation

```python
from pyhardware import HardwareProfile

# Validate complete data
try:
    profile = HardwareProfile(**hardware_data)
    print("✅ Data is valid")
except ValidationError as e:
    print(f"❌ Validation failed: {e}")

# Create partial profile for testing
from pyhardware.hardware_schema import PartialHardwareProfile

partial_data = {
    "os": {"platform": "Linux", "version": "5.15.0"},
    "cpu": {"brand_raw": "Intel i7-10700K"}
}

partial_profile = PartialHardwareProfile(**partial_data)
```

## Schema Structure

### Main Classes

- **`HardwareProfile`**: Complete hardware profile with all components
- **`OperatingSystem`**: OS platform, version, and architecture
- **`CPU`**: CPU model, cores, and instruction sets
- **`RAM`**: Total and available memory
- **`Storage`**: Primary storage type
- **`GPU`**: Comprehensive GPU information across vendors
- **`NPU`**: Neural Processing Unit information
- **`EngineRecommendation`**: Recommended inference engine

### GPU Vendor-Specific Classes

- **`NVIDIAGPU`**: NVIDIA GPU details (CUDA cores, Tensor cores, compute capability)
- **`AMDGPU`**: AMD GPU details (ROCm compatibility, compute units)
- **`IntelAccelerator`**: Intel GPU/NPU details (execution units, type)
- **`AppleGPU`**: Apple Silicon GPU details (Metal support, unified memory)

## Example Output

```json
{
  "os": {
    "platform": "Darwin",
    "version": "23.0.0",
    "architecture": "arm64"
  },
  "python_version": "3.11.0",
  "cpu": {
    "brand_raw": "Apple M2 Pro",
    "arch": "arm64",
    "physical_cores": 10,
    "logical_cores": 10,
    "instruction_sets": ["neon"]
  },
  "ram": {
    "total_gb": 32.0,
    "available_gb": 24.5
  },
  "storage": {
    "primary_type": "SSD/NVMe"
  },
  "gpu": {
    "detected_vendor": "Apple",
    "vulkan_api_version": null,
    "nvidia": null,
    "amd": null,
    "intel": null,
    "apple": {
      "model": "Apple Silicon GPU",
      "vram_gb": 32.0,
      "gpu_cores": 19,
      "metal_supported": true
    }
  },
  "npus": [
    {
      "vendor": "Apple",
      "model_name": "Apple Neural Engine",
      "npu_cores": 16
    }
  ],
  "recommended_engine": {
    "name": "MLX",
    "reason": "Natively designed for Apple Silicon..."
  }
}
```

## Running Examples

```bash
# Run the main hardware inspector (for development/testing only)
python src/pyhardware/engine_selector.py
```

## Dependencies

All dependencies are specified in `pyproject.toml` and will be installed automatically when you install the package with pip.

- **py-cpuinfo**: CPU information
- **psutil**: System and process utilities
- **nvidia-ml-py**: NVIDIA GPU monitoring
- **amdsmi**: AMD GPU monitoring
- **openvino**: Intel accelerator support
- **mlx**: Apple Silicon support
- **pyobjc**: macOS system integration
- **vulkan**: Vulkan API support
- **pydantic**: Data validation and serialization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here] 