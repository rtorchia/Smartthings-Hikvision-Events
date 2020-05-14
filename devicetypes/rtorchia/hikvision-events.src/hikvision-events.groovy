/**
 *  Copyright 2015 SmartThings
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License. You may obtain a copy of the License at:
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 *  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License
 *  for the specific language governing permissions and limitations under the License.
 *
 */
metadata {
	definition (
    	name: "Hikvision Events",
    	namespace: "rtorchia",
        author: "Ralph Torchia"
    )

	{
        capability "Motion Sensor"
		capability "Sensor"
	}

	// UI tile definitions
	tiles(scale: 2) {
		multiAttributeTile(name:"motion", type: "generic", width: 6, height: 4){
			tileAttribute("device.motion", key: "PRIMARY_CONTROL") {
				attributeState("active", label:'motion', icon:"st.motion.motion.active", backgroundColor:"#00A0DC")
				attributeState("inactive", label:'no motion', icon:"st.motion.motion.inactive", backgroundColor:"#CCCCCC")
			}
 		}
		main "motion"
		details "motion"
	}
}

def motionActive() {
	sendEvent(name: "motion",	value: "active")
    runIn(30, motionInactive)
}

def motionInactive() {
	sendEvent(name: "motion", value: "inactive")
}