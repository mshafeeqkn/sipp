## SIPp
This repository contains xml and csv files for SIPp calls

## Requirement
SIPp 3.4 or higher version is required for these xmls. The scenario files contain rtp_stream attribute to play the audio in .wav format.

## XML
The following scenarios are implemented
### basic-call
Basic call scenario
`WAN client(UAC) -> SBC WAN Interface -> SBC LAN Interface -> LAN Client(UAS)`

### call-hold-uac
Call hold from UAC
`WAN client(UAC) -> SBC WAN Interface -> SBC LAN Interface -> LAN Client(UAS)`

### lan-lan-call (WIP)
SBC will have two local clients and SIP server is deployed on the WAN side. The call flow will be like

`LAN client 1 -> SBC LAN Interface -> SBC WAN Interface -> SIP server -> SBC WAN Interface -> SBC LAN Interface -> LAN Client 2`

Here the XML files are implemented for LAN Client 1, LAN client 2 and SIP server

### register
Register a SIP client from LAN side of Edgemarc. Receive the REGISTER message from WAN side and respond with Success message
`LAN client(UAC) -> SBC LAN Interface -> SBC WAN Interface -> WAN Client(UAS)`

### transfer
This is for unattended transfer. The XML implemented for Transferer, Transferee and Target. It's assumed that, the REFER initated INVITE will be handled by the SBC and Transferee won't hold the call before call transfer.

`Transferee -> SBC LAN -> SBC WAN -> Transferer -> SBC WAN -> SBC LAN -> Target`

### Call replace
The 3PCC is employed to implement the call replace. The LAN client will be calling the WAN client, the WAN client will send a new INVITE with with `replaces` header and the call dialog will be replaced at WAN side

`LAN client -> SBC LAN -> SBC WAN -> (WAN client 1 & 2)`
