import requests
import json
import pandas as pd
import time

def get_access_token():
    """获取百度API的access_token"""
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        'grant_type': 'client_credentials',
        'client_id': 'McL6b73vcUZII7nXRjkaehEW',  # API Key
        'client_secret': '6IzcCffSr5kQXkfJlJQaYTHooRKNRnqT'  # Secret Key
    }
    response = requests.post(url, params=params)
    return response.json().get('access_token')

def sentiment_analysis(text, access_token):
    """调用百度API进行情感分析"""
    url = f"https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token={access_token}"
    
    payload = json.dumps({
        'text': text
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload.encode('utf-8'))
        result = response.json()
        return result
    except Exception as e:
        print(f"分析出错: {str(e)}")
        return None

def save_results(result_df, filename):
    """保存结果到Excel文件"""
    try:
        result_df.to_excel(filename, index=False)
        print(f"已保存至: {filename}")
    except Exception as e:
        print(f"保存失败: {str(e)}")

def main():
    # 读取Excel文件
    try:
        df = pd.read_excel("再20条待分析.xlsx")
        print("成功读取数据文件")
    except Exception as e:
        print(f"读取文件失败: {str(e)}")
        return

    # 获取access_token
    access_token = get_access_token()
    if not access_token:
        print("获取access_token失败")
        return

    # 创建结果列前，先保存原始评论内容和情感倾向
    result_df = pd.DataFrame()
    result_df['评论内容'] = df['评论内容']
    # result_df['电商平台情感倾向'] = df['情感倾向']  # 保存原始情感倾向

    # 创建百度API分析结果列
    result_df['百度API情感分析结果'] = None   # 0:负向，1:中性，2:正向
    result_df['百度API情感倾向'] = None       # 情感倾向概率
    result_df['百度API置信度'] = None         # 置信度

    # 对每条评论进行情感分析
    for idx, row in df.iterrows():
        text = str(row['评论内容'])
        result = sentiment_analysis(text, access_token)
        
        if result and 'items' in result and len(result['items']) > 0:
            item = result['items'][0]
            result_df.at[idx, '百度API情感分析结果'] = item.get('sentiment', '')
            result_df.at[idx, '百度API情感倾向'] = item.get('sentiment_prob', 0)
            result_df.at[idx, '百度API置信度'] = item.get('confidence', 0)
        
        # 每处理50条数据保存一次
        if (idx + 1) % 50 == 0:
            print(f"已处理 {idx + 1} 条数据，正在保存...")
            save_results(result_df, '再20条内容情感待修正.xlsx')
        
        time.sleep(0.1)  # API调用间隔

    # 最后保存一次
    save_results(result_df, '再20条内容情感待修正.xlsx')
    print("\n分析完成，所有结果已保存")

if __name__ == '__main__':
    main()
