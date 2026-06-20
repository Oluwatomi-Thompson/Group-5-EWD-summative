import pandas as pd
import json

def run_custom_dsa_ranking():
    print("RUNNING CUSTOM DSA RANKING ALGORITHM")
    
    try:
        print("Reading cleaned datasets...")
        clean_trips = pd.read_parquet("data/processed/cleaned_tripdata.parquet")
        
        print("Extracting columns into raw Python types...")
        raw_boroughs_list = clean_trips['pickup_borough'].dropna().tolist()
        
        print("Aggregating frequencies manually...")
        borough_counts = {}
        for borough in raw_boroughs_list:
            if borough in borough_counts:
                borough_counts[borough] += 1
            else:
                borough_counts[borough] = 1
                
        # Convert dictionary to a raw list of lists
        borough_items = list(borough_counts.items())
        
        print("Sorting records via manual Selection Sort...")
        n = len(borough_items)
        for i in range(n):
            max_idx = i
            for j in range(i + 1, n):
                # Compare both of the counts 
                if borough_items[j][1] > borough_items[max_idx][1]:
                    max_idx = j
            borough_items[i], borough_items[max_idx] = borough_items[max_idx], borough_items[i]
            
        print("\n[DSA RESULT] Top Pickup Boroughs:")
        for rank, (name, count) in enumerate(borough_items, 1):
            print(f"Rank {rank}: {name} -> {count} trips")
            
        with open("data/processed/dsa_ranking_results.txt", "w") as dsa_file:
            dsa_file.write("=== CUSTOM SELECTION SORT RESULTS ===\n")
            for rank, (name, count) in enumerate(borough_items, 1):
                dsa_file.write(f"Rank {rank}: {name} ({count} trips)\n")
                
        print("\nDSA Algorithm execution complete. Results saved.")
        
    except FileNotFoundError:
        print("\n[ERROR] Processed data not found. Please run pipeline.py first.")
    except Exception as e:
        print(f"\n[ERROR] Algorithmic execution failed")

if __name__ == "__main__":
    run_custom_dsa_ranking()
