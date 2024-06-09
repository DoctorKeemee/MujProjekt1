<?php
$servername = "sql5.webzdarma.cz";
$username = "smartwordsbo0363";
$password = '$ev&i12IOz%3M0_3&eh.';
$dbname = "smartwordsbo0363";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
$conn->set_charset("utf8");



// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT * FROM `Words`";
$result = $conn->query($sql);
echo "<head>";
echo '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">';
echo '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>';
echo "<head>";
echo '<body><table class="table table-primary table-striped">';

echo "<tr>";

    echo'<th scope="col">Word</th>
    <th scope="col">Definition</th>';
echo "<tr>";

while ($row = $result->fetch_assoc()) {

echo "<tr>";
   echo "<td>";
   echo $row["Word"];
   echo "</td>";
   echo "<td>";
   echo $row["Definition"];
   echo "</td>";
echo "<tr>";}

echo "</table></body>";
?>