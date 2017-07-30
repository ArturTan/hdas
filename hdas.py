#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import Hermes
import time
start = Hermes.Hermes()
if start.settings():
    time.sleep(120)
    start.send()
