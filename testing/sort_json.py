#!/usr/bin/env python3
import json

# Read the JSON file
with open('/home/apolosky/code/000mtg-parser/testing/test-consume.json', 'r') as f:
    data = json.load(f)

# Function to get the maximum value from a nested dictionary
def get_max_value(nested_dict):
    if not nested_dict:
        return 0
    return max(nested_dict.values())

# Sort the data by maximum value in descending order
sorted_data = dict(sorted(data.items(), key=lambda x: get_max_value(x[1]), reverse=True))

# Print the sorted results
print("Top 20 keys sorted by highest nested value:")
print("-" * 50)
for i, (key, nested_dict) in enumerate(sorted_data.items()):
    if i >= 20:  # Show only top 20
        break
    max_val = get_max_value(nested_dict)
    max_key = max(nested_dict.keys(), key=lambda k: nested_dict[k])
    print(f"{i+1:2d}. {key:<15} | Max value: {max_val:3d} (key: '{max_key}')")

# Save the sorted data to a new file
with open('/home/apolosky/code/000mtg-parser/testing/test-consume-sorted.json', 'w') as f:
    json.dump(sorted_data, f, indent=4)

print(f"\nSorted data saved to test-consume-sorted.json")