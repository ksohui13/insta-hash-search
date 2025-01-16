from flask import Flask, render_template, request
import requests
import config

app = Flask(__name__)

# config.py에서 액세스 토큰과 사용자 ID 불러오기
ACCESS_TOKEN = config.ACCESS_TOKEN
USER_ID = config.USER_ID

# Instagram Graph API의 URL
GRAPH_API_URL = 'https://graph.facebook.com/v21.0'

# 인기 게시물과 최신 게시물을 가져오는 함수
# 게시글id, 설명, 미디어 타입, 미디어 url, 댓글 수,좋아요 수
def get_instagram_posts(hashtag_id):
    # 인기 게시물 (top_media)
    top_media_url = f'{GRAPH_API_URL}/{hashtag_id}/top_media?user_id={USER_ID}&fields=id,caption,media_type,media_url,comments_count,like_count&access_token={ACCESS_TOKEN}'
    top_media_response = requests.get(top_media_url)
    top_media_data = top_media_response.json().get('data', [])

    # 최근 게시물 (recent_media)
    recent_media_url = f'{GRAPH_API_URL}/{hashtag_id}/recent_media?user_id={USER_ID}&fields=id,caption,media_type,media_url,comments_count,like_count&access_token={ACCESS_TOKEN}'
    recent_media_response = requests.get(recent_media_url)
    recent_media_data = recent_media_response.json().get('data', [])

    # # 로그에 출력
    # print("Top Media Data:", top_media_data)
    # print("Recent Media Data:", recent_media_data)

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

# 해시태그 검색
def get_hashtag_id_from_name(hashtag):
    hashtag_url = f'https://graph.facebook.com/ig_hashtag_search?user_id={USER_ID}&q={hashtag}&access_token={ACCESS_TOKEN}'
    response = requests.get(hashtag_url)
    hashtag_data = response.json()
    
    # 해시태그 ID 반환
    return hashtag_data['data'][0]['id'] if 'data' in hashtag_data else None

if __name__ == '__main__':
    app.run(debug=True)
