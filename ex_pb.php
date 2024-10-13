<?php
require 'MySQL.php';
function echoOption($row,$tag){
		if ($tag=='_group'){
			echo '<input hidden="hidden" id="_group" value="'.$row[$tag].'"></input>';
		}else{
		echo '<input hidden="hidden" id="'.$tag.'" value="'.$row[$tag].'"></input>';
		}

}
function checkISNOTempty($result,$tag){
	if ($result[$tag]==''){

	}
	else{
		if ($tag=='_group'){
			echo '<option value="_group">_group</option>';
		}else{
		echo '<option value="'.$tag.'">'.$tag.'</option>';
		}
	}
}
function echoList($id){
require 'MySQL.php';
$conn = new PDO("mysql:host=$mysql_host;dbname=$db", $mysql_user, $mysql_password);
    // set the PDO error mode to exception
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$sql=<<<EOF
select language,parody,_character,_group,artist,male,female,misc,cosplayer,mixed,other,reclass from `ex where id=:id;
EOF;
$sql=<<<EOF
call getid(:id);
EOF;
    $tag_array = array("language","parody","_character","_group","artist","male","female","misc","cosplayer","mixed","other","reclass","gd3_uploader");
$stmt = $conn->prepare($sql);
        $stmt->bindParam(':id', $id, PDO::PARAM_STR);
$stmt->execute();
	$Allrow = $stmt->fetch(PDO::FETCH_ASSOC);
        echo '<h4>需要屏蔽的TAG:</h4>';
	echo '<form action="ex_pb.php" method="get">';
	echo '<label>种类:</label>';
	# 输出TAG_LIST
	echo '<select style="width:100px;" name="tag_list" id="tag_list">';
        foreach($tag_array as $tag){
                checkISNOTempty($Allrow,$tag);
        }
	echo '</select>';
	echo '<br/>&nbsp;&nbsp;';
	echo '<label>条目:</label>';
	# 输出第一个TAG_LIST中的TAG
	echo '<select style="width:125px;" name="tag" id="tag">';
        foreach($tag_array as $tag){
                if($Allrow[$tag]!=""){
                        $tag_result = $Allrow[$tag];
                        $new_array = explode(',',$Allrow[$tag]);
                        foreach ($new_array as $a){
                                echo '<option>';
                                echo $a;
                                echo '</option>';
                        }
                        break;
                }
        }
	echo '</select>';
	echo '<button type="submit">提交</button>';
	echo '</form>';
echo '<hr>';
echo '<h4>输入需要屏蔽的标题:</h4>';
echo '<form action="ex_pb.php" method="get">';
echo '<input name="title_"></input>';
echo '<button  type="submit">提交</button>';
echo '</form>';
	# 输出TAG到隐藏区域
	foreach($tag_array as $tag){
		echoOption($Allrow,$tag);
	}
}

if(is_array($_GET)&&count($_GET)>0)
{
    if (isset($_GET['id'])){
		$id =$_GET['id'];
		echoList($id);
    }
if (isset($_GET['title_'])){
$conn = new PDO("mysql:host=$mysql_host;dbname=$db", $mysql_user, $mysql_password);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$sql = "select count(*) from title_filter where title=:title";
$stmt = $conn->prepare($sql);
$stmt->bindParam(':title', $_GET['title_'], PDO::PARAM_STR);
$file_count = $stmt->fetch(PDO::FETCH_ASSOC);
$file_count = $file_count['count(*)'];
$conn = null;
if($file_count ==0){
$conn = new PDO("mysql:host=$mysql_host;dbname=$db", $mysql_user, $mysql_password);
$sql=<<<EOF
insert into title_filter (title) VALUES (:title);
EOF;
$stmt = $conn->prepare($sql);
$stmt->bindParam(':title', $_GET['title_'], PDO::PARAM_STR);
$stmt->execute();
$conn = null;
 }
echo "window.close();";
}
	if (isset($_GET['tag_list'])&isset($_GET['tag'])){
	# 先查询是否已经存在该TAG
$conn = new PDO("mysql:host=$mysql_host;dbname=$db", $mysql_user, $mysql_password);
    // set the PDO error mode to exception
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$sql = "select count(*) from filter_list where tag_list=:tag_list and tag=:tag";
    $stmt = $conn->prepare($sql);
$stmt->bindParam(':tag_list', $_GET['tag_list'], PDO::PARAM_STR);
$stmt->bindParam(':tag', $_GET['tag'], PDO::PARAM_STR);
$file_count = $stmt->fetch(PDO::FETCH_ASSOC);
$file_count = $file_count['count(*)'];
$conn = null;
# 不存在该条目 则增加该条目
if($file_count ==0){
$conn = new PDO("mysql:host=$mysql_host;dbname=$db", $mysql_user, $mysql_password);
$sql=<<<EOF
insert into filter_list (tag_list,tag) VALUES (:tag_list,:tag);
EOF;
$stmt = $conn->prepare($sql);
$stmt->bindParam(':tag', $_GET['tag'], PDO::PARAM_STR);
$stmt->bindParam(':tag_list', $_GET['tag_list'], PDO::PARAM_STR);
$stmt->execute();
$conn = null;
	  }
	echo "window.close();";
	}
}



?>
<html>
<head>
<script type="text/javascript" src="jquery-3.6.0.min.js">
</script>
</head>
<body>
</body>
<script>
// 获取GET参数
function GetQueryString(name)
{
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}
// 判断get参数
if (GetQueryString('tag_list')!=null&GetQueryString('tag')!=null){
	window.close(); 
}
if (GetQueryString('title_')!=null){
        window.close(); 
}
// 列表选取变更的JS
$(function(){
  $("#tag_list").change(function(){
	  var selected = $(this).val();
	  var tag_list = $("#"+selected).val();
	  $("#tag").empty();
	  var tag_array = tag_list.split(",");
	  for(var i in tag_array){
		  $("#tag").append("<option>"+tag_array[i]+"</option>");
	}
   });
});
</script>
</html>
