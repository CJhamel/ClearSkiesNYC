from UrbanFlow.urbanflow import CityDataSet


def main():
   # Automatically use your data folder paths
   traffic_file = "data/Automated_Traffic_Volume_Counts_20251129.csv"
   air_folder = "data/AirQuality"


   nyc_data = CityDataSet("New York City")
   nyc_data.load_data(traffic_file, air_folder)


   # Export summary with yearly averages
   nyc_data.export_summary("nyc_yearly_summary_report.txt")

if __name__ == "__main__":
   main()
