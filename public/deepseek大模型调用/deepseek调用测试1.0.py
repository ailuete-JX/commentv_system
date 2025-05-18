import json
import time
import pandas as pd
from openai import OpenAI

def get_completion(prompt, temperature=0.7):
    """调用硅基流动API"""
    url = 'https://api.siliconflow.cn/v1/'
    api_key = 'sk-nvgchpifyvgkzlspzujqrojzfhpjsavcqnnjwjpshomrvfyr'

    client = OpenAI(
        base_url=url,
        api_key=api_key
    )
    
    messages = [{"role": "user", "content": prompt}]
    
    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",
            messages=messages,
            stream=False,
            temperature=temperature,
            max_tokens=1024  # 增加token上限以获取更详细的建议
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"API调用失败: {str(e)}")
        return None

def analyze_sentiment(text):
    """对单条评论进行情感分析"""
    prompt = f"""请分析以下电商评论的情感倾向。
评论内容："{text}"
只需回复一个数字：0表示消极情感，1表示积极情感。
不要解释，只输出数字0或1。"""
    
    try:
        result = get_completion(prompt)
        if result:
            result = result.strip()
            print(f"API返回结果: {result}")  # 调试输出
            if result in ['0', '1']:
                return int(result)
        return None
    except Exception as e:
        print(f"情感分析错误: {str(e)}")
        return None

def get_optimization_suggestion(comment):
    """根据用户评论生成优化建议"""
    prompt = f"""作为一个专业的产品经理和扫地机器人专家，请仔细分析以下用户评论，并提供具体的产品优化建议。
评论内容："{comment}"

请从以下几个方面提供优化建议：
1. 产品功能方面
2. 用户体验方面
3. 可能的技术改进
4. 其他建议

请给出详细但简洁的建议，每个方面不超过2-3点，确保建议具有可操作性。"""
    
    try:
        result = get_completion(prompt)
        return result if result else "抱歉，暂时无法生成优化建议。"
    except Exception as e:
        print(f"生成优化建议时出错: {str(e)}")
        return "系统处理出错，请稍后重试。"

def main():
    # 读取数据集
    print("正在读取数据集...")
    df = pd.read_excel('百度后60条待分析数据.xlsx')
    
    # 创建结果DataFrame
    result_df = pd.DataFrame()
    result_df['评论内容'] = df['评论内容']
    # result_df['原始情感倾向'] = df['情感倾向']
    result_df['60DeepSeek情感分析结果'] = None
    result_df['优化建议'] = None
    
    # 对每条评论进行分析
    total = len(df)
    print("\n开始情感分析和优化建议生成...")
    
    for idx, row in enumerate(df.iterrows()):
        comment = row[1]['评论内容']
        sentiment = analyze_sentiment(comment)
        suggestion = get_optimization_suggestion(comment)
        
        result_df.at[idx, '60DeepSeek情感分析结果'] = sentiment
        result_df.at[idx, '优化建议'] = suggestion
        
        # 显示进度
        if (idx + 1) % 10 == 0:
            progress = (idx + 1) / total * 100
            print(f"已处理: {idx + 1}/{total} ({progress:.1f}%)")
            time.sleep(1)  # 避免API限制
    
    # 保存结果
    output_file = 'DeepSeek情感分析结果_真.xlsx'
    result_df.to_excel(output_file, index=False)
    print(f"\n分析完成，结果已保存至: {output_file}")
    
    # 输出基本统计信息
    total = len(result_df)
    analyzed = result_df['60DeepSeek情感分析结果'].notna().sum()
    print(f"\n统计信息:")
    print(f"总评论数: {total}")
    print(f"成功分析数: {analyzed}")
    print(f"分析成功率: {(analyzed/total)*100:.2f}%")

if __name__ == "__main__":
    main()