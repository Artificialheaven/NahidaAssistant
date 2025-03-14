from pathlib import Path
from tqdm import tqdm

import response_parser
import mypptx
import moonshot
import siliconflow
import audio
import ppt_shower


Moonshot = moonshot.Moonshot()
Siliconflow = siliconflow.Siliconflow()

# 第一阶段：从 PDF 等文件使用 Moonshot AI 获取内容大纲，并且生成 Markdown 格式的总结
file = Moonshot.create_file(Path("files/痛点察觉.pdf"))
Moonshot.add_file(file)
ret = Moonshot.chat("你现在需要分析并且简单总结上述文件的内容，并且输出以 Markdown 格式的内容大纲，其余内容一律禁止输出。")

# 第二阶段，使用 Siliconflow 的 Deepseek-R1 671B 对其进行总结，扩写
Siliconflow.add_user(ret)
ret = Siliconflow.chat("你现在需要分析并且扩充上述 Markdown 文件的内容，不要修改其标题和文章结构，只对其内容进行扩写，"
                       "结果使用 Markdown 格式输出。"
                       "不要输出其他任何内容。不需要使用 ''' ''' 代码框包装内容。")

# 第三阶段，保存 Markdown 格式的文件到目录，用户生成 ppt，随后继续运行
with open("test.md", 'w') as f:
    f.write(ret)

file_name = input("请输入 ppt 文件名：")

# 第四阶段，使用 Moonshot AI 分析 ppt 并且给出讲解文稿
json = mypptx.get_pptx_tree(file_name)
Siliconflow = siliconflow.SiliconflowV3()
Siliconflow.add_user(json)
ret, _ = Siliconflow.chat("以上是一份PPT的内容结构树，你需要对每一页PPT进行讲解，开篇需要根据ppt内内容获取时间并且自我介绍，主讲人为翟召臣。"
                          "你现在需要分析并且写一份文稿，要求对每一页PPT都进行讲解，格式为在每一页的开始输出 [开始-<页数>]  ，结束"
                          "的位置输出 [结束-<页数>]，如果本页内容较多，可以使用 [停顿-<秒数>] 在本页面停留一段时间，给用户阅读和思考的时间。"
                          "页数必须严格匹配树内的页码值。"
                          "几十中间讲解结构相似也必须每一页都进行讲解，不允许跳过或者压缩中间页面讲解内容。"
                          "要求使用纯文本生成，不要输出其他内容或者使用markdown语法。")

with open("test.txt", 'w') as f:
    f.write(ret)


with open("test.txt", 'r') as f:
    ret = f.read()
parsed_res, _ = response_parser.split_segments(ret)

workers = 0
for i in range(len(parsed_res)):
    workers += len(parsed_res[i])

with tqdm(total=workers) as pbar:
    pbar.set_description('生成克隆语音: ')
    # print(parsed_res)
    for i in range(len(parsed_res)):
        for j in range(len(parsed_res[i])):
            if "停顿" in parsed_res[i][j]:
                pbar.update(1)
                continue
            print(parsed_res[i][j])
            audio.create_audio(parsed_res[i][j], f"{i}-{j}.mp3")
            # print(f"{i}-{j} {parsed_res[i][j]}")
            pbar.update(1)


ppt_shower.open_ppt("需求挖掘：痛点痒点爽点与营销策略.pptx")
ppt_shower.play_ppt(parsed_res)
