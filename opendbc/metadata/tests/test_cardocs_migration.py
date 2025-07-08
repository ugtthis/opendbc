#!/usr/bin/env python3
"""
Simple CarDocs migration validation test.

Usage:
  # Generate baseline before migration
  python -c "from opendbc.metadata.tests.test_cardocs_migration import save_baseline; save_baseline()"
  
  # Run validation test
  python -m pytest opendbc/metadata/tests/test_cardocs_migration.py -v
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from opendbc.car.docs import get_all_car_docs
from opendbc.car.docs_definitions import Column


def save_baseline():
  """Generate and save CarDocs baseline for migration validation"""
  baseline_file = Path(__file__).parent / "baseline_cardocs.json"
  baseline = _generate_cardocs_baseline()
  with open(baseline_file, 'w') as f:
    json.dump(baseline, f, indent=2, sort_keys=True)
  print(f"✅ Baseline saved: {len(baseline)} cars → {baseline_file}")


def _generate_cardocs_baseline():
  """Generate comprehensive CarDocs baseline from current state"""
  baseline = []
  for car_doc in get_all_car_docs():
    baseline.append({
      'name': car_doc.name,
      'package': car_doc.package,
      'requirements': car_doc.requirements,
      'video': car_doc.video,
      'setup_video': car_doc.setup_video,
      'min_steer_speed': car_doc.min_steer_speed if car_doc.min_steer_speed != float('-inf') else None,
      'min_enable_speed': car_doc.min_enable_speed if car_doc.min_enable_speed != float('-inf') else None,
      'auto_resume': car_doc.auto_resume,
      'merged': car_doc.merged,
      'support_type': car_doc.support_type.value if car_doc.support_type else None,
      'support_link': car_doc.support_link,
      'make': car_doc.make,
      'model': car_doc.model,
      'years': car_doc.years,
      'year_list': car_doc.year_list,
      'car_parts': [str(part) for part in car_doc.car_parts.parts],
      'footnotes': [str(footnote) for footnote in car_doc.footnotes],
      'row_make': car_doc.row.get(Column.MAKE),
      'row_model': car_doc.row.get(Column.MODEL),
      'row_package': car_doc.row.get(Column.PACKAGE),
      'row_longitudinal': car_doc.row.get(Column.LONGITUDINAL),
      'row_fsr_longitudinal': car_doc.row.get(Column.FSR_LONGITUDINAL),
      'row_fsr_steering': car_doc.row.get(Column.FSR_STEERING),
      'row_steering_torque': str(car_doc.row.get(Column.STEERING_TORQUE)),
      'row_auto_resume': str(car_doc.row.get(Column.AUTO_RESUME)),
      'row_hardware': car_doc.row.get(Column.HARDWARE),
      'row_video': car_doc.row.get(Column.VIDEO),
      'row_setup_video': car_doc.row.get(Column.SETUP_VIDEO),
    })
  return sorted(baseline, key=lambda x: (x['make'], x['name']))


class TestCarDocsMigration:
  """Simple validation that CarDocs migration preserves all functionality"""
  
  @classmethod
  def setup_class(cls):
    cls.baseline_file = Path(__file__).parent / "baseline_cardocs.json"
    
    if cls.baseline_file.exists():
      with open(cls.baseline_file, 'r') as f:
        cls.baseline = json.load(f)
      cls.baseline_cars = {(car['make'], car['name']): car for car in cls.baseline}
    else:
      cls.baseline = None
      cls.baseline_cars = {}
    
    cls.current = _generate_cardocs_baseline()
    cls.current_cars = {(car['make'], car['name']): car for car in cls.current}

  def test_cardocs_migration(self):
    """Test CarDocs migration - shows all changes like GitHub diff"""
    if not self.baseline:
      pytest.fail("No baseline found. Run: python -c \"from opendbc.metadata.tests.test_cardocs_migration import save_baseline; save_baseline()\"")
    
    errors = []
    
    # Missing cars
    missing = set(self.baseline_cars.keys()) - set(self.current_cars.keys())
    for make, name in sorted(missing):
      errors.append(f"❌ MISSING: {make} {name}")
    
    # New cars
    new = set(self.current_cars.keys()) - set(self.baseline_cars.keys())
    for make, name in sorted(new):
      errors.append(f"➕ NEW: {make} {name}")
    
    # Changed cars
    common = set(self.baseline_cars.keys()) & set(self.current_cars.keys())
    for make, name in sorted(common):
      baseline_car = self.baseline_cars[(make, name)]
      current_car = self.current_cars[(make, name)]
      
      for attr in baseline_car:
        if baseline_car[attr] != current_car.get(attr):
          old_val = baseline_car[attr]
          new_val = current_car.get(attr)
          errors.append(f"🔄 CHANGED: {make} {name} → {attr}: '{old_val}' → '{new_val}'")
      
      for attr in current_car:
        if attr not in baseline_car:
          errors.append(f"➕ NEW ATTR: {make} {name} → {attr}: '{current_car[attr]}'")
    
    # Count check
    if len(self.current) != len(self.baseline):
      errors.append(f"📊 COUNT: {len(self.baseline)} → {len(self.current)} cars")
    
    if errors:
      error_msg = f"\n🚨 CarDocs Migration Failed ({len(errors)} changes detected):\n\n" + "\n".join(errors[:20])
      if len(errors) > 20:
        error_msg += f"\n... and {len(errors) - 20} more changes"
      pytest.fail(error_msg)
    
    print(f"✅ CarDocs Migration Passed: {len(self.current)} cars validated, no changes detected") 