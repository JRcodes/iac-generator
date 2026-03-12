#!/usr/bin/env python3
"""
Test script for configuration models.
Tests ModuleType, ServiceConfig, VPCConfig, EKSConfig, and ALBConfig.
"""

import sys
sys.path.insert(0, 'src')

from iacgen.config import ModuleType, ServiceConfig, VPCConfig, EKSConfig, ALBConfig, BlueprintConfig

def test_module_type():
    """Test ModuleType enum."""
    print("=" * 60)
    print("Testing ModuleType Enum")
    print("=" * 60)
    for mt in ModuleType:
        print(f"  {mt.name} = {mt.value}")
    print("✅ ModuleType enum works!\n")

def test_service_config():
    """Test ServiceConfig with valid and invalid data."""
    print("=" * 60)
    print("Testing ServiceConfig")
    print("=" * 60)
    
    # Valid default
    service = ServiceConfig(name="api")
    print(f"✅ Default config: {service.name}, replicas={service.replicas}, port={service.port}")
    
    # Valid custom
    custom = ServiceConfig(name="worker", replicas=3, port=9090, cpu="500m", memory="1Gi")
    print(f"✅ Custom config: {custom.name}, replicas={custom.replicas}, cpu={custom.cpu}")
    
    # Test validation errors
    print("\nTesting validation errors:")
    try:
        ServiceConfig(name="bad", replicas=0)
        print("❌ Should have failed: replicas=0")
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")
    
    try:
        ServiceConfig(name="bad", port=70000)
        print("❌ Should have failed: port=70000")
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")
    
    try:
        ServiceConfig(name="bad", cpu="invalid")
        print("❌ Should have failed: cpu='invalid'")
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")
    
    print()

def test_vpc_config():
    """Test VPCConfig with valid and invalid data."""
    print("=" * 60)
    print("Testing VPCConfig")
    print("=" * 60)
    
    # Valid default
    vpc = VPCConfig()
    print(f"✅ Default config: enabled={vpc.enabled}, cidr={vpc.cidr_block}, azs={vpc.availability_zones}")
    
    # Valid custom
    custom = VPCConfig(enabled=True, cidr_block="192.168.0.0/20", availability_zones=2)
    print(f"✅ Custom config: cidr={custom.cidr_block}, azs={custom.availability_zones}")
    
    # Test validation errors
    print("\nTesting validation errors:")
    try:
        VPCConfig(cidr_block="invalid")
        print("❌ Should have failed: cidr='invalid'")
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")
    
    try:
        VPCConfig(cidr_block="10.0.0.0/33")
        print("❌ Should have failed: cidr with prefix > 32")
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")
    
    try:
        VPCConfig(availability_zones=0)
        print("❌ Should have failed: azs=0")
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")
    
    print()

def test_eks_config():
    """Test EKSConfig with valid and invalid data."""
    print("=" * 60)
    print("Testing EKSConfig")
    print("=" * 60)
    
    # Valid default
    eks = EKSConfig()
    print(f"✅ Default config: enabled={eks.enabled}, version={eks.cluster_version}")
    print(f"   Nodes: min={eks.node_min_size}, desired={eks.node_desired_size}, max={eks.node_max_size}")
    
    # Valid custom
    custom = EKSConfig(enabled=True, node_min_size=2, node_desired_size=3, node_max_size=5)
    print(f"✅ Custom config: min={custom.node_min_size}, desired={custom.node_desired_size}, max={custom.node_max_size}")
    
    # Test validation errors
    print("\nTesting validation errors:")
    try:
        EKSConfig(node_min_size=0)
        print("❌ Should have failed: min_size=0")
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")
    
    try:
        EKSConfig(node_min_size=5, node_max_size=3)
        print("❌ Should have failed: max < min")
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")
    
    try:
        EKSConfig(node_min_size=2, node_desired_size=5, node_max_size=4)
        print("❌ Should have failed: desired > max")
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")
    
    print()

def test_alb_config():
    """Test ALBConfig."""
    print("=" * 60)
    print("Testing ALBConfig")
    print("=" * 60)
    
    # Valid default
    alb = ALBConfig()
    print(f"✅ Default config: enabled={alb.enabled}, internal={alb.internal}, https={alb.enable_https}")
    
    # Valid custom
    custom = ALBConfig(enabled=True, internal=True, enable_https=False)
    print(f"✅ Custom config: enabled={custom.enabled}, internal={custom.internal}, https={custom.enable_https}")
    
    print()

def test_blueprint_config():
    """Test BlueprintConfig with minimal and full configurations."""
    print("=" * 60)
    print("Testing BlueprintConfig")
    print("=" * 60)
    
    # Minimal config - only name required
    minimal = BlueprintConfig(name="test-infra")
    print(f"✅ Minimal config:")
    print(f"   name: {minimal.name}")
    print(f"   region: {minimal.region}")
    print(f"   vpc.enabled: {minimal.vpc.enabled}")
    print(f"   eks.enabled: {minimal.eks.enabled}")
    print(f"   alb.enabled: {minimal.alb.enabled}")
    print(f"   services: {len(minimal.services)} services")
    
    # Full custom config
    custom = BlueprintConfig(
        name="production-infra",
        region="us-west-2",
        vpc=VPCConfig(enabled=True, cidr_block="10.0.0.0/16"),
        eks=EKSConfig(enabled=True, cluster_version="1.29", node_desired_size=3),
        alb=ALBConfig(enabled=True, enable_https=True),
        services=[
            ServiceConfig(name="api", replicas=3, port=8080),
            ServiceConfig(name="worker", replicas=2, port=9090),
        ]
    )
    print(f"\n✅ Full config:")
    print(f"   name: {custom.name}")
    print(f"   region: {custom.region}")
    print(f"   vpc: enabled={custom.vpc.enabled}, cidr={custom.vpc.cidr_block}")
    print(f"   eks: enabled={custom.eks.enabled}, version={custom.eks.cluster_version}")
    print(f"   alb: enabled={custom.alb.enabled}")
    print(f"   services: {len(custom.services)} services")
    for svc in custom.services:
        print(f"     - {svc.name}: replicas={svc.replicas}, port={svc.port}")
    
    # Test JSON serialization
    print(f"\n✅ JSON serialization:")
    json_data = custom.model_dump_json(indent=2)
    print(f"   Serialized to {len(json_data)} bytes")
    
    # Test deserialization
    from_json = BlueprintConfig.model_validate_json(json_data)
    print(f"   Deserialized: name={from_json.name}, {len(from_json.services)} services")
    
    # Test validation errors
    print("\nTesting validation errors:")
    try:
        BlueprintConfig(name="")  # Empty name
        print("❌ Should have failed: empty name")
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")
    
    try:
        BlueprintConfig(name="a" * 65)  # Name too long
        print("❌ Should have failed: name too long")
    except ValueError as e:
        print(f"✅ Caught expected error: {e}")
    
    print()

if __name__ == "__main__":
    try:
        test_module_type()
        test_service_config()
        test_vpc_config()
        test_eks_config()
        test_alb_config()
        test_blueprint_config()
        
        print("=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
