# Metadata Framework Decoupling

## Problem Statement

The current metadata system creates unnecessary coupling between documentation generation and the car interface implementation. This coupling introduces complexity, fragility, and maintenance overhead without providing corresponding benefits.

## Core Issues Identified

### 1. Unnecessary Runtime Complexity for Static Data

**Problem:** The current system uses runtime flag checking for static platform properties.

```python
# Current approach - checking static flags at runtime
def init_make(self, CP: structs.CarParams):
    if CP.flags & HyundaiFlags.CANFD:  # This flag is ALWAYS static
        self.footnotes.insert(0, Footnote.CANFD)
```

**Issue:** The `CANFD` flag is statically determined by platform configuration - there's no runtime variation or detection needed.

### 2. Coupling Documentation to Car Interface

**Problem:** Documentation generation requires importing car interface modules.

```python
# Creates unnecessary dependencies
from opendbc.car.hyundai.values import HyundaiFlags
from opendbc.car import structs
```

**Impact:**
- Documentation tests require full car interface setup
- Changes to car interface can break documentation
- Circular dependency risk
- Increased build complexity

### 3. Confusion Between Functional and Documentation Concerns

**Problem:** Mixing car control logic with installation documentation.

- **Functional flags:** Affect CAN message formats, safety parameters, actual car behavior
- **Documentation flags:** Affect installation instructions, harness selection, user warnings

These have different requirements and shouldn't share infrastructure.

## Analysis: Functional vs Documentation Usage

### Functional Requirements (Keep Dynamic)
```python
# MUST be runtime - affects actual car behavior
if candidate in HONDA_BOSCH:
    ret.safetyConfigs = [get_safety_config(SafetyModel.hondaBosch)]
    # Different CAN protocols, safety parameters, etc.
```

### Documentation Requirements (Should be Static)
```python
# SHOULD be static - just installation instructions
harness = CarHarness.bosch_c if CP.flags & HondaFlags.BOSCH_CANFD else CarHarness.bosch_a
```

## Decision: Move to Static Documentation

### Rationale

1. **Documentation generation has no car connected** - all information is static
2. **Platform capabilities are known at build time** - no runtime detection needed
3. **Harness/parts selection is static per platform** - no variation within platform
4. **Footnotes are static per platform type** - CAN FD cars always need CAN FD footnote

### Implementation Strategy

**Replace dynamic logic:**
```python
# OLD: Runtime flag checking
def init_make(self, CP: structs.CarParams):
    if CP.flags & HyundaiFlags.CANFD:
        self.footnotes.insert(0, Footnote.CANFD)
```

**With static data:**
```python
# NEW: Direct static declaration
METADATA = {
    "HYUNDAI_IONIQ_5": [
        HyundaiCarDocs(
            name="Hyundai Ioniq 5",
            footnotes=[Footnote.CANFD],  # Static, obvious, simple
            car_parts=CarParts.common([CarHarness.hyundai_q])
        ),
    ],
}
```

## Benefits of Static Approach

### Technical Benefits
- ✅ **Zero coupling** to car interface
- ✅ **Minimal dependencies** - just docs framework
- ✅ **Simple testing** - pure data structure tests
- ✅ **Fast build** - no runtime car interface setup
- ✅ **Clear intent** - documentation is obviously documentation

### Maintenance Benefits  
- ✅ **Explicit is better than implicit** - footnotes visible in definition
- ✅ **Easier debugging** - no hidden runtime logic
- ✅ **Simpler refactoring** - documentation changes don't affect car interface
- ✅ **Reduced cognitive load** - less complexity to understand

### Architectural Benefits
- ✅ **Proper separation of concerns** - docs vs functionality
- ✅ **Reduced fragility** - car interface changes don't break docs
- ✅ **Better testability** - docs can be tested independently
- ✅ **Clearer abstractions** - each system has single responsibility

## Trade-offs and Considerations

### Potential Downsides (Acceptable)
- **Slight duplication** - footnotes repeated across similar cars
- **Manual maintenance** - need to update docs when adding platforms
- **Loss of shared constants** - can't reuse flag enums

### Why These Are Acceptable
- **Duplication is minimal** - just a few footnotes per brand
- **Manual maintenance is rare** - new platforms added infrequently  
- **Clarity over DRY** - explicit is better than clever

### What We Keep Dynamic
Only keep `init_make` pattern where genuinely needed:
- **Honda harness selection** - legitimately varies by ECU generation within same model
- **Subaru longitudinal availability** - complex technical constraints
- **Cases with real runtime variation** - not just static platform flags

## Implementation Guidelines

### For Static Cases (Preferred)
```python
# Direct static declaration
METADATA = {
    "PLATFORM_NAME": [
        CarDocs(
            name="Clear Name",
            footnotes=[StaticFootnote.EXAMPLE],
            car_parts=CarParts.common([StaticHarness.example])
        ),
    ],
}
```

### For Dynamic Cases (Only When Necessary)
```python
# Only use when documentation genuinely varies based on car capabilities
def init_make(self, CP: CarParams):
    if CP.alphaLongitudinalAvailable:  # Genuinely varies within platform
        self.footnotes.append(Footnote.EXP_LONG)
```

### Migration Strategy
1. **Start with obviously static cases** (Hyundai CANFD)
2. **Analyze each brand** - determine if variation is real or artificial
3. **Convert static cases** to direct data declarations
4. **Keep only genuinely dynamic cases** using `init_make`
5. **Document rationale** for remaining dynamic cases

## Scope and Boundaries

### In Scope
- ✅ Decoupling documentation from car interface flags
- ✅ Converting static flag checks to static data
- ✅ Simplifying documentation generation
- ✅ Reducing dependencies and coupling

### Out of Scope  
- ❌ Changing functional car interface logic
- ❌ Modifying CAN message generation
- ❌ Altering safety parameter logic
- ❌ Adding new documentation features

### Success Criteria
- Documentation generation works without importing car interface modules
- Tests run faster and with fewer dependencies
- New platforms can add documentation without touching car interface
- Code is simpler and more explicit

## Future Considerations

### When to Use Each Approach

**Use Static Documentation When:**
- Platform capabilities are fixed and known
- No variation within platform/model
- Pure installation/setup information
- Footnotes, harnesses, parts lists

**Use Dynamic Documentation When:**
- Genuine variation within same platform/model
- Documentation depends on detected car capabilities  
- Complex conditional logic required
- Multiple configurations possible

### Evolution Path
As the codebase evolves, prefer static approaches unless dynamic behavior is clearly necessary. The burden of proof should be on dynamic complexity - simple static data should be the default.

## Key Takeaway

**The fundamental insight:** Documentation generation is a static process working with static platform data. Using dynamic runtime patterns for static information creates unnecessary complexity and coupling without benefits.

**The principle:** Choose the simplest solution that works. Static data declarations are simpler than runtime flag checking for static platform properties. 