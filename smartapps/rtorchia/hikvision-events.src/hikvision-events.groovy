/**
 *  Hikvision Events
 *
 *  Copyright 2019 Ralph Torchia
 *  Modified code from "HikvisionMotion" by Adrian Caramaliu
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
definition (
    name: "Hikvision Events",
    namespace: "rtorchia",
    author: "Ralph Torchia",
    description: "Notification for events from Hikvision NVRs",
    category: "Safety & Security",
    iconUrl: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience.png",
    iconX2Url: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience@2x.png",
    iconX3Url: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience@2x.png"
)


preferences {
	section("Hikvison Events") {
		// TODO: put inputs here
	}
}

def installed() {
	initialize()
}

def updated() {
	unsubscribe()
	initialize()
}

def initialize() {
	initializeEndpoint()
	// TODO: subscribe to attributes, devices, locations, etc.
}

private Integer convertHexToInt(hex) {
	Integer.parseInt(hex,16)
}

private String convertHexToIP(hex) {
	[convertHexToInt(hex[0..1]),convertHexToInt(hex[2..3]),convertHexToInt(hex[4..5]),convertHexToInt(hex[6..7])].join(".")
}

private initializeEndpoint() {
	try {
        if (!state.endpoint) {
            try {
                def accessToken = createAccessToken()
                if (accessToken) {
                    state.endpoint = apiServerUrl("/api/token/${accessToken}/smartapps/installations/${app.id}/")
                }
            } catch(e) {
                state.endpoint = null
            }
        }
        //log.trace "Endpoint is $state.endpoint"
        return state.endpoint
	} catch (all) {
    	error "An error has occurred during endpoint initialization: ", all
    }
    return false
}

/***********************************************************************/
/*                      EXTERNAL EVENT MAPPINGS                        */
/***********************************************************************/
mappings {
    path("/event") {
        action: [
            PUT: "processEvent"
        ]
    }
}

/***********************************************************************/
/*                      EXTERNAL EVENT HANDLERS                        */
/***********************************************************************/
private processEvent(event) {
    def data = request?.JSON?:[:]
    def eventType = data?.eventType
    def eventTime = data?.eventTime
    def cameraName = data?.cameraName
    def channelName = data?.channelName
    if (!eventType || !cameraName || !channelName) return
    def deviceDNI = (app.id + '-' + channelName + '-' + eventType.toLowerCase().replaceAll(' ', '-')).toLowerCase();
    def device = getChildDevice(deviceDNI)
    def deviceName = "$cameraName $eventType Sensor".split()*.capitalize().join(" ")
    if(!device) device = addChildDevice("rtorchia", "Hikvision Events", deviceDNI, null, [label: deviceName])
    if (device) device.motionActive()
}