# ex

抓取exhentai数据,预览图 写入到数据库记录<br>
过滤TAG，标题，上传人等条件，并显示<br>
暂时只维护MySQL模式数据库<br>

## Install

git clone https://github.com/kcenceis/ex.git

pip install -r requirements.txt


## Usage

config.json
<code>

{

"host":"数据库地址",

"user":"数据库用户名",

"password":"数据库密码",

"db":"数据库"

}</code>

<code>python main.py</code>

## Maintainer

[@kcenceis](https://github.com/kcenceis)

## License

[MIT License](LICENSE)
