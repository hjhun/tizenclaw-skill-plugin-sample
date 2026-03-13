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
PROJECT(tizenclaw-skill-plugin-sample LANGUAGES NONE)

# RPK app directory
SET(RPK_APP_DIR /usr/apps/org.tizen.tizenclaw-skill-plugin-sample)

# Install skill directories under lib/
INSTALL(DIRECTORY lib/get_sample_info/
    DESTINATION ${RPK_APP_DIR}/lib/get_sample_info
)
INSTALL(DIRECTORY lib/get_sample_status/
    DESTINATION ${RPK_APP_DIR}/lib/get_sample_status
)
