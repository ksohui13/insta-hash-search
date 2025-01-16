from flask import Flask, render_template, request
import requests
import config

app = Flask(__name__)

# config.py에서 액세스 토큰과 사용자 ID 불러오기
ACCESS_TOKEN = config.ACCESS_TOKEN
USER_ID = config.USER_ID

# Instagram Graph API의 URL
GRAPH_API_URL = 'https://graph.facebook.com/v12.0'

# 인기 게시물과 최신 게시물을 가져오는 함수
def get_instagram_posts(hashtag_id):
    # 인기 게시물 (top_media)
    top_media_url = f'{GRAPH_API_URL}/{hashtag_id}/top_media?user_id={USER_ID}&fields=id,caption,media_type,media_url&access_token={ACCESS_TOKEN}'
    top_media_response = requests.get(top_media_url)
    top_media_data = top_media_response.json().get('data', [])

    # 최신 게시물 (recent_media)
    recent_media_url = f'{GRAPH_API_URL}/{hashtag_id}/recent_media?user_id={USER_ID}&fields=id,caption,media_type,media_url&access_token={ACCESS_TOKEN}'
    recent_media_response = requests.get(recent_media_url)
    recent_media_data = recent_media_response.json().get('data', [])

    return top_media_data, recent_media_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 사용자가 입력한 해시태그 가져오기
        hashtag = request.form['hashtag']
        
        # 해시태그에 해당하는 ID를 요청하거나, 미리 설정된 해시태그 ID를 사용할 수 있습니다.
        # 예시에서는 해시태그 ID를 미리 알아두어야 합니다. 
        hashtag_id = get_hashtag_id_from_name(hashtag)

        # Instagram에서 인기 게시물과 최신 게시물 가져오기
        top_media_data, recent_media_data = get_instagram_posts(hashtag_id)

        return render_template('index.html', top_media=top_media_data, recent_media=recent_media_data, hashtag=hashtag)
    
    return render_template('index.html')

# 해시태그 이름을 ID로 변환하는 함수 (예시로 기능 구현)
def get_hashtag_id_from_name(hashtag):
    # Instagram Graph API에서 해시태그 이름을 ID로 변환하는 API 호출 (예시)
    hashtag_url = f'https://graph.facebook.com/ig_hashtag_search?user_id={USER_ID}&q={hashtag}&access_token={ACCESS_TOKEN}'
    response = requests.get(hashtag_url)
    hashtag_data = response.json()
    
    # 해시태그 ID 반환
    return hashtag_data['data'][0]['id'] if 'data' in hashtag_data else None

if __name__ == '__main__':
    app.run(debug=True)
