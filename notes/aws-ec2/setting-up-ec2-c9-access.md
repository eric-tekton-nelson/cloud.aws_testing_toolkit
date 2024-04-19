# Layout

## VPC

Setup a standard vpc with 2 pub subnets, 2 priv subnets, sgs, rts, and ngw as required.

## Cloud9 

Cloud9 cloudformation template will create a default security group for your c9 env

In:
- Config: HTTP, Port: 80, Source: pub sg that you will use for other test ec2s
- Config: SSH, Port: 20, Source: pub sg that you will use for other test ec2s

## Test EC2s

For testing purposes, just create simple free tier t2.micros, but add them to the security group below.

### create a security group for ec2 prior to creating ec2 instances

- Config: HTTP, Port: 80, Source: from c9 sg
- Config: SSH, Port: 20, Source: from c9 sg
- Config: custom TCP, Port 8181, Source: from c9 sg
- Config: HTTPS, Port 443, Source: all
- Config: All ICMP - IPv4, Port all, Source: from c9 sg
- Config: SSH, Port: 22, Source: local ip address xxx/32

