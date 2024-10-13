<?php
require 'MySQL.php';
$ex_path = 'ex';
        # 删除操作
if(is_array($_GET)&&count($_GET)>0)
{
    if (isset($_GET['id'])&isset($_GET['tag_list'])&isset($_GET['tag'])){
$conn = new PDO("mysql:host=$mysql_host;dbname=$db", $mysql_user, $mysql_password);
    // set the PDO error mode to exception
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$sql=<<<EOF
delete from filter_list where id=:id and tag_list=:tag_list and tag=:tag;
EOF;
$stmt = $conn->prepare($sql);
$stmt->bindParam(':id', $_GET['id'], PDO::PARAM_STR);
$stmt->bindParam(':tag_list', $_GET['tag_list'], PDO::PARAM_STR);
$stmt->bindParam(':tag', $_GET['tag'], PDO::PARAM_STR);
$stmt->execute();
$conn = null;
    }
}


$conn = new PDO("mysql:host=$mysql_host;dbname=$db", $mysql_user, $mysql_password);
    // set the PDO error mode to exception
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$sql=<<<EOF
select * from filter_list;
EOF;
$stmt = $conn->prepare($sql);
$stmt->execute();
$Allrow = $stmt->fetchAll(PDO::FETCH_ASSOC);
                 echo '<div>';
		 echo '<table>';
		 echo '<tr>';
		 echo '<td>';
		 echo 'id';
		 echo '</td>';
		 echo '<td>';
		 echo '种类';
		 echo '</td>';
		 echo '<td>';
		 echo '条目';
		 echo '</td>';
		 echo '<td>';
		 echo '操作';
		 echo '</td>';
		 echo '</tr>';
         foreach($Allrow as $row){
			 echo '<tr>';
			 echo '<td>';
			 echo $row['id'];
			 echo '</td>';
			 echo '<td class="tag_list" name="tag_list">';
			 echo $row['tag_list'];
			 echo '</td>';
			 echo '<td class="tag" name="tag">';
			 echo $row['tag'];
			 echo '</td>';
			 echo '<td>';
			 echo '<a href="?id='.$row['id'].'&tag_list='.$row['tag_list'].'&tag='.$row['tag'].'"><button type="button">删除</button></a>';
			 echo '</td>';
			 echo '</tr>';
		 }
		 echo '</table>';
		 echo '</div>';
$conn = null;
?>
<style>
div{
    display: grid;
    place-items: center;
}
table{
	border:1px solid #000;
#width:300px;
text-align:left;
}
.tag_list{
	width:100px;
}
.tag{
	width:250px;
}
td{
	border:1px solid #000;
}
</style>
