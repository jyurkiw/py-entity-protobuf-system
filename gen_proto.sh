#!/bin/bash

if [[ $1 = "-t" ]]
then
  protoc @proto/_test_proto_cmd
else
  protoc @proto/_proto_cmd
fi
