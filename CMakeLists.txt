#
# Copyright (c) 2026 Samsung Electronics Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

CMAKE_MINIMUM_REQUIRED(VERSION 3.10)
PROJECT(tizenclaw-skill-plugin-sample)

# RPK app directory
SET(RPK_APP_DIR /usr/apps/org.tizen.tizenclaw-skill-plugin-sample)

# Build native C++ skill binary
ADD_EXECUTABLE(get_sample_load_native
  lib/get_sample_load_native/main.cc
)

# Install Python skills
INSTALL(DIRECTORY lib/get_sample_info/
    DESTINATION ${RPK_APP_DIR}/lib/get_sample_info
)
INSTALL(DIRECTORY lib/get_sample_status/
    DESTINATION ${RPK_APP_DIR}/lib/get_sample_status
)

# Install Node.js skill
INSTALL(DIRECTORY lib/get_sample_time_node/
    DESTINATION ${RPK_APP_DIR}/lib/get_sample_time_node
)

# Install Native C++ skill (manifest + binary)
INSTALL(FILES lib/get_sample_load_native/manifest.json
    DESTINATION ${RPK_APP_DIR}/lib/get_sample_load_native
)
INSTALL(TARGETS get_sample_load_native
    DESTINATION ${RPK_APP_DIR}/lib/get_sample_load_native
)
