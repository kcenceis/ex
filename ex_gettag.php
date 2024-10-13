<?php
require "MySQL.php";
if(is_array($_POST)&&count($_POST)>0)
{
$conn = new PDO("mysql:host=$mysql_host;dbname=$db", $mysql_user, $mysql_password);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$sql=<<<EOF
insert into push (address) value (:address);
EOF;
$stmt = $conn->prepare($sql);
$stmt->bindParam(':address', $_POST['address'], PDO::PARAM_STR);
$stmt->execute();
$conn = null;
}
?>
