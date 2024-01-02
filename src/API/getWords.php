<?php
header('Content-Type: application/json; charset=utf-8');
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

$sql = 'SELECT * FROM Words WHERE Explained = 0;';
$result = $conn->query($sql);

$response = [];

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $response[] = [
            "Word" => $row["Word"],
            "Definition" => $row["Definition"],
            "Level" => $row["Level"],
            "Explained" => $row["Explained"]
        ];
    }
} else {
    $response[] = ["message" => "No results"];
}

echo json_encode($response, JSON_PRETTY_PRINT);

$conn->close();
?>