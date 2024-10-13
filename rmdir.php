<?php
require "MySQL.php";
    function deldir($path){
        //如果是目录则继续
        if(is_dir($path)){
            //扫描一个文件夹内的所有文件夹和文件并返回数组
            $p = scandir($path);
            //如果 $p 中有两个以上的元素则说明当前 $path 不为空
            if(count($p)>2){
                foreach($p as $val){
                    //排除目录中的.和..
                    if($val !="." && $val !=".."){
                        //如果是目录则递归子目录，继续操作
                        if(is_dir($path.$val)){
                            //子目录中操作删除文件夹和文件
                            deldir($path.$val.'/');
                        }else{
                            //如果是文件直接删除
                            unlink($path.$val);
                        }
                    }
                }
            }
        }
        
        //删除当前文件夹：
        return rmdir($path);
    }

  $exPath = "ex/Preview/";
  $result = deldir($exPath);
  if($result==1){
    echo "exhentai Preview delete";
  }
$conn = new PDO("mysql:host=$mysql_host;dbname=$db", $mysql_user, $mysql_password);
    // set the PDO error mode to exception
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$conn->exec('TRUNCATE TABLE ex_gd3;');
$conn = null;
$db = 'ex';
$conn = new PDO("mysql:host=$mysql_host;dbname=$db", $mysql_user, $mysql_password);
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$conn->exec("update ex set _delete='1';");
$conn = null;
?>
