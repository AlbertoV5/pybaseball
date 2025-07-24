import pandas as pd
from datetime import datetime
import os
import hashlib
import time
from pybaseball import pitching_stats, batting_stats
from pybaseball.datasources.fangraphs import (
    FangraphsSplitsBattingTable,
    FangraphsSplitsPitchingTable,
)


# FangraphsSplitsBattingTable.ROOT_URL = PROXY_URL
# FangraphsSplitsPitchingTable.ROOT_URL = PROXY_URL

fg_batting_splits = FangraphsSplitsBattingTable().fetch
fg_pitching_splits = FangraphsSplitsPitchingTable().fetch

batting_stats = fg_batting_splits
pitching_stats = fg_pitching_splits


class FangraphsScraper:
    """Scraper for Fangraphs data via pybaseball with local CSV caching by day"""

    def __init__(self, cache_dir="cache"):
        self.cache_dir = cache_dir
        # Create cache directory if it doesn't exist
        self._setup_cache_dir()

    def _setup_cache_dir(self):
        """Create cache directory structure if it doesn't exist"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _generate_cache_key(self, method_name, **kwargs):
        """Generate a unique cache key based on method name and parameters"""
        # Create a string from sorted parameters
        param_str = "_".join(
            [f"{k}-{v}" for k, v in sorted(kwargs.items()) if v is not None]
        )
        # Create hash to handle long parameter strings
        param_hash = hashlib.md5(param_str.encode()).hexdigest()[:8]
        return f"fangraphs_{method_name}_{param_hash}"

    def _get_cache_filename(self, cache_key):
        """Get cache filename with today's date"""
        today = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.cache_dir, f"{cache_key}_{today}.csv")

    def _is_cache_valid(self, cache_file):
        """Check if cache file exists and is from today"""
        if not os.path.exists(cache_file):
            return False

        # Check if file is from today based on filename
        today = datetime.now().strftime("%Y-%m-%d")
        return today in cache_file

    def _load_from_cache(self, cache_file):
        """Load data from cache file"""
        try:
            df = pd.read_csv(cache_file)
            print(f"Loaded data from cache: {cache_file}")
            return df
        except Exception as e:
            print(f"Error loading cache file {cache_file}: {e}")
            return None

    def _save_to_cache(self, df, cache_file):
        """Save DataFrame to cache file"""
        try:
            df.to_csv(cache_file, index=False)
            print(f"Saved data to cache: {cache_file}")
        except Exception as e:
            print(f"Error saving to cache file {cache_file}: {e}")

    def __repr__(self):
        return f"FangraphsScraper(cache_dir={self.cache_dir})"

    def get_pitching_stats(self, year=2024, qual=50, use_cache=True):
        """
        Get Fangraphs pitching stats with caching

        Parameters:
        - year: season year
        - qual: minimum qualifying threshold
        - use_cache: whether to use cached data (default True)
        """

        # Generate cache key and filename
        cache_key = self._generate_cache_key(
            "pitching_stats",
            year=year,
            qual=qual,
        )
        cache_file = self._get_cache_filename(cache_key)

        # Try to load from cache first
        if use_cache and self._is_cache_valid(cache_file):
            cached_data = self._load_from_cache(cache_file)
            if cached_data is not None:
                return cached_data

        try:
            print(
                f"Fetching pitching stats from Fangraphs (year={year}, qual={qual})..."
            )
            df = pitching_stats(year, qual=qual)

            # Save to cache
            if use_cache:
                self._save_to_cache(df, cache_file)

            return df

        except Exception as e:
            print(f"Error fetching pitching stats: {e}")
            return None

    def get_batting_stats(self, year=2024, qual=50, use_cache=True):
        """
        Get Fangraphs batting stats with caching

        Parameters:
        - year: season year
        - qual: minimum qualifying threshold
        - use_cache: whether to use cached data (default True)
        """

        # Generate cache key and filename
        cache_key = self._generate_cache_key(
            "batting_stats",
            year=year,
            qual=qual,
        )
        cache_file = self._get_cache_filename(cache_key)

        # Try to load from cache first
        if use_cache and self._is_cache_valid(cache_file):
            cached_data = self._load_from_cache(cache_file)
            if cached_data is not None:
                return cached_data

        try:
            print(
                f"Fetching batting stats from Fangraphs (year={year}, qual={qual})..."
            )
            df = batting_stats(year, qual=qual)

            # Save to cache
            if use_cache:
                self._save_to_cache(df, cache_file)

            return df

        except Exception as e:
            print(f"Error fetching batting stats: {e}")
            return None

    def clear_cache(self, older_than_days=None):
        """
        Clear cache files

        Parameters:
        - older_than_days: if specified, only clear files older than this many days
                          if None, clear all cache files
        """
        if not os.path.exists(self.cache_dir):
            return

        cache_files = [
            f
            for f in os.listdir(self.cache_dir)
            if f.endswith(".csv") and "fangraphs" in f
        ]

        for cache_file in cache_files:
            file_path = os.path.join(self.cache_dir, cache_file)

            if older_than_days is None:
                # Clear all cache files
                os.remove(file_path)
                print(f"Removed cache file: {cache_file}")
            else:
                # Check file age
                file_time = os.path.getmtime(file_path)
                file_age = (time.time() - file_time) / (24 * 3600)  # days

                if file_age > older_than_days:
                    os.remove(file_path)
                    print(f"Removed old cache file: {cache_file}")


def main():
    scraper = FangraphsScraper()
    df = scraper.get_pitching_stats(year=2024, qual=50, use_cache=False)
    print(df)


if __name__ == "__main__":
    main()