# 豆瓣添加条目助手 Douban listing helper

我的豆瓣 Follow me on Douban: lzqqqqqq (https://www.douban.com/people/49528893/)

豆瓣添加条目设计的太缺了，受不了了，设想写一个自动检索并自动填表的助手。目前只写了自动检索，但还是省去了不少麻烦。

## 进展 Progress

v 0.0.1
目前实现了：给定一批专辑的url（支持discogs/bangcamp链接，未来会增加支持），自动下载专辑信息和专辑并调整格式。填表还需要手动复制粘贴，上传封面也是，但还是能省不少麻烦的。

## 使用说明 Documentation

目前版本基于python3，并使用了这些库：pandas，os, re, requests, argparse, BeautifulSoup 4. 

如果你需要帮助配置python环境可以在豆瓣上私信我(https://www.douban.com/people/49528893/)，我会一一答复。配置过程很简单但不同系统不一样，就不在这里放全面的教程了。

使用：创建一个文本文档url_list.txt, 每一行粘贴一个专辑链接（暂时只支持discogs/bandcamp)，不能有空行。在命令行中运行：
~~~
python3 metadata_scrapper.py
~~~
专辑信息会和封面图片会自动下载到一个文件夹中。专辑信息是按豆瓣添加条目页面排好序的，逐行复制粘贴即可。也可以自定义输入文件和输出路径
~~~
python3 metadata_scrapper.py -i 'some_url_list_file.txt" -o "output_folder"
~~~

需要帮助或报bug随时开issue或者在豆瓣私信我。我网页开发的经验很少，很需要大家的帮助。

## 未来计划 Plan
- 添加网站支持（apple/spotfiy/soundcloud...)
- 自动填表
    - 我没有网页开发经验，熟悉javascript的朋友请私信我教我怎么写  
- 增加用户友好程度（不需要配置环境）
- 有什么建议或想参与这个项目欢迎开issue/在豆瓣上私信我 

## License 

MIT 
