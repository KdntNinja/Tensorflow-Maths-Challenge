import requests

def get_closest_combination(num_input):
    api_key: int = 9521383
    try:
        response = requests.get(f"https://api.kdnsite.xyz/maths/{num_input}?api_key={api_key}")
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
    else:
        data = response.json()
        print(f"Closest total: {data["Closest total"]}\nOperation used: {data["Operation used"]}")

if __name__ == "__main__":
    while True:
        user_input = int(input("Enter a number: "))
        get_closest_combination(user_input)