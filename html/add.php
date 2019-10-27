<?php
$servername = "localhost";
$username = "bence";
$password = "benc1e";
$dbname = "db";

$conn = mysqli_connect($servername, $username, $password, $dbname);

if (!$conn) {
	    die("Connection failed: " . mysqli_connect_error());
}

$num = $_POST['cardnumber'];

$sql = "INSERT INTO parking (cardnumber) VALUES ('$num')";

mysqli_query($conn, $sql);

mysqli_close($conn);

header ('Location: index.php');

die();
?>
