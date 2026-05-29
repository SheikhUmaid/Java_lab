set ns [new Simulator]

set tf [open t2a.tr w]
$ns trace-all $tf

set nf [open t2a.nam w]
$ns namtrace-all $nf

proc finish {} {
    global ns nf tf
    $ns flush-trace
    execute nam t2a.nam &
    close $tf
    close $nf
    exit 0
}

set n0 [$ns node]
set n1 [$ns node]

$ns duplex-link $n0 $n1 3Mb 10ms DropTail

set tcp0 [new Agent/TCP]
$ns attach-agent $n0 $tcp0

set sink [new Agent/TCPSink]
$ns attach-agent $n1 $sink

$ns connect $tcp0 $sink

set ftp [new Application/FTP]
$ftp attach-agent $tcp0

$ns at 0.5 "$cbr0 start"
$ns at 4.5 "$cbr0 stop"
$ns at 5.0 "finish"

$ns run