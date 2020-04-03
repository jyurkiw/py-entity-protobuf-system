#!/bin/bash

./gen_proto.sh -t
pytest
rm ./*_pb2.py
