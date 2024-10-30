import json
import numpy as np
import sys
import re

from database_setup import *

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


def main():
    if len(sys.argv) < 2:
        print("please provide input file")
    else:
        data = load_tester(sys.argv[1])
        
    # Store username and password as environment variables or in a config file
    username = "root"
    password = "Pr0jectR"
    host = "localhost"
    port = "3306"  # Default MySQL port
    database = "ProjectR"


    
    tags = set()
    for store in data:
        for tag in store.get('types', []):
            tags.add(tag)

    engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}", echo=True)
    
    with Session(engine) as session:
        for tag in tags:
            if not session.query(Tags).filter_by(name=tag).first():
                session.add(Tags(name=tag))
        
        for store in data:
            address = parse_address(store['address'])
            new_store = Stores(
                name=store['name'],
                rating=store['rating'],
                numrating=store['user_ratings_total'],
                streetnum=address['street_num'],
                streetname=address['street_name'],
                aptnum=address['apt_num'],
                city=address['city_name'],
                state=address['state_name'],
                zip=address['zip_code'],
                country=address['country']
            )
            session.add(new_store)
            session.flush()

            for tag in store.get('types', []):
                tag_entry = session.query(Tags).filter_by(name=tag).first()
                if tag_entry:
                    store_tag = StoreTags(storeid=new_store.id, tagid=tag_entry.id)
                    session.add(store_tag)
        
        session.commit()

if __name__ == '__main__':
    main()