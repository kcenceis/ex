<?php
require 'MySQL.php';
        # 删除操作
if(is_array($_GET)&&count($_GET)>0)
{
    if (isset($_GET['id'])){
$conn = new PDO("mysql:host=$mysql_host;dbname=$db", $mysql_user, $mysql_password);
    // set the PDO error mode to exception
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$sql=<<<EOF
delete from title_filter where id=:id;
EOF;
$stmt = $conn->prepare($sql);
$stmt->bindParam(':id', $_GET['id'], PDO::PARAM_STR);
$stmt->execute();
$conn = null;
    }
}

$conn = new PDO("mysql:host=$mysql_host;dbname=$db", $mysql_user, $mysql_password);
    // set the PDO error mode to exception
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$sql=<<<EOF
select * from title_filter;
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
                         echo $row['title'];
                         echo '</td>';
                         echo '<td>';
                         echo '<a href="?id='.$row['id'].'"><button type="button">删除</button></a>';
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
