
def run_pipeline():
    print("PIPELINE STARTED")

    print("Creating schema...")
    load_schema()

    print("Loading zones...")
    load_zones()

    print("Loading trips...")
    load_trips()

    print("Database setup complete")