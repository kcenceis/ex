<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,  initial-scale=1.0"/>
<script type="text/javascript" src="jquery-3.6.0.min.js"></script>

<?php
function char_replace($char){
	$_char=str_replace('%','%25',$char);
	$_char = str_replace('<','&lt;',$_char);
	$_char = str_replace('>','&gt;',$_char);
	$_char=str_replace('#','%23',$_char);
	$_char=str_replace('\'','%27',$_char);
	$_char=str_replace('\"','%22',$_char);
	$_char=str_replace('?','%3F',$_char);
	$_char=str_replace('+','%2B',$_char);
	$_char=str_replace('/','%2F',$_char);
	#   $_char=str_replace('&','%25',$_char);
	$_char=str_replace('=','%3D',$_char);
	return $_char;
}


function ex(){
require 'MySQL.php';
$conn = new PDO("mysql:host=$mysql_host;dbname=$db", $mysql_user, $mysql_password);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$sql = "call getEX_Count()";
$stmt = $conn->prepare($sql);
$stmt->execute();
$sql_count = $stmt->fetch(PDO::FETCH_ASSOC)['count(*)'];
$lastpg=ceil($sql_count/100);

$page_offset = 0;
$page_count = 100;
$page = "";
if (isset($_GET['page'])){
       $page=$_GET['page'];
       $page_offset = ($page-1)*100;
   #若为最后一页
   if($page==$lastpg){
     $pagecount = $sql_count-($page-1)*100;
   }
}



// 当前页码 (假设从GET参数获取)
$currentPage = isset($_GET['page']) ? (int)$_GET['page'] : 1;

// 确保当前页码在有效范围内
$currentPage = max(1, min($currentPage, $lastpg));

// 计算显示的页码范围
$range = 10;
$startPage = max(1, $currentPage - floor($range / 2));
$endPage = min($lastpg, $startPage + $range - 1);

// 调整startPage，确保显示的页码数量为$range
$startPage = max(1, $endPage - $range + 1);

// 生成分页HTML
$paginationHtml = '<div class="pagination">';

// 上一页
if ($currentPage > 1) {
    $paginationHtml .= '<a href="?page=' . ($currentPage - 1) . '">上一页</a> ';
}

// 显示页码
for ($i = $startPage; $i <= $endPage; $i++) {
    if ($i == $currentPage) {
        $paginationHtml .= '<span class="current">' . $i . '</span> ';
    } else {
        $paginationHtml .= '<a href="?page=' . $i . '">' . $i . '</a> ';
    }
}

// 下一页
if ($currentPage < $lastpg) {
    $paginationHtml .= '<a href="?page=' . ($currentPage + 1) . '">下一页</a>';
}

$paginationHtml .= '</div>';

// 输出分页HTML
echo $paginationHtml;
$conn = null;


$conn = new PDO("mysql:host=$mysql_host;dbname=$db", $mysql_user, $mysql_password);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$sql=<<<EOF
call getEX($page_offset,$page_count);
EOF;
$stmt = $conn->prepare($sql);
$stmt->execute();
$Allrow = $stmt->fetchAll(PDO::FETCH_ASSOC);
if(count($Allrow)>0){
		echo '<div class="parent">';
		echo '<div class="content">';
foreach($Allrow as $row){
			echo '<div class="c1">';
			echo '<div class="c2">';
			echo '<a href="'.$row['address'].'"><div>'.$row['title'].'</div></a> ';
			echo '</div>';
			echo '<div class="c3">';
			echo '<a href="'.$row['address'].'">';
                  # 取消lazyload
			#echo '<img  alt="" src="../favicon.ico" data-original="ex/Preview/'.char_replace($row['file_name']).'"/>';
                  echo '<img  alt="" src="ex/Preview/'.char_replace($row['file_name']).'" data-original="ex/Preview/'.char_replace($row['file_name']).'"/>';
			echo "</a>";
			echo '</div>';
			echo '<div class="c4">';
#			if ($row['magnet']!=""){
#				echo "<a  href=".$row['magnet']."><button type='button'>磁链</button></a>";
#			}else{
#				echo '<button class="dl" type="button" value="excatch.php?address='.$row['address'].'">抓图</button></a>';
#			}
#                       echo "&nbsp";
#                        echo "<button type='button' id='push' value='".$row['address']."'>推送</button>";
			echo "&nbsp";
                        echo '<a onClick="openPB('.$row['id'].')"><button type="button">屏蔽</button></a>';
                        echo "&nbsp";
                        echo "<button type='button' id='gettag' value='".$row['address']."'>抓TAG</button>";
			echo '</div>';
			echo '</div>';
             }
		echo "<title>ex</title>";
		echo '</div>';
		echo '</div>';
echo $paginationHtml;
    }else{
		echo "空白页";
		echo "<title>无数据</title>";
	}
}
function endecho(){
	# 增加右下角 删除功能
	echo "<div class='right_bottom'>";
	echo '<button type="button" id="rm" value="rmdir.php">Delete</button>';
	echo '<button type="button" onclick="openNEW(\'tag\')">TAG黑名单</button>';
        echo '<button type="button" onclick="openNEW(\'title\')">title黑名单</button>';
	echo "</div>";
}
function delScript(){
	echo '<script>';
	echo '$(document).keydown(function(event){';
	echo 'if(event.keyCode==46){';
	echo '$.get("rmdir.php",function(data,status){});';
	echo '}';
	echo '});';
	echo '</script>';
}
$search_form_html=<<<EOF
    <div class="search-container">
<form action="#" method="get">
        <input name="search_text" type="text" class="search-input" placeholder="搜索...">
        <button class="search-button">
            <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
            </svg>
        </button>
</form>
    </div>
EOF;
#echo $search_form_html; #搜索栏
endecho();
ex();
delScript();
?>

<body>
</body>
<style>

.pagination {
    margin: 20px 0;
    text-align: center;
}
.pagination a, .pagination span {
    padding: 5px 10px;
    margin: 0 2px;
    border: 1px solid #ddd;
    text-decoration: none;
    color: #337ab7;
}
.pagination span.current {
    background-color: #337ab7;
    color: white;
    border-color: #337ab7;
}
div.right_bottom{
background: #C0C0C0;
color:#ffffff;
overflow: hidden;
z-index: 9999;
position: fixed;
padding:5px;
text-align:center;

border-bottom-left-radius: 4px;
border-bottom-right-radius: 4px;
border-top-left-radius: 4px;
border-top-right-radius: 4px;
right: 10px;
bottom: 150px;

display:grid;
}
body {
    background: darkgray;
    font-family: sans-serif;
    text-align: center;
    font-size: small;
}
.parent{
margin:0 auto;
#border:1px solid #000;
#max-width:1360px;

}
.content{
    display: flex;
    flex-wrap: wrap;
    align-items: stretch;
    padding: 0 !important;
    border-left: 1px solid #6f6f6f4d;
}
.content {
    display: grid;
    grid-template-columns: repeat(5,1fr);
}

@media screen and (max-width: 1360px){
 .content {
     grid-template-columns: repeat(4,1fr);
 }
}
@media screen and (max-width: 1090px){
 .content {
     grid-template-columns: repeat(3,1fr);
 }
}
.c1 {
    min-height: 200px;
    padding-bottom: 2px;
    min-width: 267px;
    max-width: 267px;
    display: flex;
    flex-direction: column;
    border-right: 1px solid #6f6f6f4d;
    border-bottom: 1px solid #6f6f6f4d;
}
.c1 {
    min-width: 250px;
    max-width: 400px;
}
.c2{
	overflow: hidden;
    min-height: 32px;
    max-height: 32px;
    line-height: 16px;
    margin: 6px 4px 0;
    font-size: 10pt;
    text-align: center;
}
.c3{
	overflow: hidden;
    border-radius: 5px;
    margin: 3px auto 0;

}
.c4{
    margin: auto auto 0 auto;
    display: flex;
    flex-direction: row;
    justify-content: center;
}
button{
font-family: sans-serif;
}
a{
text-decoration:none;
color: black;
}
        .search-container {
            position: relative;
            width: 300px;
            margin: 0 auto;
        }

        .search-input {
            width: 100%;
            padding: 10px 15px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 25px;
            outline: none;
            transition: all 0.3s ease;
        }

        .search-input:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 8px 0 rgba(76,175,80,0.4);
        }

        .search-button {
            position: absolute;
            right: 5px;
            top: 50%;
            transform: translateY(-50%);
            border: none;
            background: none;
            cursor: pointer;
        }

        .search-icon {
            width: 20px;
            height: 20px;
            fill: #666;
            transition: fill 0.3s ease;
        }

        .search-button:hover .search-icon {
            fill: #4CAF50;
        }
</style>
<script>
//$(".cs").click(function(){   
//   $(this).attr("data-disabled",function(i,origValue){
//      if(typeof(origValue) == "undefined"){
//	  return "1";
//	  }else{
//	   $(this).removeAttr("data-disabled");
//	  }
//   });
//});
pushurl = 'qqpush.php'
$(document).ready(function(){
        $("button").click(function(){
                var btn_id = $(this).attr("id");
                if(btn_id=="push"){
                $(this).attr("disabled",true);
                var buttonValue = $(this).val();
                $.post(pushurl,{address : buttonValue});
                } else if (btn_id=="rm"){
                $(this).attr("disabled",true);
                var url = $(this).val();
                $.get(url,function(data,status){
                        //alert("数据: " + data + "\n状态: " + status);
                });
                } else if (btn_id=="gettag"){
                $(this).attr("disabled",true);
                var url = $(this).val();
                $.post("ex_gettag.php",{address : url});
                }
        });
});
$(function(){
	$(".dl").click(function(){
		$(this).attr("disabled",true);
		var url = $(this).val();
		$.get(url,function(data,status){
			//alert("数据: " + data + "\n状态: " + status);
		});
	});
});

//$(function(){
//	$("#rm").click(function(){
//		$(this).attr("disabled",true);
//		var url = $(this).val();
//		$.get(url,function(data,status){
//			//alert("数据: " + data + "\n状态: " + status);
//		});
//	});
//});
//$("img").lazyload();
function openPB(value){
	window.open('ex_pb.php?id='+value,'','width=600,height=500,left=10, top=10,toolbar=no, status=no, menubar=no, resizable=yes, scrollbars=yes');return false;
}
function openNEW(value){
        if(value=='tag'){
	window.open('ex_black_list_tag.php','','width=600,height=500,left=10, top=10,toolbar=no, status=no, menubar=no, resizable=yes, scrollbars=yes');return false;
        }else if(value=='title'){
        window.open('ex_black_list_title.php','','width=600,height=500,left=10, top=10,toolbar=no, status=no, menubar=no, resizable=yes, scrollbars=yes');return false;
        }
}

function toggle(i){ 
	a = "#cat_"+i;
	var num1 = parseInt($("#f_cats").val());
	var num2 = parseInt(i);
	　　$(a).attr("data-disabled",function(i,origValue){
		if(typeof(origValue) == "undefined"){
			var result = num1+num2;
			$("#f_cats").val(result);
			return "1";
		}else{
			var result = num1-num2;
			$("#f_cats").val(result);
			$(a).removeAttr("data-disabled");
		}
	});
}
</script>
</html>
