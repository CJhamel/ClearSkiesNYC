import os
import csv

def count_air_quality_rows(air_folder: str) -> int:
    """Count all rows in all air quality CSV files (no restrictions)."""
    total_rows = 0
    if not os.path.exists(air_folder):
        print(f"Air quality folder not found: {air_folder}")
        return 0

    air_files = [os.path.join(air_folder, f)
                 for f in os.listdir(air_folder)
                 if f.startswith("ad_viz_plotval_data (") and f.endswith(".csv")]

    for f in air_files:
        try:
            with open(f, newline='', encoding='utf-8') as fh:
                reader = csv.DictReader(fh)
                total_rows += sum(1 for _ in reader)
        except Exception as e:
            print(f"Error reading air file {f}: {e}")

    return total_rows

def count_traffic_rows(traffic_file: str) -> int:
    """Count all rows in the traffic CSV file (no restrictions)."""
    total_rows = 0
    try:
        with open(traffic_file, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            total_rows = sum(1 for _ in reader)
    except FileNotFoundError:
        print(f"Traffic file not found: {traffic_file}")
    except Exception as e:
        print(f"Error reading traffic file: {e}")

    return total_rows

def main():
    # Paths
    script_dir = os.path.dirname(__file__)
    traffic_file = os.path.join(script_dir, "..", "data", "Automated_Traffic_Volume_Counts_20251129.csv")
    air_folder = os.path.join(script_dir, "..", "data", "AirQuality")
    output_file = os.path.join(script_dir, "data_summary.txt")  # <- same directory as script

    # Run both checks
    traffic_count = count_traffic_rows(traffic_file)
    air_count = count_air_quality_rows(air_folder)

    # Write results to single txt file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== NYC Data Summary ===\n")
            f.write(f"Total Traffic Rows (no restrictions): {traffic_count}\n")
            f.write(f"Total Air Quality Rows (no restrictions): {air_count}\n")
        print(f"Summary successfully written to {output_file}")
    except Exception as e:
        print(f"Error writing summary file: {e}")

if __name__ == "__main__":
    main()
