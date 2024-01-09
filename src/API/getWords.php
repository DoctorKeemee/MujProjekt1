<?php
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST'){
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

if (!isset($data->email)) {
    http_response_code(400); // Bad Request
    $response = array('message' => "Bad request.(missing email)");
    echo json_encode($response);
    exit();
}

$email = $data->email;

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

$sql = "SELECT Word, Definition, Level, Explained FROM Users JOIN WordsToUsers ON Users.ID = WordsToUsers.IDUser JOIN Words ON WordsToUsers.IDWord = Words.ID WHERE Explained = 0 and Users.email = '".$email."';";
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