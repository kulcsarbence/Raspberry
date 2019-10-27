<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="main.css">
</head>
<body>
<h2>Accepted cards</h2>
<?php include ('prog.php'); ?>
<h2>Currently parked cards</h2>
<?php include ('prog2.php'); ?>
<h3>Add Card Number Separated By Commas</h3>
<form action="add.php" method="POST">
    <input type="text" name="cardnumber" id="cardnumber" value=""><br>
    <input type="submit">
</form>
<h3>Delete Card By ID</h3>
<form action="delete.php" method="POST">
    <input type="text" name="id" id="id" value=""><br>
    <input type="submit">
</form>
</body>
</html>
