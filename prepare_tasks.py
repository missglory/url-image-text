import requests
import json

def get_tasks():
    try:
        response = requests.get('http://localhost:8000/tasks', timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error occurred: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error occurred: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")
    return []

def get_urls(url_id):
    try:
        response = requests.get('http://localhost:8000/urls', timeout=10)
        response.raise_for_status()
        urls = [url for url in response.json() if url['id'] == url_id]
        return urls
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error occurred: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error occurred: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")
    return []

def get_requests():
    try:
        response = requests.get('http://localhost:8000/requests', timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error occurred: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error occurred: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")
    return []

def main():
    tasks = get_tasks()
    
    results_to_save = []
    for task in tasks:
        urls = get_urls(task['url_id'])
        requests_data = get_requests()
        request_found = next((req for req in requests_data if req['task_id'] == task['id']), None)
        for url in urls:
            result = {
                "task_id": task['id'],
                "url": url['value'],
                # "request_id": request_found['id'] if request_found else None,
            }
            results_to_save.append(result)
    
    with open('results.json', 'w') as f:
        json.dump(results_to_save, f, indent=4)

if __name__ == "__main__":
    main()