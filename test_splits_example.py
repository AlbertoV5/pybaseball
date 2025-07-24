#!/usr/bin/env python3
"""
Simple test script to verify the new Fangraphs splits functionality.
This script demonstrates how to use the new splits features.
"""

import sys
import os

# Add the pybaseball package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

try:
    from pybaseball import fg_batting_splits, fg_pitching_splits
    from pybaseball.enums.fangraphs import FangraphsSplits
    
    print("✅ Successfully imported splits functionality")
    
    # Test 1: Basic enum usage
    print(f"VS_LHH value: {FangraphsSplits.VS_LHH.value}")  # Should be 5
    print(f"AS_RHP value: {FangraphsSplits.AS_RHP.value}")  # Should be 96
    
    # Test 2: Test split formatting
    formatted_splits = FangraphsSplits.format_split_array([FangraphsSplits.VS_LHH, FangraphsSplits.AS_RHP])
    print(f"Formatted splits: {formatted_splits}")  # Should be "5,96"
    
    # Test 3: Test with different input types
    print("Testing format_split_array with different inputs:")
    print(f"  [5, 96]: {FangraphsSplits.format_split_array([5, 96])}")
    print(f"  '5,96': {FangraphsSplits.format_split_array('5,96')}")
    print(f"  ['VS_LHH', 'AS_RHP']: {FangraphsSplits.format_split_array(['VS_LHH', 'AS_RHP'])}")
    
    print("✅ All basic functionality tests passed!")
    print("\nNote: To test with actual data fetching, you would run:")
    print("  batting_splits = fg_batting_splits(2024, splits=[FangraphsSplits.VS_LHH])")
    print("  pitching_splits = fg_pitching_splits(2024, splits=[FangraphsSplits.AS_RHP])")
    print("\nBut we're not running those here to avoid making network requests.")
    
except Exception as e:
    print(f"❌ Error testing splits functionality: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 