<?php

error_reporting(E_ERROR);
ini_set("display_errors","Off");

require_once "pdo.php";

$dbInfo = new stdClass();
$dbInfo->ip = '127.0.0.1';
$dbInfo->user = 'root';
$dbInfo->password = 'root';
$dbInfo->db = 'steamdb';
$dbInfo->port = 3306;
$dbInfo->config = "mysql:host=$dbInfo->ip;dbname=$dbInfo->db";

$result = query($dbInfo, "select * FROM freegame; SELECT * FROM asf LIMIT 1;", []);
if ($result == -1 || $result == -2) {
    echo "failed to connect to DB";
    return;
}
$freeGame = [];
$asf = [];
if (is_object($result[0])) {
    $freeGame = $result;
} else {
    $freeGame = $result[0];
    $asf = $result[1];
}
?>
<html lang="en">
<head>
    <title>Steam Free Game List</title>
    <meta charset="utf-8"/>
    <style>
        * {
            margin: 0;
            padding: 0;
        }

        .container {
            left: 0;
            right: 0;
            margin: 0 auto;
            width: 570px;
        }

        .border {
            width: 100%;
            border: 1px solid #808080;
        }

        td, th {
            padding: 3px 2px 3px 2px;
            text-align: center;
        }

        a {
            color: black;
            text-decoration: none;
        }

        .asf {
            width: 90%;
            border: 2px solid #808080;
            left: 0;
            right: 0;
            margin: 50px auto 0 auto;
            min-height: 50px;
        }

        .asf > p {
            min-height: 40px;
            padding: 5px;
            width: 100%;
            font-size: 14px;
            text-align: left;
        }
    </style>
</head>
<body>
<div class="container">
    <h1 style="text-align: center; margin: 20px 0;">Steam Free Game List</h1>
    <table border="1" cellspacing="0" class="border">
        <tr>
            <th>Game</th>
            <th>Sub Number</th>
        </tr>
        <?php
        for ($i = 0, $j = count($freeGame); $i < $j; $i++) {
            echo "<tr>
                    <td><a target=\"_blank\" href=\"" . $freeGame[$i]->steam_link . "\">" . $freeGame[$i]->game_name . "</a></td>
                    <td>" . $freeGame[$i]->sub_id . "</td>
                    </tr>";
        }
        ?>
    </table>
    <?php
    if ($asf[0]->display == "1") {
        echo "<div class=\"asf\">" .
            "<p>" . $asf[0]->command . "</p>" .
            "</div>";
    }
    ?>
</div>
</body>
</html>