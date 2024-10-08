import requests
print("hello world")

def test_api():
    response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Failed to fetch data")

if __name__ == "__main__":
    test_api()