import json
import numpy as np
import sys
import re

"""
Old regex patterns:

address_pattern = r'^(?P<street_num>\d+)\s+(?P<street_name>[A-Za-z\s]+),\s+(?P<city_name>[A-Za-z\s]+),\s+(?P<state_name>[A-Z]{2})\s+(?P<zip_code>\d{5}),\s+(?P<country>[A-Za-z\s]+)'

address_pattern = (
    r'^(?P<street_num>\d+)\s+(?P<street_name>[A-Za-z\s]+)\s*'  # Street num and name
    r'(?:#|STE|Suite|Ste|floor)?\s*(?P<apt_num>\d+)?\s*,?\s*'  # Optional Apt/Ste/Floor with optional apt_num
    r'(?P<city_name>[A-Za-z\s]+),\s+'  # City name
    r'(?P<state_name>[A-Z]{2})\s+(?P<zip_code>\d{5}),\s+'  # State and zip
    r'(?P<country>[A-Za-z\s]+)'  # Country
)

# Match and handle cases with special starting numeric block
    numeric_prefix_pattern = (
        r'^(?P<numeric_prefix>\d+),\s+(?P<street_num>\d+)\s+(?P<street_name>[A-Za-z\s]+),\s+'
        r'(?P<city_name>[A-Za-z\s]+),\s+(?P<state_name>[A-Z]{2})\s+(?P<zip_code>\d{5}),\s+'
        r'(?P<country>[A-Za-z\s]+)'
    )

address_pattern = (
    r'^(?P<street_num>\d+)\s+(?P<street_name>[A-Za-z\s]+)\s*'  # Street number and name
    r'(?:#|STE|Suite|Ste|floor)?\s*(?P<apt_num>[\w\s]+)?\s*,?\s*'  # Optional Apt/Ste/Floor with alphanumeric apt_num
    r'(?P<city_name>[A-Za-z\s]+),\s+'  # City name
    r'(?P<state_name>[A-Z]{2})\s+(?P<zip_code>\d{5}),\s+'  # State and zip code
    r'(?P<country>[A-Za-z\s]+)'  # Country
)
"""
def parse_address(address):
    # Regular expression to match the address format
    address_pattern = (
        r'^(?:(?P<numeric_prefix>\d+),\s+)?'  # Optional numeric prefix at the start
        r'(?P<street_num>\d+)\s+(?P<street_name>[A-Za-z\s]+)\s*'  # Street number and name
        r'(?:#|STE|Suite|Ste|floor)?\s*(?P<apt_num>[\w\s]+)?\s*,?\s*'  # Optional Apt/Ste/Floor with alphanumeric apt_num
        r'(?P<city_name>[A-Za-z\s]+),\s+'  # City name
        r'(?P<state_name>[A-Z]{2})\s+(?P<zip_code>\d{5}),\s+'  # State and zip code
        r'(?P<country>[A-Za-z\s]+)'  # Country
    )
    
    
    match = re.match(address_pattern, address)

    if not match:
        return None  # Return None if the address doesn't match any pattern
    
    # Extract the components from the match object
    components = match.groupdict()

    # Convert street_num and zip_code to integers
    components['numeric_prefix'] = int(components['numeric_prefix']) if components['numeric_prefix'] else components['numeric_prefix']
    components['street_num'] = int(components['street_num']) if components['street_num'] else components['street_num']
    components['zip_code'] = int(components['zip_code']) if components['zip_code'] else components['zip_code']
    
    return components

def load_tester(path):
    with open(path) as f:
        data = json.load(f)
    # print(data)
    return np.asarray(data)

def parse_object(map, file, failed):
    i=1
    for key, entry in map.items():
        # Check for the 'numeric_prefix' key and skip it
        if key == 'numeric_prefix':
            i+=1
            continue

        # Check for the last item and don't print the extra comma and space
        if i < len(map):
            end1=', '
        else:
            end1=''

        #
        if type(entry) == str:
            if key == 'address':
                file.write(f'"{key}": ')
                file.write('[{')
                parsed_address = parse_address(entry)

                # adkey = Address Key, adent = Address Entry
                if parsed_address:
                    failed = parse_object(parsed_address, file, failed)
                else:
                    print(entry)
                    failed+=1
                
                file.write('}]')
                file.write(f'{end1}')

            else:
                file.write(f'"{key}": "{entry}"{end1}')


        elif type(entry) == list:
            file.write(f'"{key}": [')
            j=1
            for item in entry:
                if j < len(entry):
                    end2=', '
                else:
                    end2=''

                file.write(f'"{item}"{end2}')
                j+=1
            file.write(']')

        elif not entry:
            file.write(f'"{key}": null{end1}')

        # It's a number
        else:
            file.write(f'"{key}": {entry}{end1}')
        i+=1

    return failed


def main():
    if len(sys.argv) < 2:
        print("no args lol")
    elif len(sys.argv) < 3:
        print("provide input and output file")
    else:
        arr = load_tester(sys.argv[1])

    with open(sys.argv[2], 'w') as file:
        failed = 0
        for map in arr:
            file.write('{')
            failed = parse_object(map, file, failed)
            file.write('}\n')
        
        if failed:
            print(f'Failed Address Matches: {failed}')

if __name__ == '__main__':
    main()