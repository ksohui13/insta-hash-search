from flask import Flask, render_template, request
import requests
import config

app = Flask(__name__)

# config.py에서 액세스 토큰과 사용자 ID 불러오기
ACCESS_TOKEN = config.ACCESS_TOKEN
USER_ID = config.USER_ID

# Instagram Graph API URL
GRAPH_API_URL = 'https://graph.facebook.com/v21.0'

# JSON 데이터를 저장하는 함수 (디버깅 용도)
def save_json_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        import json
        json.dump(data, f, ensure_ascii=False, indent=4)

# Instagram 게시물 가져오기 함수
def get_instagram_posts(hashtag_id):
    try:
        # 인기 게시물
        top_media_url = f'{GRAPH_API_URL}/{hashtag_id}/top_media?user_id={USER_ID}&fields=id,caption,media_type,media_url,comments_count,like_count,permalink&access_token={ACCESS_TOKEN}'
        top_media_response = requests.get(top_media_url)
        top_media_response.raise_for_status()
        top_media_data = top_media_response.json().get('data', [])

        # 최근 게시물
        recent_media_url = f'{GRAPH_API_URL}/{hashtag_id}/recent_media?user_id={USER_ID}&fields=id,caption,media_type,media_url,comments_count,like_count,permalink&access_token={ACCESS_TOKEN}'
        recent_media_response = requests.get(recent_media_url)
        recent_media_response.raise_for_status()
        recent_media_data = recent_media_response.json().get('data', [])

        # JSON 데이터를 파일로 저장 (디버깅 용)
        save_json_to_file("top_media.json", top_media_data)
        save_json_to_file("recent_media.json", recent_media_data)

        return top_media_data, recent_media_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Instagram posts: {e}")
        return [], []

# 해시태그 ID 가져오기 함수
def get_hashtag_id_from_name(hashtag):
    try:
        hashtag_url = f'https://graph.facebook.com/ig_hashtag_search?user_id={USER_ID}&q={hashtag}&access_token={ACCESS_TOKEN}'
        response = requests.get(hashtag_url)
        response.raise_for_status()
        hashtag_data = response.json()
        if 'data' in hashtag_data and len(hashtag_data['data']) > 0:
            return hashtag_data['data'][0]['id']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching hashtag ID: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hashtag = request.form['hashtag']
        hashtag_id = get_hashtag_id_from_name(hashtag)

        if not hashtag_id:
            return render_template('index.html', error="Invalid hashtag. Please try another hashtag.")

        top_media_data, recent_media_data = get_instagram_posts(hashtag_id)
        return render_template('index.html', top_media=top_media_data, recent_media=recent_media_data, hashtag=hashtag)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
