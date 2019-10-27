<?php
$con=mysqli_connect("localhost","bence","benc1e","db");

 if (mysqli_connect_errno())
 {
 echo "Failed to connect to MySQL: " . mysqli_connect_error();
 }

 $result = mysqli_query($con,"SELECT * FROM parking");

 echo "<table class='zui-table'>
<thead>
 <tr>
 <th>ID</th>
 <th>Card Number</th>
 </tr></thead><tbody>";

 while($row = mysqli_fetch_array($result))
 {
 echo "<tr>";
 echo "<td>" . $row['id'] . "</td>";
 echo "<td>" . $row['cardnumber'] . "</td>";
 echo "</tr></tbody>";
 }
 echo "</table>";

 mysqli_close($con);
 ?>
