#! /usr/bin/env sh
uvicorn main:app & node web/dist/server/entry.mjs