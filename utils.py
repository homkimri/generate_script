from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

#定义函数 script:脚本，video_lenght:视频时长，creativity：创造性，api_key:用户的 api_key
def generate_script(subject, video_lenght, creativity, api_key):
    # 标题提示词模板
    title_template = ChatPromptTemplate.from_messages([
        ("human","请为'{subject}'这个主题的视频想一个吸引人的标题")
    ])
    #脚本提示词模板
    script_template = ChatPromptTemplate.from_messages([
        ("human","""你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```""")
    ])
    #模型实例化 如果使用第三方的API，添加参数openai_api_base="API地址"
    model = ChatOpenAI(model="gpt-3.5-turbo",openai_api_key=api_key,temperature=creativity)
    # 标题链
    title_chain = title_template | model
    # 脚本链
    script_chain = script_template | model
    # 生成标题
    title = title_chain.invoke({"subject": subject}).content
    # 基于 AI 提供的标题，维基百科搜索结果
    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)
    # 最终生成的脚本
    script = script_chain.invoke({"title": title,"duration": video_lenght,
                                  "wikipedia_search": search_result}).content
    return search_result,title,script
