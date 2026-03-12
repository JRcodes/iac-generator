# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-30

### Added

- Initial release of the **iacgen** CLI tool for generating Terraform infrastructure blueprints.
- VPC module template generation, including:
  - Public and private subnets
  - NAT gateway configuration
  - Availability Zone handling
- EKS cluster module templates with:
  - IAM roles and node groups
  - Support for using an existing VPC (via flags and config)
- Service module templates for Kubernetes workloads:
  - Namespace management
  - Deployment and Service manifests
  - Optional Horizontal Pod Autoscaler (HPA) support
- ALB module templates covering:
  - Security groups and listeners
  - Target groups
  - Path-based routing to services
- Pydantic-based configuration models:
  - `BlueprintConfig`, `VPCConfig`, `EKSConfig`, `ALBConfig`, `ServiceConfig`
  - Field-level validation (CIDR, ports, replica counts, node sizing, etc.)
- Blueprint persistence:
  - `blueprint.json` generation from CLI arguments
  - Loading and recreating infrastructure via `iacgen recreate`
- Dependency validation engine:
  - EKS requires VPC
  - Services require EKS
  - ALB requires at least one service
  - No empty blueprints (at least one module or service must be enabled)
- Jinja2-based rendering engine:
  - Template context builder for Terraform modules
  - Custom Terraform-friendly filters for lists and maps
  - Filesystem generator for `main.tf`, `variables.tf`, `outputs.tf`, and module files
- Rich console experience with:
  - Colored output and configuration summary panels
  - Clear validation and error messages with suggestions
  - `--debug` flag for full tracebacks
- CLI commands:
  - `iacgen create` for generating new blueprints from flags and/or presets
  - `iacgen recreate` for regenerating from an existing `blueprint.json`
  - `iacgen version` for printing the installed version
- YAML preset system:
  - Built-in presets: `microservice`, `simple-vpc`, and `full-stack`
  - `--preset` flag with CLI overrides on top of YAML configuration
- Comprehensive test suite:
  - Unit tests for configuration models and validation rules
  - Tests for the preset loader and preset/CLI integration
  - Rendering tests to ensure Terraform templates are generated as expected

[1.0.0]: https://github.com/JRcodes/iac-generator/releases/tag/v1.0.0
