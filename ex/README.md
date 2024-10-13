# ex

抓取exhentai数据,预览图 写入到数据库记录

## Install

git clone https://github.com/kcenceis/ex.git

pip install -r requirements.txt

## Database_Design
SQLite: ex.db

<div>
    <table>
        <tr>
            <td colspan="4" align="center">ex</td>
        </tr>
        <tr>
            <td>Column</td>
            <td>SQL Type</td>
            <td>Size</td>
            <td>PK</td>
        </tr>
        <tr>
            <td>id</td>
            <td>INTEGER</td>
            <td></td>
            <td>PK</td>
        </tr>
        <tr>
            <td>title</td>
            <td>CHAR</td>
            <td>200</td>
            <td></td>
        </tr>
        <tr>
            <td>address</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>torrent_address</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>magnet</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
       </tr>
       <tr>
            <td>file_name</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>category</td>
            <td>CHAR</td>
            <td>200</td>
            <td></td>
        </tr>
        <tr>
            <td>language</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>parody</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>character</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>_group</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>artist</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>male</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>female</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>misc</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>_delete</td>
            <td>INT</td>
            <td>4</td>
            <td></td>
        </tr>
        <tr>
            <td>dDate</td>
            <td>TIMESTAMP</td>
            <td></td>
            <td></td>
        </tr>
    </table>
</div>
<div>
    <table>
        <tr>
            <td colspan="4" align="center">filter_list</td>
        </tr>
        <tr>
            <td>Column</td>
            <td>SQL Type</td>
            <td>Size</td>
            <td>PK</td>
        </tr>
        <tr>
            <td>id</td>
            <td>INTEGER</td>
            <td></td>
            <td>PK</td>
        </tr>
        <tr>
            <td>tag_list</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>tag</td>
            <td>CHAR</td>
            <td>2000</td>
            <td></td>
        </tr>
        <tr>
            <td>dDate</td>
            <td>TIMESTAMP</td>
            <td></td>
            <td></td>
        </tr>
    </table>
</div>


## Usage

<code>python main.py</code>

## Maintainer

[@kcenceis](https://github.com/kcenceis)

## License

[MIT License](LICENSE)
