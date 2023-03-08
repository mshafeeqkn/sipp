#!/bin/bash

LAN_CERT=dev_10.1.12.1.crt
LAN_KEY=dev_10.1.12.1.key
WAN_CERT=dev_172.17.12.1.crt
WAN_KEY=dev_172.17.12.1.key

DEV_WAN=172.17.1.14
DEV_LAN=10.1.1.14
TEST_LAN=10.1.12.1
TEST_WAN=172.17.12.1

SIPP=sipp-3.3
SIPP_LAN="${SIPP} -i ${TEST_LAN} -p 10001 ${DEV_LAN}"
SIPP_WAN="${SIPP} -i ${TEST_WAN} -p 5055 ${DEV_WAN}"
TLS_LAN="-t ln -tls_cert ${LAN_CERT} -tls_key ${LAN_KEY}"
TLS_WAN="-t ln -tls_cert ${WAN_CERT} -tls_key ${WAN_KEY}"

# mandctl client sip add 981001 ${TEST_LAN} 10001 2
# mandctl client sip add 982001 ${TEST_LAN} 10001 0

function test_lo_wan_srtp_to_lan_srtp() {
    # WAN(TLS/SRTP) - LAN(TLS/SRTP)
    ${SIPP_LAN}:5061 -sf uas_srtp_late_offer.xml -inf user_tls_1.csv ${TLS_LAN} -m 1 -bg
    ${SIPP_WAN}:5061 -sf uac_srtp_late_offer.xml -inf user_tls_1.csv ${TLS_WAN} -m 1
}

function test_lo_wan_rtp_to_lan_srtp() {
    # WAN(UDP/RTP)  - LAN(TLS/SRTP)
    ${SIPP_LAN}:5061 -sf uas_srtp_late_offer.xml -inf user_tls_1.csv ${TLS_LAN} -m 1 -bg
    ${SIPP_WAN}:5060 -sf uac_rtp_late_offer.xml -inf user_tls_1.csv -m 1
}

function test_lo_wan_srtp_to_lan_rtp() {
    # WAN(TLS/SRTP) - LAN(UDP/RTP)
    ${SIPP_LAN}:5060 -sf uas_rtp_late_offer.xml -inf user_udp_1.csv -m 1 -bg
    ${SIPP_WAN}:5061 -sf uac_srtp_late_offer.xml -inf user_udp_1.csv ${TLS_WAN} -m 1
}

function test_lo_wan_rtp_to_lan_rtp() {
    # WAN(UDP/RTP)  - LAN(UDP/RTP)
    ${SIPP_LAN}:5060 -sf uas_rtp_late_offer.xml -inf user_udp_1.csv -m 1 -bg
    ${SIPP_WAN}:5060 -sf uac_rtp_late_offer.xml -inf user_udp_1.csv -m 1
}

function test_lo_lan_srtp_to_wan_srtp() {
    # LAN(TLS/SRTP) - WAN(TLS/SRTP)
    ${SIPP_WAN}:5061 -sf uas_srtp_late_offer.xml -inf user_tls_2.csv ${TLS_WAN} -m 1 -bg
    ${SIPP_LAN}:5061 -sf uac_srtp_late_offer.xml -inf user_tls_2.csv ${TLS_LAN} -m 1
}

function test_lo_lan_rtp_to_wan_srtp() {
    # LAN(UDP/RTP)  - WAN(TLS/SRTP)
    ${SIPP_WAN}:5061 -sf uas_srtp_late_offer.xml -inf user_udp_2.csv ${TLS_WAN} -m 1 -bg
    ${SIPP_LAN}:5060 -sf uac_rtp_late_offer.xml -inf user_udp_2.csv -m 1
}

function test_lo_lan_srtp_to_wan_rtp() {
    # LAN(TLS/SRTP) - WAN(UDP/RTP)
    ${SIPP_WAN}:5060 -sf uas_rtp_late_offer.xml -inf user_tls_2.csv -m 1 -bg
    ${SIPP_LAN}:5061 -sf uac_srtp_late_offer.xml -inf user_tls_2.csv ${TLS_LAN} -m 1
}

function test_lo_lan_rtp_to_wan_rtp() {
    # LAN(UDP/RTP)  - WAN(UDP/RTP)
    ${SIPP_WAN}:5060 -sf uas_rtp_late_offer.xml -inf user_udp_2.csv -m 1 -bg
    ${SIPP_LAN}:5060 -sf uac_rtp_late_offer.xml -inf user_udp_2.csv -m 1
}

function test_nc_lan_srtp_to_wan_rtp() {
    ${SIPP_WAN}:5060 -sf uas_rtp_normal_call.xml -inf user_tls_2.csv -m 1 -bg
    ${SIPP_LAN}:5061 -sf uac_srtp_normal_call.xml -inf user_tls_2.csv ${TLS_LAN} -m 1
}

function test_nc_wan_rtp_to_lan_srtp() {
    ${SIPP_LAN}:5061 -sf uas_srtp_normal_call.xml -inf user_tls_1.csv -m 1 ${TLS_LAN} -bg
    ${SIPP_WAN}:5060 -sf uac_rtp_normal_call.xml -inf user_tls_1.csv -m 1
}

test_lo_wan_rtp_to_lan_srtp
# test_nc_lan_srtp_to_wan_rtp
# test_nc_wan_rtp_to_lan_srtp
