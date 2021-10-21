<?php
$file = fopen("test.txt", "a+");
while(!feof($file))
{
    echo fgets($file);
    echo "<br>";
}
fwrite($file, "test", 4);
fclose($file)
?>