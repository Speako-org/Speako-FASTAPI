# import requests 

# def send_txt_url_to_spring(record_id: int, txt_url: str):
#     url = "SPRING_API"
    
#     payload = {
#         "record_id" : record_id,
#         "s3_path" : txt_url
#     }
    
#     response = requests.post(url, json=payload)
#     response.raise_for_status()
#     return response.json()