<?php
header('Content-Type: application/json; charset=utf-8');
header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header("Access-Control-Allow-Headers: X-Requested-With");

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

if (!isset($data->level)) {
    http_response_code(400); // Bad Request
    $response = array('message' => "Bad request.(missing level)");
    echo json_encode($response);
    exit();
}



if (!is_numeric($data->level) || floor($data->level) != $data->level) {
    http_response_code(400); // Bad Request
    $response = array('message' => "New level must be an integer.");
    echo json_encode($response);
    exit();
}

if (!isset($data->explained)) {
    $data->explained = 1;
}
if (!is_numeric($data->explained) || floor($data->explained) != $data->explained || !($data->explained == 0 || $data->explained == 1)){
        http_response_code(400); // Bad Request
        $response = array('message' => "Explained must be 1 or 0.");
        echo json_encode($response);
        exit();
}

$level = intval($data->level);
$word = htmlspecialchars($data->word);
$explained = intval($data->explained);

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

$sql = "SELECT * FROM Words WHERE Word = '".$word."';";
$result = $conn->query($sql);

if ($result->num_rows == 0) {
    http_response_code(404);
    $response = array('message' => "Word ".$word." wasn't found.");
    echo json_encode($response);
    exit();
}
$sql = "UPDATE WordsToUsers SET Level = ".$level.", Explained = ".$explained."  WHERE IDWord = (SELECT w.ID FROM Words w WHERE w.Word = '".$word."') AND IDUser = (SELECT u.ID FROM Users u WHERE u.email='".$data->email."');";
$result = $conn->query($sql);

// Check for success or failure
if ($result) {
    $response = array('message' => "Update successful.");
} else {
    $response = array('message' => "No rows updated.");
}

// Respond with the result
echo json_encode($response);

$conn->close();
?>