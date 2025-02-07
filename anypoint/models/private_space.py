from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from anypoint import Anypoint


class VPNTunnel:
    def __init__(self, raw_json):
        self.accepted_route_count: int = raw_json.get("acceptedRouteCount")
        self.ike_versions = raw_json.get("ikeVersions", [])
        self.last_status_change: str = raw_json.get("lastStatusChange")
        self.local_external_ip_address: str = raw_json.get("localExternalIpAddress")
        self.local_ptp_ip_address: str = raw_json.get("localPtpIpAddress")
        self.phase1_dh_groups = raw_json.get("phase1DhGroups", [])
        self.phase1_encryption_algorithms = raw_json.get("phase1EncryptionAlgorithms", [])
        self.phase1_integrity_algorithms = raw_json.get("phase1IntegrityAlgorithms", [])
        self.phase2_dh_groups = raw_json.get("phase2DhGroups", [])
        self.phase2_encryption_algorithms = raw_json.get("phase2EncryptionAlgorithms", [])
        self.phase2_integrity_algorithms = raw_json.get("phase2IntegrityAlgorithms", [])
        self.psk: str = raw_json.get("psk")
        self.rekey_fuzz: int = raw_json.get("rekeyFuzz")
        self.rekey_margin_in_seconds: int = raw_json.get("rekeyMarginInSeconds")
        self.remote_ptp_ip_address: str = raw_json.get("remotePtpIpAddress")
        self.startup_action: str = raw_json.get("startupAction")
        self.status: str = raw_json.get("status")
        self.status_message: str = raw_json.get("statusMessage")
        self.vpn_connection_id: str = raw_json.get("vpnConnectionId")

        self._data = raw_json


class VPN:
    def __init__(self, raw_json):
        self.connection_id: str = raw_json.get("connectionId")
        self.connection_name: str = raw_json.get("connectionName")
        self.local_asn: int = raw_json.get("localAsn")
        self.name: str = raw_json.get("name")
        self.remote_asn: int = raw_json.get("remoteAsn")
        self.remote_ip_address: str = raw_json.get("remoteIpAddress")
        self.vpn_connection_status: str = raw_json.get("vpnConnectionStatus")
        self.vpn_id: str = raw_json.get("vpnId")
        self.vpn_tunnels = [VPNTunnel(tunnel) for tunnel in raw_json.get("vpnTunnels", [])]

        self._data = raw_json


class Connection:
    def __init__(self, raw_json):
        self.id: str = raw_json.get("id")
        self.name: str = raw_json.get("name")
        self.vpns = [VPN(vpn) for vpn in raw_json.get("vpns", [])]

        self._data = raw_json


class PrivateSpace:
    def __init__(self, raw_json, client: "Anypoint"):
        self.id: str = raw_json.get("id")
        self.name: str = raw_json.get("name")
        self.organization_id: str = raw_json.get("organizationId")
        self.region: str = raw_json.get("region")
        self.root_organization_id: str = raw_json.get("rootOrganizationId")
        self.status: str = raw_json.get("status")

        self._data = raw_json
        self._client = client

    def get_connections(self) -> list[Connection]:
        return self._client.organizations.get_private_space_connections(self.organization_id, self.id)
