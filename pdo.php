<?php
function query($dbInfo, $sql, $param)
{
//    $dbInfo = $GLOBALS['dbInfo'];
    try {
        // 创建PDO对象，最后一个参数尝试使用长连接
        $pdo = new PDO($dbInfo->config, $dbInfo->user, $dbInfo->password, array(PDO::ATTR_PERSISTENT => true));
        // 设置编码格式为utf8mb4
        $pdo->exec('set names utf8mb4;');
    } catch (PDOException $e) {
        // return "{\"error\":\"Database connect error.\"}";
        // -2代表连接失败
        return -2;
    }
    try {
        // 尝试准备sql语句
        $stmt = $pdo->prepare($sql);
    } catch (PDOException $e) {
        // -1代表sql语句无法执行
        return -1;
    }
    // 循环绑定参数
    for ($i = 1, $count = count($param); $i <= $count; $i++) {
        $stmt->bindParam($i, $param[$i - 1]);
    }
    try {
        // 尝试执行sql语句
        $stmt->execute();
    } catch (PDOException $e) {
        // 同执行失败，返回-1
        return -1;
    }
    // 定义一个结果集的数组
    $rowsets = array();
    do {
        // 获取一个结果集
        $rows = $stmt->fetchAll(PDO::FETCH_OBJ);
        if ($rows) {
            // 存在，则存入$rowsets数组
            array_push($rowsets, $rows);
        }
    } while ($stmt->nextRowset());
    $rowcount = $stmt->rowCount();
    if (count($rowsets) == 0 && $rowcount != 0) { // update、delete有行改变，但是没有select结果
        return 1;
    } else if (count($rowsets) != 0) { // 有select结果
        return count($rowsets) == 1 ? $rowsets[0] : $rowsets;
    } else { // update、delete没有行改变，或者select没有结果
        return 0;
    }
}
