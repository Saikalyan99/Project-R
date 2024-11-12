import json

def remove_duplicates(input_file, output_file):
    # Load the data from the JSON file
    with open(input_file, "r") as f:
        data = json.load(f)

    # Use a set to track unique entries
    seen = set()
    deduplicated_data = []

    for item in data:
        # Define a unique identifier (e.g., name and plus_code)
        name = item.get("name")
        plus_code = item.get("plus_code", None)  # None if plus_code is missing
        identifier = (name, plus_code)

        # Check if identifier is unique, then add to deduplicated_data
        if identifier not in seen:
            deduplicated_data.append(item)
            seen.add(identifier)

    # Save the deduplicated data to a new JSON file
    with open(output_file, "w") as f:
        json.dump(deduplicated_data, f, indent=4)

    print(f"Duplicates removed. Deduplicated data saved to {output_file}")

# Example usage
input_file = "restaurants_results.json"
output_file = "restaurants_results_deduplicated.json"
remove_duplicates(input_file, output_file)
