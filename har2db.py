import json
import requests
import argparse

def load_har_file(file_path):
    """Loads a HAR file and returns its content."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Failed to parse {file_path} as JSON.")
        return None

def extract_request_data(har_data):
    """Extracts request data from HAR file content."""
    requests_data = []
    for entry in har_data['log']['entries']:
        request = entry['request']
        response = entry['response']
        
        # Extracting relevant information
        url = request['url']
        method = request['method']
        headers = dict(request['headers'])
        data = ""  # HAR files typically don't include request bodies
        
        status_code = response['status']
        response_headers = dict(response['headers'])
        content = response.get('content', {})
        content_size = content.get('size', 0)
        content_mimeType = content.get('mimeType', '')
        content_compression = content.get('compression', 0)
        content_text = content.get('text', "")
        
        responses_data = {
            'status_code': status_code,
            'headers': json.dumps(response_headers),
            'content_size': content_size,
            'content_mime_type': content_mimeType,
            'content_compression': content_compression,
            'content_text': content_text,
            'time': entry['time']
        }

        requests_data.append({
            'request': {
                'url': url,
                'method': method,
                'headers': json.dumps(headers),
                'data': data,
                'startedDateTime': entry['startedDateTime']
            },
            'response': responses_data
        })
    
    return requests_data

def send_request_to_db(_data, base_url='http://localhost:8000'):
    """Sends a request to the database via FastAPI endpoint."""
    for d in _data:
        req_data = d['request']
        resp_data = d['response']
        response = requests.post(f"{base_url}/requests", json=req_data)
        if response.status_code == 200:
            print(f"Request added successfully. ID: {response.json()['id']}")
            # Now, let's add the corresponding response
            # We need the request_id which we just got
            request_id = response.json()['id']
            # responses_data = {
            #     'status_code': 200,  # Placeholder, should be replaced with actual status code
            #     'headers': '{}',  # Placeholder
            #     'content': '',  # Placeholder
            # }
            response_response = requests.post(f"{base_url}/responses", json=resp_data, params={'request_id': request_id})
            if response_response.status_code == 200:
                print(f"Response added successfully. ID: {response_response.json()['id']}")
            else:
                print(f"Failed to add response. Status code: {response_response.status_code}")
        else:
            print(f"Failed to add request. Status code: {response.status_code}")

def main():
    parser = argparse.ArgumentParser(description='Load HAR file and send requests to database')
    parser.add_argument('har_file_path', help='Path to the HAR file')
    args = parser.parse_args()
    
    har_data = load_har_file(args.har_file_path)
    if har_data:
        _data = extract_request_data(har_data)
        send_request_to_db(_data)

if __name__ == "__main__":
    main()
