<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="main.css">
<meta charset="utf-8">
</head>
<body>
<h1>Parking Support</h2>
<hr></hr>
<h2>Accepted cards</h2>
<img src="bg2.jpg" align="left">
<img src="bg2.jpg" align="right">
<?php include ('prog.php'); ?>
<h2>Currently parked cards</h2>
<?php include ('prog2.php'); ?>
<h3>Add Card Number Separated By Commas</h3>
<form action="add.php" method="POST">
    <input type="text" name="cardnumber" pattern="[0-9]{1,3}[,][0-9]{1,3}[,][0-9]{1,3}[,][0-9]{1,3}[,][0-9]{1,3}" id="cardnumber" value=""><br>
    <input type="submit">
</form>
<h3>Delete Card By ID</h3>
<form action="delete.php" method="POST">
    <input type="text" name="id" id="id" pattern="[0-9]{1,}" value=""><br>
    <input type="submit">
</form>

</body>
</html>
