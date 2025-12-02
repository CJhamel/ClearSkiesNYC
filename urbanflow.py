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

        # Load Data:

        # Purpose:
        # Load traffic and air quality CSV files, merge them, and create CityRecord objects.
        # Input, Output:
        # Input: traffic_file (str), air_folder (str)
        # Output: None (populates self.records with CityRecord objects)
        # Identify the representation of the data:
        # Traffic CSV: 'Boro', 'Yr', 'M', 'D', 'Vol'
        # Air CSVs: 'County', 'Date', 'Daily Mean PM2.5 Concentration'
        # Each CityRecord: location (str), traffic_volume (int), pm25 (float), date (str)
        # Name and template the function:
        # def load_data(self, traffic_file: str, air_folder: str = "data/AirQuality")
        # Hand Test:
        # Traffic CSV row: {'Boro': 'Bronx', 'Yr': 2016, 'M': 5, 'D': 8, 'Vol': 356}
        # Air CSV row: {'County': 'Bronx', 'Date': '05/08/2016', 'Daily Mean PM2.5 Concentration': 12.5}
        # Expected: self.records contains CityRecord(location='bronx', traffic_volume=356, pm25=12.5, date='2016-05-08')
        # Implementation steps:
        # 1. Initialize empty index dictionary keyed by (location.lower(), date).
        # 2. Read traffic CSV row by row:
        #    - Skip non-NYC counties.
        #    - Parse date as YYYY-MM-DD.
        #    - Parse traffic volume as int.
        #    - Create CityRecord with pm25=0 and add to index.
        # 3. Read all air quality CSVs:
        #    - Skip non-NYC counties.
        #    - Parse date MM/DD/YYYY → YYYY-MM-DD.
        #    - Parse PM2.5 value as float.
        #    - Update corresponding CityRecord in index.
        # 4. Keep only records with traffic_volume > 0 and pm25 > 0.
        # 5. Assign list of valid records to self.records.

    def load_data(self, traffic_file: str, air_folder: str = "data/AirQuality"):
        """
        Load traffic CSV and all air quality CSVs in air_folder.
        Only keep rows where both traffic and PM2.5 exist (>0).
        Merge PM2.5 from air quality files by county/date.
        """
        import os
        import csv

        index = {}  # key = (county.lower(), date_str)
        NYC_COUNTIES = {"bronx", "brooklyn", "manhattan", "queens", "staten island"}

        # ---- Load traffic data ----
        with open(traffic_file, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                boro = row.get("Boro", "").strip().lower()
                if boro not in NYC_COUNTIES:
                    continue

                try:
                    year = int(row.get('Yr', 0))
                    month = int(row.get('M', 0))
                    day = int(row.get('D', 0))
                    date_str = f"{year:04d}-{month:02d}-{day:02d}"
                except Exception:
                    continue

                traffic_str = row.get('Vol', row.get('Volume', '0')).replace(',', '')
                try:
                    traffic = int(float(traffic_str))
                except Exception:
                    traffic = 0

                if traffic == 0:
                    continue  # skip traffic rows with no data

                location = boro
                key = (location, date_str)
                index[key] = CityRecord(location, traffic, 0.0, date_str)

        # ---- Load air quality CSVs ----
        if os.path.exists(air_folder):
            air_files = [os.path.join(air_folder, f)
                         for f in os.listdir(air_folder)
                         if f.startswith("ad_viz_plotval_data (") and f.endswith(".csv")]

            for air_file in air_files:
                with open(air_file, newline='', encoding='utf-8') as fh:
                    reader = csv.DictReader(fh)
                    for row in reader:
                        try:
                            # parse date MM/DD/YYYY → YYYY-MM-DD
                            m, d, y = row['Date'].split('/')
                            date_str = f"{int(y):04d}-{int(m):02d}-{int(d):02d}"

                            location = row.get('County', '').strip().lower()
                            if location not in NYC_COUNTIES:
                                continue

                            pm25 = float(row.get('Daily Mean PM2.5 Concentration', 0.0))
                            if pm25 == 0:
                                continue  # skip rows with no PM2.5 data

                            key = (location, date_str)
                            if key in index:
                                index[key].pm25 = pm25


                        except Exception:
                            continue  # skip invalid rows

        # ---- Keep only records where both traffic and PM2.5 are >0 ----
        self.records = [record for record in index.values()
                        if record.traffic_volume > 0 and record.pm25 > 0]

        print(f"Loaded {len(self.records)} valid records for NYC counties with traffic and PM2.5.")
        # Find HostSpot:

        # Purpose:
        # Identify locations with unusually high pollution relative to traffic.
        # Input, Output:
        # Input: threshold (float)
        # Output: List[CityRecord] where pollution-to-traffic ratio > threshold
        # Identify the representation of the data:
        # Each CityRecord has traffic_volume and pm25 attributes.
        # Ratio = pm25 / traffic_volume
        # Name and template the function:
        # def find_hotspots(self, threshold: float) -> List[CityRecord]
        # Hand Test:
        # Records:
        #   CityRecord(location='A', traffic_volume=100, pm25=5) → ratio 0.05
        #   CityRecord(location='B', traffic_volume=200, pm25=1) → ratio 0.005
        # Threshold: 0.01
        # Expected output: [CityRecord(location='A', ...)]
        # Implementation steps:
        # 1. Initialize empty list `hotspots`.
        # 2. Iterate through self.records:
        #    - Skip if traffic_volume <= 0 or pm25 <= 0.
        #    - Compute ratio = record.pm25 / record.traffic_volume.
        #    - If ratio > threshold, append record to hotspots.
        # 3. Return hotspots list (empty if none meet threshold).

    def find_hotspots(self, threshold: float) -> List[CityRecord]:
        """
        Find locations with pollution-to-traffic ratios above the specified threshold.


        Args:
            threshold: Minimum pollution-to-traffic ratio to be considered a hotspot


        Returns:
            List of CityRecord objects that exceed the threshold
        """
        hotspots = []
        for record in self.records:
            # Skip records with zero traffic or zero PM2.5 to avoid invalid ratios
            if record.traffic_volume > 0 and record.pm25 > 0:
                ratio = record.compute_pollution_to_traffic_ratio()
                if ratio > threshold:
                    hotspots.append(record)
        return hotspots

        # Purpose:
        # Generate a formatted report of traffic and air quality statistics and write to a file.
        # Input, Output:
        # Input: output_file (str)
        # Output: None (writes report to file)
        # Identify the representation of the data:
        # - self.records: list of CityRecord objects
        # - Compute statistics using helper methods:
        #   - self.average_traffic() → float
        #   - self.average_air_quality() → dict with 'pm25'
        # - Count high traffic and poor air quality locations.
        # Name and template the function:
        # def export_summary(self, output_file: str) -> None
        # Hand Test:
        # Records: 3 records with varying traffic and pm25
        # Threshold for hotspots: 0.01
        # Expected output: Text file with:
        #   - City: New York City
        #   - Total Records: 3
        #   - Average Traffic: computed value
        #   - Average PM2.5: computed value
        #   - High Traffic Locations: count
        #   - Poor Air Quality Locations: count
        #   - Hotspots: list of locations exceeding threshold
        # Implementation steps:
        # 1. Compute total_records = len(self.records).
        # 2. Compute avg_traffic = self.average_traffic().
        # 3. Compute avg_air = self.average_air_quality().
        # 4. Count high_traffic_count = number of records with traffic_volume >= threshold.
        # 5. Count poor_air_count = number of records with pm25 >= threshold.
        # 6. Compute hotspots using self.find_hotspots(threshold=0.01).
        # 7. Format report as multi-line string using f-strings.
        # 8. Write report to output_file using with open(..., 'w').
        # 9. Handle exceptions in file writing and print error if occurs.

    def export_summary(self, output_file: str) -> None:
        """
        Export a summary report including overall and yearly averages of traffic and PM2.5.
        """
        try:
            if not self.records:
                print("No records to summarize.")
                return

            # Overall averages
            overall_avg_traffic = self.average_traffic()
            overall_avg_air = self.average_air_quality()['pm25']

            # Aggregate yearly data
            yearly_data: Dict[int, Dict[str, List[float]]] = {}
            for record in self.records:
                year = int(record.date[:4])  # YYYY-MM-DD → YYYY
                if year not in yearly_data:
                    yearly_data[year] = {'traffic': [], 'pm25': []}
                yearly_data[year]['traffic'].append(record.traffic_volume)
                yearly_data[year]['pm25'].append(record.pm25)

            # Compute yearly averages
            yearly_avg_lines = []
            for year in sorted(yearly_data.keys()):
                traffic_list = yearly_data[year]['traffic']
                pm25_list = yearly_data[year]['pm25']
                avg_traffic = sum(traffic_list) / len(traffic_list)
                avg_pm25 = sum(pm25_list) / len(pm25_list)
                traffic_diff = avg_traffic - overall_avg_traffic
                pm25_diff = avg_pm25 - overall_avg_air
                yearly_avg_lines.append(
                    f"{year}: Avg Traffic = {avg_traffic:.2f} "
                    f"(Diff {traffic_diff:+.2f}), "
                    f"Avg PM2.5 = {avg_pm25:.2f} "
                    f"(Diff {pm25_diff:+.2f})"
                )

            # Hotspots
            hotspot_threshold = 0.01
            hotspots = self.find_hotspots(threshold=hotspot_threshold)
            hotspot_locations = [f"{r.location} - Ratio: {r.compute_pollution_to_traffic_ratio():.6f}"
                                 for r in hotspots]

            # Prepare report string
            report = (
                "========================================\n"
                "UrbanFlow Analysis Report\n"
                "========================================\n"
                f"City: {self.city_name}\n"
                f"Total Records: {len(self.records)}\n"
                f"Overall Average Traffic: {overall_avg_traffic:.2f} vehicles/hour\n"
                f"Overall Average PM2.5: {overall_avg_air:.2f} µg/m³\n\n"
                "Yearly Averages and Differences:\n"
            )
            report += "\n".join(yearly_avg_lines)
            report += "\n\nHotspots:\n" + ", ".join(hotspot_locations) + "\n"

            # Write to file
            with open(output_file, 'w') as f:
                f.write(report)

            print(f"Summary report successfully written to {output_file}")


        except Exception as e:
            print(f"Error writing summary report: {e}")

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
