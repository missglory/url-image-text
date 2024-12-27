import requests
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description='Get URLs and create tasks')
    parser.add_argument('url_value_filter', type=str, help='URL value filter for /urls endpoint')
    args = parser.parse_args()

    # Get URLs
    response = requests.get(f'http://localhost:8000/urls?url_value_filter={args.url_value_filter}')
    if response.status_code == 200:
        urls = response.json()
        for url in urls:
            url_id = url['id']
            print(f'Creating task for URL ID {url_id}...')

            # Create task
            task_data = {'url_id': url_id}
            response = requests.post('http://localhost:8000/tasks', json=task_data)
            if response.status_code == 200:
                print(f'Task created successfully. ID: {response.json()["id"]}')
            else:
                print(f'Failed to create task. Status code: {response.status_code}')
    else:
        print(f'Failed to get URLs. Status code: {response.status_code}')

if __name__ == "__main__":
    main()