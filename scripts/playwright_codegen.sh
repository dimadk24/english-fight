#!/usr/bin/env bash

FRONTEND_URL="http://localhost:3000/english-fight?fake_vk_id=374637778"

playwright codegen "$FRONTEND_URL"
