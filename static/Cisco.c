Building> enable
# configure terminal

(config)# interface GigabitEthernet 0/0
(config-if)# ip address 10.11.48.97 255.255.255.240
(config-if)# no shutdown

(config)# interface GigabitEthernet 0/1
(config-if)# ip address 10.11.48.85 255.255.255.224
(config-if)# no shutdown


ASN-3> enable
# configure terminal

(config)# interface vlan 1
(config-if)# ip address 10.11.48.114 255.255.255.248
(config-if)# exit

(config)# ip default-gateway 10.11.48.113

(config)# interface vlan 1
(config-if)# no shutdown


IP Address      : 10.11.48.62
Subnet Mask     : 255.255.255.192
Default Gateway : 10.11.48.1