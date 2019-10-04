#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###
### Web-UI > Backend > Serializers
###
from flask_restplus import fields

from lib.db.Service import Protocol
from lib.webui.api.Api import api


class ProtocolString(fields.Raw):
    def format(self, value):
        return { 
            'Protocol.TCP': 'tcp',
            'Protocol.UDP': 'udp'
        }.get(value, 'tcp')



mission = api.model('Mission', {
    'id': fields.Integer(readonly=True, description='The mission unique identifier'),
    'name': fields.String(required=True, description='Mission name'),
    'comment': fields.String(description='Mission comment'),
    'creation_date': fields.DateTime(description='Creation datetime of the mission'),
    'services_count': fields.Integer(description='Number of services in the mission'),
})

host = api.model('Host', {
    'id': fields.Integer(readonly=True, description='The host unique identifier'),
    'ip': fields.String(required=True, description='Host IP address'),
    'hostname': fields.String(description='Hostname'),
    'os': fields.String(description='Host OS name'),
    'os_vendor': fields.String(description='Host OS vendor name'),
    'os_family': fields.String(description='Host OS family'),
    'mac': fields.String(description='Host MAC address'),
    'vendor': fields.String(description='Host vendor name'),
    'type': fields.String(description='Host type'),
    'comment': fields.String(description='Host comment'),
    'tcp_count': fields.Integer(description='TCP services count'),
    'udp_count': fields.Integer(description='UDP services count'),
    'creds_count': fields.Integer(description='Credentials (username & password) count'),
    'users_count': fields.Integer(description='Single usernames count'),
    'vulns_count': fields.Integer(description='Vulnerabilities count'),
    'mission_id': fields.Integer(description='Mission identifier'),
})

option = api.model('Product', {
    'id': fields.Integer(readonly=True, description='The option unique identifier'),
    'type': fields.String(description='Product type'),
    'name': fields.String(description='Product name'),
    'version': fields.String(description='Product version'), 
})

service = api.model('Service', {
    'id': fields.Integer(readonly=True, description='The service unique identifier'),
    'name': fields.String(description='Service name'),
    'name_original': fields.String(description='Service original name (as given by Nmap/Shodan'),
    'port': fields.Integer(description='Port number'),
    'protocol': ProtocolString(attribute='protocol', description='Protocol (tcp/udp)', default='tcp', enum=['tcp', 'udp']),
    'encrypted': fields.Boolean(description='Boolean indicating if encrypted protocol (SSL/TLS)', default=False),
    'url': fields.String(description='Target URL (for HTTP(s))'),
    'up': fields.Boolean(description='Status', default=True),
    'banner': fields.String(description='Service banner'),
    'html_title': fields.String(description='HTML title (for HTTP(s))'),
    'web_technos': fields.String(description='Web technologies (for HTTP(s)) (unused)'),
    'comment': fields.String(description='Service comment'),
    'products': fields.List(fields.Nested(option)),
    'creds_count': fields.Integer(description='Credentials (username & password) count'),
    'users_count': fields.Integer(description='Single usernames count'),
    'vulns_count': fields.Integer(description='Vulnerabilities count'),
    'checks_categories': fields.List(fields.String()),
    'host_id': fields.Integer(description='Host identifier'),
    'host_ip': fields.String(description='Host IP address'),
})

mission_with_hosts = api.inherit('Mission with hosts', mission, {
    'hosts': fields.List(fields.Nested(host))
})

host_with_services = api.inherit('Host with services', host, {
    'services': fields.List(fields.Nested(service))
})