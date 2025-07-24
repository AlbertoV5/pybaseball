from ..enum_base import EnumBase


class FangraphsSplits(EnumBase):
    """
    Enum for Fangraphs splits values used in the splitArr parameter.
    
    These splits can be combined using comma separation in the splitArr parameter.
    For example: splitArr=5,96 means "vs LHH" and "as RHP"
    """
    VS_LHH = 5   # vs Left-Handed Hitters
    VS_RHH = 6   # vs Right-Handed Hitters
    AS_RHP = 96  # as Right-Handed Pitcher
    AS_LHP = 97  # as Left-Handed Pitcher
    
    @classmethod
    def format_split_array(cls, splits) -> str:
        """
        Convert splits to the splitArr parameter format.
        
        Args:
            splits: Can be a single split, list of splits, or comma-separated string
            
        Returns:
            Comma-separated string of split values
        """
        if isinstance(splits, str):
            if ',' in splits:
                # Already formatted
                return splits
            # Single split as string, try to parse
            splits = [splits]
        
        if not isinstance(splits, list):
            splits = [splits]
        
        result_values = []
        for split in splits:
            if isinstance(split, cls):
                result_values.append(str(split.value))
            elif isinstance(split, str):
                # Try to parse as enum name
                parsed_split = cls.parse(split.upper())
                result_values.append(str(parsed_split.value))
            elif isinstance(split, int):
                result_values.append(str(split))
            else:
                raise ValueError(f"Invalid split type: {type(split)}")
        
        return ','.join(result_values) 