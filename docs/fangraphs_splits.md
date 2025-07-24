# Fangraphs Splits Data

The pybaseball library now supports fetching splits data from Fangraphs, allowing you to analyze player performance in specific situations like vs Left-Handed Hitters (LHH), vs Right-Handed Hitters (RHH), as Right-Handed Pitcher (RHP), or as Left-Handed Pitcher (LHP).

## Available Functions

- `fg_batting_splits()` - Get batting splits data
- `fg_pitching_splits()` - Get pitching splits data

## Available Splits

The following splits are available using the `FangraphsSplits` enum:

- `VS_LHH` (5) - vs Left-Handed Hitters
- `VS_RHH` (6) - vs Right-Handed Hitters  
- `AS_RHP` (96) - as Right-Handed Pitcher
- `AS_LHP` (97) - as Left-Handed Pitcher

## Usage Examples

### Basic Usage

```python
from pybaseball import fg_batting_splits, fg_pitching_splits
from pybaseball.enums.fangraphs import FangraphsSplits

# Get batting splits for 2024 season vs LHH
batting_vs_lhh = fg_batting_splits(2024, splits=[FangraphsSplits.VS_LHH])

# Get pitching splits for 2024 season as RHP
pitching_as_rhp = fg_pitching_splits(2024, splits=[FangraphsSplits.AS_RHP])
```

### Multiple Splits

```python
# Get batting data for vs LHH and vs RHH
batting_splits = fg_batting_splits(2024, splits=[FangraphsSplits.VS_LHH, FangraphsSplits.VS_RHH])

# You can also use the numeric values directly
batting_splits = fg_batting_splits(2024, splits=[5, 6])

# Or use a comma-separated string
batting_splits = fg_batting_splits(2024, splits='5,6')
```

### Advanced Options

```python
# Get pitching splits with specific parameters
pitching_splits = fg_pitching_splits(
    start_season=2023,
    end_season=2024,
    splits=[FangraphsSplits.AS_RHP, FangraphsSplits.AS_LHP],
    position='P',  # Pitchers only
    qual=50,       # Minimum 50 plate appearances/innings
    stat_columns=['ERA', 'WHIP', 'K_9', 'BB_9', 'HR_9']  # Specific stats only
)
```

### Season Range

```python
# Get multi-season data
batting_splits = fg_batting_splits(
    start_season=2020,
    end_season=2024,
    splits=[FangraphsSplits.VS_LHH],
    split_seasons=True  # Separate data by season
)
```

## Parameters

All splits functions support the same parameters as the regular Fangraphs functions, plus:

| Parameter     | Type                    | Description
|  ---          | ---                     | ---
| splits        | Union[str, List, int]   | The splits to apply. Can be enum values, numeric codes, or comma-separated string
| auto_pt       | bool                    | Enable auto pitcher/team selection (default: True)
| split_teams   | bool                    | Whether to split by teams (default: False)
| group_by      | str                     | How to group results (default: 'season')

## Common Split Combinations

```python
# Pitcher splits - performance as RHP vs LHH and RHH
pitcher_splits = fg_pitching_splits(2024, splits=[
    FangraphsSplits.AS_RHP,  # When pitching as RHP
])

# Batter splits - performance vs different pitcher handedness
batter_splits = fg_batting_splits(2024, splits=[
    FangraphsSplits.VS_LHH,  # When facing LHP
    FangraphsSplits.VS_RHH   # When facing RHP
])

# Complete handedness analysis for pitchers
pitcher_handedness = fg_pitching_splits(2024, splits=[
    FangraphsSplits.AS_RHP,  # As right-handed pitcher
    FangraphsSplits.AS_LHP   # As left-handed pitcher  
])
```

## Notes

- The splits functionality uses Fangraphs' splits leaderboards endpoint
- Date ranges are automatically converted from seasons (e.g., 2024 becomes 2024-03-01 to 2024-11-01)
- Multiple splits will show combined data for those situations
- Some combinations may not make logical sense (e.g., AS_RHP and AS_LHP for the same player)
- Data availability depends on what Fangraphs has recorded for the specified splits and time periods 