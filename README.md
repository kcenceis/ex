# ex

抓取exhentai数据,预览图 写入到数据库记录<br>
过滤TAG，标题，上传人等条件，并显示到页面<br>
暂时只维护MySQL模式数据库<br>


## Debian/Ubuntu Install

git clone https://github.com/kcenceis/ex.git

pip3 install -r ex/requirements.txt

apt install php8.2 php8.2-mysql php8.2-fpm


## Usage

注意！！页面需要有tag内容才会显示数据，分开两次运行抓取是因为过早获得的页面有可能没有tag。

ex/config.json
<code>
{
"host":"数据库地址",
"user":"数据库用户名",
"password":"数据库密码",
"db":"数据库"
}</code>

### 设置每小时运行一次
crontab -e -u www-data

<code>0 * * * * /etc/caddy/html/tools/ex/venv/bin/python3 /etc/caddy/html/ex/main.py</code> # main.py 抓取预览图

<code>30 * * * * /etc/caddy/html/tools/ex/venv/bin/python3 /etc/caddy/html/ex/gettag.py</code> # gettag.py 抓取第二页页面信息(tag,上传者等等)

## Maintainer

[@kcenceis](https://github.com/kcenceis)

## License

[MIT License](LICENSE)
