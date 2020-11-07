#!/bin/bash

uvicorn --host 0.0.0.0 --port 9000 src."$1":app