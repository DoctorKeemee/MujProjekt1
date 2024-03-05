<?php
header('Content-Type: application/json; charset=utf-8');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405); // Method Not Allowed
    $response = array('message' => "Invalid request method.");
    echo json_encode($response);
    exit();
}

$file_content = file_get_contents('php://input');
$data = json_decode($file_content);

if ($data == null){
    http_response_code(400); // Bad Request
    $response = array('message' => "Bad request.(empty data)");
    echo json_encode($response);
    exit();
}

if (!isset($data->word)) {
    http_response_code(400); // Bad Request
    $response = array('message' => "Bad request.(missing word)");
    echo json_encode($response);
    exit();
}
if (!isset($data->definition)) {
    http_response_code(400); // Bad Request
    $response = array('message' => "Bad request.(missing definition)");
    echo json_encode($response);
    exit();
}

$definition = htmlspecialchars($data->definition);
$word = htmlspecialchars($data->word);

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

$sql = "INSERT INTO Words (word, definition) VALUES ('".$word."','".$definition."');";
$result = $conn->query($sql);

// Check for success or failure
if ($result) {
    $response = array('message' => "Insert successful.");
} else {
    $response = array('message' => "No rows inserted.");
}

// Respond with the result
echo json_encode($response);

$conn->close();
?>