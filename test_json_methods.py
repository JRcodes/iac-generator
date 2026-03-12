#!/usr/bin/env python3
"""
Test script for BlueprintConfig to_json and from_json methods.
Tests successful serialization/deserialization and error handling.
"""

import sys
sys.path.insert(0, 'src')

from pathlib import Path
from iacgen.config import BlueprintConfig, VPCConfig, EKSConfig, ServiceConfig
from iacgen.exceptions import ConfigError

def test_successful_roundtrip():
    """Test successful save and load of configuration."""
    print("=" * 70)
    print("Test 1: Successful Roundtrip")
    print("=" * 70)
    
    # Create a test configuration
    original = BlueprintConfig(
        name="test-infrastructure",
        region="us-west-2",
        vpc=VPCConfig(enabled=True, cidr_block="10.0.0.0/16"),
        eks=EKSConfig(enabled=True, cluster_version="1.29"),
        services=[
            ServiceConfig(name="api", replicas=3, port=8080),
            ServiceConfig(name="worker", replicas=2, port=9090),
        ]
    )
    
    print(f"Created config: {original.name}")
    print(f"  - VPC: {original.vpc.enabled}, CIDR: {original.vpc.cidr_block}")
    print(f"  - EKS: {original.eks.enabled}, Version: {original.eks.cluster_version}")
    print(f"  - Services: {len(original.services)}")
    
    # Save to file
    test_file = Path("test_config.json")
    try:
        original.to_json(test_file)
        print(f"\n✅ Saved to {test_file}")
        
        # Load from file
        loaded = BlueprintConfig.from_json(test_file)
        print(f"✅ Loaded from {test_file}")
        
        # Verify data matches
        assert loaded.name == original.name
        assert loaded.region == original.region
        assert loaded.vpc.enabled == original.vpc.enabled
        assert loaded.vpc.cidr_block == original.vpc.cidr_block
        assert loaded.eks.enabled == original.eks.enabled
        assert loaded.eks.cluster_version == original.eks.cluster_version
        assert len(loaded.services) == len(original.services)
        assert loaded.services[0].name == "api"
        assert loaded.services[1].name == "worker"
        
        print("✅ All data verified correctly!")
        
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()
            print(f"🧹 Cleaned up {test_file}")
    
    print()

def test_missing_file_error():
    """Test error when loading non-existent file."""
    print("=" * 70)
    print("Test 2: Missing File Error")
    print("=" * 70)
    
    try:
        BlueprintConfig.from_json(Path("nonexistent.json"))
        print("❌ Should have raised ConfigError for missing file")
    except ConfigError as e:
        print(f"✅ Caught expected ConfigError:")
        print(f"   Message: {e.message}")
        if e.suggestions:
            print(f"   Suggestions: {e.suggestions}")
    
    print()

def test_invalid_json_error():
    """Test error when loading invalid JSON."""
    print("=" * 70)
    print("Test 3: Invalid JSON Error")
    print("=" * 70)
    
    bad_json_file = Path("bad_config.json")
    try:
        # Create file with invalid JSON
        bad_json_file.write_text('{"name": "test", invalid json}')
        
        BlueprintConfig.from_json(bad_json_file)
        print("❌ Should have raised ConfigError for invalid JSON")
    except ConfigError as e:
        print(f"✅ Caught expected ConfigError:")
        print(f"   Message: {e.message[:100]}...")
        if e.suggestions:
            print(f"   Suggestions: {e.suggestions}")
    finally:
        if bad_json_file.exists():
            bad_json_file.unlink()
    
    print()

def test_validation_error():
    """Test error when loading JSON with invalid data."""
    print("=" * 70)
    print("Test 4: Validation Error")
    print("=" * 70)
    
    invalid_file = Path("invalid_config.json")
    try:
        # Create file with valid JSON but invalid data
        invalid_file.write_text('''{
  "name": "",
  "region": "us-east-1",
  "vpc": {"enabled": true},
  "services": [
    {"name": "bad", "port": 70000}
  ]
}''')
        
        BlueprintConfig.from_json(invalid_file)
        print("❌ Should have raised ConfigError for validation failure")
    except ConfigError as e:
        print(f"✅ Caught expected ConfigError:")
        print(f"   Message (first 200 chars): {e.message[:200]}...")
        if e.suggestions:
            print(f"   Suggestions: {e.suggestions}")
    finally:
        if invalid_file.exists():
            invalid_file.unlink()
    
    print()

def test_minimal_config():
    """Test save/load with minimal configuration."""
    print("=" * 70)
    print("Test 5: Minimal Configuration")
    print("=" * 70)
    
    minimal = BlueprintConfig(name="minimal-infra")
    print(f"Created minimal config: {minimal.name}")
    print(f"  - Region: {minimal.region} (default)")
    print(f"  - VPC enabled: {minimal.vpc.enabled} (default)")
    
    test_file = Path("minimal_config.json")
    try:
        minimal.to_json(test_file)
        print(f"✅ Saved minimal config")
        
        loaded = BlueprintConfig.from_json(test_file)
        print(f"✅ Loaded minimal config")
        
        assert loaded.name == "minimal-infra"
        assert loaded.region == "us-east-1"  # default
        assert loaded.vpc.enabled == False  # default
        print("✅ Minimal config verified!")
        
    finally:
        if test_file.exists():
            test_file.unlink()
    
    print()

if __name__ == "__main__":
    try:
        test_successful_roundtrip()
        test_missing_file_error()
        test_invalid_json_error()
        test_validation_error()
        test_minimal_config()
        
        print("=" * 70)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 70)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
