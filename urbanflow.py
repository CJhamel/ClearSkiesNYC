"""
UrbanFlow: NYC Traffic & Air Quality Analysis
CSC-101 Project
"""

from typing import List, Dict, Optional, Any


class CityRecord:
    """
    Represents a single data record for a city location with traffic and air quality metrics.
    
    Attributes:
        location: The location identifier (e.g., street name, intersection)
        traffic_volume: Number of vehicles per hour
        pm25: PM2.5 air quality reading in micrograms per cubic meter
        date: Optional date string for the record
    """
    
    # Thresholds for high traffic and poor air quality
    HIGH_TRAFFIC_THRESHOLD: int = 1000  # vehicles per hour
    POOR_AIR_PM25_THRESHOLD: float = 12.0  # micrograms per cubic meter
    
    def __init__(self, location: str, traffic_volume: int, pm25: float, 
                 date: Optional[str] = None) -> None:
        """
        Initialize a CityRecord with traffic and air quality data.
        
        Args:
            location: Location identifier for this record
            traffic_volume: Traffic volume in vehicles per hour
            pm25: PM2.5 concentration in micrograms per cubic meter
            date: Optional date string (format: YYYY-MM-DD)
        """
        self.location = location
        self.traffic_volume = traffic_volume
        self.pm25 = pm25
        self.date = date
    
    def is_high_traffic(self) -> bool:
        """
        Determine if this record represents high traffic conditions.
        
        Returns:
            True if traffic volume exceeds the high traffic threshold, False otherwise
        """
        return self.traffic_volume >= CityRecord.HIGH_TRAFFIC_THRESHOLD
    
    def is_poor_air(self) -> bool:
        """
        Determine if this record represents poor air quality conditions.
        
        Air quality is considered poor if PM2.5 exceeds the threshold.
        
        Returns:
            True if air quality is poor (PM2.5 exceeds threshold), False otherwise
        """
        return self.pm25 >= CityRecord.POOR_AIR_PM25_THRESHOLD
    
    def compute_pollution_to_traffic_ratio(self) -> float:
        """
        Calculate the ratio of PM2.5 pollution to traffic volume.
        
        Divides PM2.5 concentration by traffic volume.
        Higher ratios indicate more pollution per unit of traffic.
        
        Returns:
            Pollution-to-traffic ratio (float). Returns 0.0 if traffic volume is 0.
        """
        if self.traffic_volume == 0:
            return 0.0
        
        return self.pm25 / self.traffic_volume
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the CityRecord to a dictionary representation.
        
        Returns:
            Dictionary containing all record attributes
        """
        return {
            'location': self.location,
            'traffic_volume': self.traffic_volume,
            'pm25': self.pm25,
            'date': self.date,
            'is_high_traffic': self.is_high_traffic(),
            'is_poor_air': self.is_poor_air(),
            'pollution_to_traffic_ratio': self.compute_pollution_to_traffic_ratio()
        }


class CityDataSet:
    """
    Manages a collection of CityRecord objects for a specific city.
    
    Attributes:
        city_name: Name of the city
        records: List of CityRecord objects
    """
    
    def __init__(self, city_name: str) -> None:
        """
        Initialize a CityDataSet for the specified city.
        
        Args:
            city_name: Name of the city (e.g., "New York City")
        """
        self.city_name = city_name
        self.records: List[CityRecord] = []
    
    def average_traffic(self) -> float:
        """
        Calculate the average traffic volume across all records.
        
        Returns:
            Average traffic volume (float). Returns 0.0 if no records exist.
        """
        if not self.records:
            return 0.0
        
        total_traffic = sum(record.traffic_volume for record in self.records)
        return total_traffic / len(self.records)
    
    def average_air_quality(self) -> Dict[str, float]:
        """
        Calculate the average PM2.5 air quality metric across all records.
        
        Returns:
            Dictionary with 'pm25' key containing average value.
            Returns {'pm25': 0.0} if no records exist.
        """
        if not self.records:
            return {'pm25': 0.0}
        
        total_pm25 = sum(record.pm25 for record in self.records)
        num_records = len(self.records)
        
        return {
            'pm25': total_pm25 / num_records
        }
    
    # TODO (GAGE): implement load_data()
    # 
    # INSTRUCTIONS FOR GAGE:
    # This method should read data from CSV files and populate self.records with CityRecord objects.
    # 
    # Requirements:
    # 1. Use Python's csv module or pandas to read the CSV files
    # 2. You'll need to combine data from TWO sources:
    #    a) Traffic data: "data/Automated_Traffic_Volume_Counts_20251130.csv"
    #       - Column "street" maps to CityRecord.location
    #       - Column "Vol" maps to CityRecord.traffic_volume
    #       - Columns "Yr", "M", "D" can be combined to create date string (format: "YYYY-MM-DD")
    #    b) Air quality data: "data/ad_viz_plotval_data (*).csv" files
    #       - Extract PM2.5 values (column names may vary - check actual file structure)
    #       - Match air quality data to traffic data by location/date
    # 3. Create CityRecord objects from the combined data
    # 4. Append each CityRecord to self.records
    # 5. Handle potential errors (file not found, invalid data, missing columns, etc.)
    # 6. Note: The air quality CSV files may need special handling (they appear to be alias files)
    #
    def load_data(self, filepath: str) -> None:
        """
        Load city data from a CSV file and populate the records list.
        
        Args:
            filepath: Path to the CSV file containing city data
        """
        pass
    
    # TODO (GAGE): implement find_hotspots()
    #
    # INSTRUCTIONS FOR GAGE:
    # This method should identify locations with high pollution-to-traffic ratios.
    #
    # Requirements:
    # 1. Iterate through all records in self.records
    # 2. For each record, compute the pollution-to-traffic ratio using record.compute_pollution_to_traffic_ratio()
    # 3. If the ratio exceeds the given threshold, add the record to the results list
    # 4. Return a list of CityRecord objects that are considered hotspots
    # 5. Consider returning an empty list if no records meet the threshold
    #
    # Example logic:
    #   hotspots = []
    #   for record in self.records:
    #       if record.compute_pollution_to_traffic_ratio() > threshold:
    #           hotspots.append(record)
    #   return hotspots
    #
    def find_hotspots(self, threshold: float) -> List[CityRecord]:
        """
        Find locations with pollution-to-traffic ratios above the specified threshold.
        
        Args:
            threshold: Minimum pollution-to-traffic ratio to be considered a hotspot
            
        Returns:
            List of CityRecord objects that exceed the threshold
        """
        pass
    
    # TODO (GAGE): implement export_summary()
    #
    # INSTRUCTIONS FOR GAGE:
    # This method should generate and write a summary report to a file.
    #
    # Requirements:
    # 1. Create a formatted text report containing:
    #    - City name
    #    - Total number of records
    #    - Average traffic volume (use self.average_traffic())
    #    - Average air quality metrics (use self.average_air_quality())
    #    - Number of high traffic locations
    #    - Number of poor air quality locations
    #    - List of hotspot locations (use self.find_hotspots() with an appropriate threshold)
    # 2. Write the report to the specified output_file path
    # 3. Use proper file handling (open, write, close) or context managers
    # 4. Format the output in a readable way (consider using f-strings or template formatting)
    # 5. Handle potential file writing errors
    #
    # Suggested report format:
    #   ========================================
    #   UrbanFlow Analysis Report
    #   ========================================
    #   City: [city_name]
    #   Total Records: [count]
    #   Average Traffic: [value] vehicles/hour
    #   Average PM2.5: [value] µg/m³
    #   High Traffic Locations: [count]
    #   Poor Air Quality Locations: [count]
    #   Hotspots: [list of locations]
    #
    def export_summary(self, output_file: str) -> None:
        """
        Export a summary report of the dataset to a file.
        
        Args:
            output_file: Path to the output file
        """
        pass


# ---- CHRISTOPHER'S TEST CODE BELOW ----

def main():
    """Test script demonstrating CityRecord and CityDataSet functionality."""
    
    # Manually create 2-3 CityRecord objects using real data from NYC traffic and air quality datasets
    # Data based on actual NYC traffic volume counts and typical NYC air quality readings
    record1 = CityRecord(
        location="HEMPSTEAD AVENUE",
        traffic_volume=356,  # Real traffic volume from Automated_Traffic_Volume_Counts dataset
        pm25=12.5,  # Typical NYC PM2.5 reading (micrograms per cubic meter)
        date="2016-05-08"
    )
    
    record2 = CityRecord(
        location="METROPOLITAN AVENUE",
        traffic_volume=190,  # Real traffic volume from dataset
        pm25=9.8,  # Typical NYC PM2.5 reading
        date="2016-01-17"
    )
    
    record3 = CityRecord(
        location="1 AVENUE",
        traffic_volume=1247,  # Realistic high-traffic NYC street
        pm25=15.2,  # Higher PM2.5 in high-traffic areas
        date="2016-05-08"
    )
    
    # Create CityDataSet and add records
    nyc_data = CityDataSet("New York City")
    nyc_data.records.append(record1)
    nyc_data.records.append(record2)
    nyc_data.records.append(record3)
    
    # Print average traffic
    avg_traffic = nyc_data.average_traffic()
    print(f"Average Traffic Volume: {avg_traffic:.2f} vehicles/hour")
    print()
    
    # Print average PM2.5
    avg_air = nyc_data.average_air_quality()
    print(f"Average PM2.5: {avg_air['pm25']:.2f} µg/m³")
    print()
    
    # Print pollution-to-traffic ratios for each record
    print("Pollution-to-Traffic Ratios:")
    for record in nyc_data.records:
        ratio = record.compute_pollution_to_traffic_ratio()
        print(f"  {record.location}: {ratio:.6f}")


if __name__ == "__main__":
    main()

