<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,  initial-scale=1.0"/>
<script type="text/javascript" src="jquery-3.6.0.min.js"></script>
<!--# 取消lazyload-->
<!--<script type="text/javascript" src="jquery.lazyload.min.js"></script>-->

<?php
require 'SQLiteDB.php';
$ex_path = 'ex';
if(is_array($_GET)&&count($_GET)>0)
{
	if (isset($_GET['pic'])){
		$pic=$_GET['pic'];
		if($pic=='ex'){
			endecho();
		}
	}
}
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
	global $path;
	DBUtils::$db=new SQLiteDB('ex/ex.db');
	$sql = "select count(*) from ex where _delete is NULL";
	$db=DBUtils::$db;
	$stmt = $db->prepare($sql);
	$file_count = $stmt->execute()->fetchArray(SQLITE3_ASSOC);
	$file_count = $file_count['count(*)'];
	if($file_count>0){      
		$sql=<<<EOF
select tag_list,tag from filter_list;
EOF;
		$stmt = $db->prepare($sql);
		$ret = $stmt->execute();
		$result = "";

		while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
			$result= $result.' AND NOT '.$row['tag_list'].' like \'%'.$row['tag'].'%\' ';
		}
		$sql=<<<EOF
   select * from (select * from ex where _delete is NULL)
   where NOT category like '%Western%'  AND NOT category like '%Misc%' 
EOF;
		$sql_order_by = 'order by dDate desc;';
		$sql = $sql.$result.$sql_order_by;
		$db=DBUtils::$db;
		$stmt = $db->prepare($sql);
		$ret = $stmt->execute();
		echo '<div class="parent">';
		echo '<div class="content">';
		while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
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
			if ($row['magnet']!=""){
				echo "<a  href=".$row['magnet']."><button type='button'>磁链</button></a>";
			}else{
				echo '<button class="dl" type="button" value="excatch.php?address='.$row['address'].'">抓图</button></a>';
			}
                        echo "&nbsp";
                        echo "<button type='button' id='push' value='".$row['address']."'>推送</button>";
			echo "&nbsp";
                        echo '<a onClick="openPB('.$row['id'].')"><button type="button">屏蔽</button></a>';
			echo '</div>';
			echo '</div>';
		}
		echo "<title>ex</title>";
		echo '</div>';
		echo '</div>';

	}else{
		echo "空白页";
		echo "<title>无数据</title>";
	}
}
function endecho(){
	# 增加右下角 删除功能
	echo "<div class='right_bottom'>";
	echo '<button type="button" id="rm" value="rmdir.php">Delete</button>';
	echo '<button type="button" onclick="openNEW()">黑名单</button>';
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

if($pic=="ex"){
	ex();
	delScript();
}
?>

<body>
</body>
<style>
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
	window.open('ex_black_list.php','','width=600,height=500,left=10, top=10,toolbar=no, status=no, menubar=no, resizable=yes, scrollbars=yes');return false;
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
