<?php
$servername = "localhost";
$username = "bence";
$password = "benc1e";
$dbname = "db";
$tester = $_POST['id'];
if(!preg_match('/[0-9]+/', $tester)){
	echo "no match";
}else{
$conn = mysqli_connect($servername, $username, $password, $dbname);

if (!$conn) {
	    die("Connection failed: " . mysqli_connect_error());
}

$num = $_POST['id'];

$sql = "DELETE FROM parking WHERE id = $num";

mysqli_query($conn, $sql);

mysqli_close($conn);
}
header ('Location: index.php');

die();
?>
