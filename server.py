from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os

app = Flask(__name__)

# 配置CORS，允许所有源
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# 配置日志记录
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置请求重试策略
retry_strategy = Retry(
    total=5,  # 增加重试次数
    backoff_factor=0.5,  # 重试间隔时间
    status_forcelist=[408, 429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"]
)
adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=10)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

# 全局异常处理
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"服务器发生错误: {str(error)}")
    return jsonify({
        'error': '服务器内部错误',
        'message': str(error)
    }), 500

@app.route('/api/token', methods=['GET'])
def get_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        'grant_type': 'client_credentials',
        'client_id': 'McL6b73vcUZII7nXRjkaehEW',
        'client_secret': '6IzcCffSr5kQXkfJlJQaYTHooRKNRnqT'
    }
    
    try:
        logger.info("开始获取access token")
        response = http.post(url, params=params, timeout=15)
        
        if response.status_code == 429:  # Too Many Requests
            logger.warning("API请求太频繁，等待后重试")
            time.sleep(2)  # 等待2秒后重试
            response = http.post(url, params=params, timeout=15)
            
        logger.info(f"Token请求响应状态码: {response.status_code}")
        logger.debug(f"Token请求响应内容: {response.text}")
        
        if response.status_code != 200:
            error_msg = f"请求Token失败，状态码: {response.status_code}"
            logger.error(error_msg)
            return jsonify({'error': error_msg}), response.status_code
            
        data = response.json()
        if 'error' in data:
            error_msg = f"获取Token失败: {data}"
            logger.error(error_msg)
            return jsonify({'error': f"API错误: {data.get('error_description', '未知错误')}"}), 400
            
        if 'access_token' not in data:
            error_msg = "响应中没有access_token"
            logger.error(error_msg)
            return jsonify({'error': '无效的API响应'}), 500
            
        logger.info("成功获取access token")
        return jsonify(data)
        
    except requests.exceptions.Timeout:
        error_msg = "请求Token超时"
        logger.error(error_msg)
        return jsonify({'error': '请求超时，请重试'}), 504
    except requests.exceptions.RequestException as e:
        error_msg = f"请求Token时发生错误: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': f'网络请求错误: {str(e)}'}), 500
    except Exception as e:
        error_msg = f"处理Token请求时发生未知错误: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/api/sentiment', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.json
        if not data or 'text' not in data or 'access_token' not in data:
            return jsonify({'error': '缺少必要参数'}), 400

        url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify"
        params = {'access_token': data['access_token']}
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payload = {'text': data['text']}

        logger.info(f"正在进行情感分析，文本长度: {len(data['text'])}")
        response = http.post(url, params=params, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 429:  # Too Many Requests
            logger.warning("API请求太频繁，等待后重试")
            time.sleep(2)
            response = http.post(url, params=params, json=payload, headers=headers, timeout=15)
            
        logger.info(f"情感分析响应状态码: {response.status_code}")
        logger.debug(f"情感分析响应内容: {response.text}")

        if response.status_code != 200:
            error_msg = f"情感分析请求失败，状态码: {response.status_code}"
            logger.error(error_msg)
            return jsonify({'error': error_msg}), response.status_code

        result = response.json()
        if 'error_code' in result:
            error_msg = f"情感分析API返回错误: {result}"
            logger.error(error_msg)
            return jsonify({'error': f"API错误: {result.get('error_msg', '未知错误')}"}), 400

        return jsonify(result)
        
    except requests.exceptions.Timeout:
        error_msg = "情感分析请求超时"
        logger.error(error_msg)
        return jsonify({'error': '请求超时，请重试'}), 504
    except requests.exceptions.RequestException as e:
        error_msg = f"情感分析请求时发生错误: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': f'网络请求错误: {str(e)}'}), 500
    except Exception as e:
        error_msg = f"处理情感分析时发生未知错误: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

if __name__ == '__main__':
    logger.info("正在启动Flask服务器...")
    # 确保日志文件存在
    if not os.path.exists('api_server.log'):
        open('api_server.log', 'a').close()
    app.run(host='127.0.0.1', port=5000)