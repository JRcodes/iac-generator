#!/usr/bin/env python3
"""
Integration test for CLI with BlueprintConfig.
Tests the from_cli_args classmethod and CLI integration.
"""

import sys
sys.path.insert(0, 'src')

from pathlib import Path
from iacgen.config import BlueprintConfig

def test_from_cli_args_minimal():
    """Test from_cli_args with minimal arguments."""
    print("=" * 70)
    print("Test 1: Minimal CLI Args")
    print("=" * 70)
    
    config = BlueprintConfig.from_cli_args(
        name="test-infra"
    )
    
    print(f"✅ Created config: {config.name}")
    print(f"   Region: {config.region} (default)")
    print(f"   VPC enabled: {config.vpc.enabled}")
    print(f"   EKS enabled: {config.eks.enabled}")
    print(f"   ALB enabled: {config.alb.enabled}")
    print(f"   Services: {len(config.services)}")
    
    assert config.name == "test-infra"
    assert config.region == "us-west-2"  # default
    assert config.vpc.enabled == False
    assert config.eks.enabled == False
    assert config.alb.enabled == False
    assert len(config.services) == 0
    
    print()

def test_from_cli_args_with_modules():
    """Test from_cli_args with module flags enabled."""
    print("=" * 70)
    print("Test 2: CLI Args with Modules")
    print("=" * 70)
    
    config = BlueprintConfig.from_cli_args(
        name="vpc-eks-infra",
        region="us-east-1",
        vpc=True,
        eks=True
    )
    
    print(f"✅ Created config: {config.name}")
    print(f"   Region: {config.region}")
    print(f"   VPC enabled: {config.vpc.enabled}")
    print(f"   VPC CIDR: {config.vpc.cidr_block} (default)")
    print(f"   EKS enabled: {config.eks.enabled}")
    print(f"   EKS version: {config.eks.cluster_version} (default)")
    
    assert config.name == "vpc-eks-infra"
    assert config.region == "us-east-1"
    assert config.vpc.enabled == True
    assert config.vpc.cidr_block == "10.0.0.0/16"  # default
    assert config.eks.enabled == True
    assert config.eks.cluster_version == "1.28"  # default
    
    print()

def test_from_cli_args_with_services():
    """Test from_cli_args with service list."""
    print("=" * 70)
    print("Test 3: CLI Args with Services")
    print("=" * 70)
    
    config = BlueprintConfig.from_cli_args(
        name="service-infra",
        vpc=True,
        eks=True,
        alb=True,
        services=["api", "worker", "scheduler"]
    )
    
    print(f"✅ Created config: {config.name}")
    print(f"   VPC: {config.vpc.enabled}")
    print(f"   EKS: {config.eks.enabled}")
    print(f"   ALB: {config.alb.enabled}")
    print(f"   Services ({len(config.services)}):")
    for svc in config.services:
        print(f"     - {svc.name}: replicas={svc.replicas}, port={svc.port}")
    
    assert len(config.services) == 3
    assert config.services[0].name == "api"
    assert config.services[1].name == "worker"
    assert config.services[2].name == "scheduler"
    
    # Verify default service values
    assert config.services[0].replicas == 2  # default
    assert config.services[0].port == 8080  # default
    assert config.services[0].cpu == "256m"  # default
    
    print()

def test_roundtrip_with_cli_args():
    """Test save and load with from_cli_args."""
    print("=" * 70)
    print("Test 4: Roundtrip with CLI Args")
    print("=" * 70)
    
    # Create config from CLI args
    original = BlueprintConfig.from_cli_args(
        name="roundtrip-test",
        region="eu-west-1",
        vpc=True,
        eks=True,
        services=["frontend", "backend"]
    )
    
    print(f"Created config from CLI args: {original.name}")
    
    # Save to file
    test_file = Path("test_cli_config.json")
    try:
        original.to_json(test_file)
        print(f"✅ Saved to {test_file}")
        
        # Load from file
        loaded = BlueprintConfig.from_json(test_file)
        print(f"✅ Loaded from {test_file}")
        
        # Verify
        assert loaded.name == original.name
        assert loaded.region == original.region
        assert loaded.vpc.enabled == original.vpc.enabled
        assert loaded.eks.enabled == original.eks.enabled
        assert len(loaded.services) == len(original.services)
        assert loaded.services[0].name == "frontend"
        assert loaded.services[1].name == "backend"
        
        print("✅ Roundtrip successful!")
        
    finally:
        if test_file.exists():
            test_file.unlink()
            print(f"🧹 Cleaned up {test_file}")
    
    print()

def test_cli_args_with_defaults():
    """Test that defaults match CLI defaults."""
    print("=" * 70)
    print("Test 5: CLI Default Values")
    print("=" * 70)
    
    config = BlueprintConfig.from_cli_args()
    
    print(f"Name: {config.name}")
    print(f"Region: {config.region}")
    
    # These should match the defaults in cli.py
    assert config.name == "infrastructure"
    assert config.region == "us-west-2"
    
    print("✅ Default values match CLI!")
    print()

def test_service_name_extraction():
    """Test that service names are properly extracted."""
    print("=" * 70)
    print("Test 6: Service Name Extraction")
    print("=" * 70)
    
    service_names = ["api", "worker", "scheduler", "notifier"]
    config = BlueprintConfig.from_cli_args(
        name="multi-service",
        services=service_names
    )
    
    extracted_names = [svc.name for svc in config.services]
    print(f"Input: {service_names}")
    print(f"Extracted: {extracted_names}")
    
    assert extracted_names == service_names
    print("✅ Service names extracted correctly!")
    print()

if __name__ == "__main__":
    try:
        test_from_cli_args_minimal()
        test_from_cli_args_with_modules()
        test_from_cli_args_with_services()
        test_roundtrip_with_cli_args()
        test_cli_args_with_defaults()
        test_service_name_extraction()
        
        print("=" * 70)
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("=" * 70)
        print("\n📋 Summary:")
        print("  ✅ from_cli_args() works with all argument combinations")
        print("  ✅ Default values match CLI specification")
        print("  ✅ Services are properly created from name list")
        print("  ✅ Roundtrip save/load works correctly")
        print("  ✅ Module flags enable modules as expected")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
