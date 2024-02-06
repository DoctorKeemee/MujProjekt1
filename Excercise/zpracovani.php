<?php
if ($_SERVER['REQUEST_METHOD'] !== 'GET'){
    http_response_code(405); // Method Not Allowed
    $response = array('message' => "Invalid request method.");
    echo json_encode($response);
    exit();
    }

?>
<!DOCTYPE html>
 <html lang="en">
 <head>
     <meta charset="UTF-8">
     <meta http-equiv="X-UA-Compatible" content="IE=edge">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>Welcome Page</title>
     <style>
         html, body {
             height: 100%;
             margin: 0;
             padding: 0;
             display: flex;
             align-items: center;
             justify-content: center;
             font-family: Arial, sans-serif;
             background-color: #f4f4f4;
         }

         .container {
             text-align: left;
             max-width: 400px; /* Adjust the width as needed */
             width: 100%;
             background-color: #fff;
             padding: 20px;
             border-radius: 8px;
             box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
         }

         h1 {
             color: #333;
         }

         p {
             margin: 10px 0;
             color: #666;
         }
     </style>
 </head>
 <body>
     <div class="container">
         <h1>Welcome!</h1>

         <?php
         if (isset($_GET['fname'], $_GET['lname'], $_GET['gender'], $_GET['age'], $_GET['birthday'])) {
             $fname = htmlspecialchars($_GET['fname']);
             $lname = htmlspecialchars($_GET['lname']);
             $gender = htmlspecialchars($_GET['gender']);
             $age = htmlspecialchars($_GET['age']);
             $birthday = htmlspecialchars($_GET['birthday']);

             echo "<p>Hello $fname $lname!</p>";
             echo "<p>Gender: $gender</p>";
             echo "<p>Age: $age</p>";
             echo "<p>Birthday: $birthday</p>";
         } else {
             echo "<p>Error: All parameters (fname, lname, gender, age, birthday) are required.</p>";
         }
         ?>
     </div>
 </body>
 </html>


