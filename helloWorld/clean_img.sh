 for x in $( docker images | grep 'harbor.test.101.com/edbox_qa' | awk '{print $1}'| awk -F '/' '{print $3}' ) ;
    do echo  echo harbor.test.101.com/edbox_qa$x:1.00 ;
 done