from typing import TYPE_CHECKING

from anypoint.models.environment import Environment

if TYPE_CHECKING:
    from anypoint.api.organization import OrganizationApi


class Organization:
    def __init__(self, raw_json, client: "OrganizationApi"):
        self.id: str = raw_json.get("id")
        self.name: str = raw_json.get("name")
        self.owner_id: str = raw_json.get("ownerId")
        self.created_at: str = raw_json.get("createdAt")
        self.updated_at: str = raw_json.get("updatedAt")
        self.is_federated: bool = raw_json.get("isFederated")
        self.org_type: str = raw_json.get("orgType")
        self.domain: str = raw_json.get("domain")
        self.is_root: bool = raw_json.get("isRoot")
        self.is_master: bool = raw_json.get("isMaster")
        self.mfa_required: str = raw_json.get("mfaRequired")
        self.entitlements: Entitlements = Entitlements(raw_json.get("entitlements", {}))

        self._data = raw_json
        self._api_client = client

        usage = raw_json.get("usage", {})
        self.standard_connectors = usage.get("standardConnectors", 0)
        self.premium_connectors = usage.get("premiumConnectors", 0)
        self.production_applications = usage.get("productionApplications", 0)
        self.sandbox_applications = usage.get("sandboxApplications", 0)
        self.design_applications = usage.get("designApplications", 0)
        self.production_workers = usage.get("productionWorkers", 0)
        self.sandbox_workers = usage.get("sandboxWorkers", 0)
        self.design_workers = usage.get("designWorkers", 0)
        self.static_ips = usage.get("staticIps", 0)
        self.vpcs = usage.get("vpcs", 0)
        self.vpns = usage.get("vpns", 0)
        self.network_connections = usage.get("networkConnections", 0)
        self.load_balancers = usage.get("loadbalancers", 0)
        self.load_balancer_workers = usage.get("loadbalancerWorkers", 0)
        self.deployment_groups = usage.get("deploymentGroups", 0)

    def get_environments(self) -> list[Environment]:
        return list(self._api_client.get_environments(self.id))

    def get_private_spaces(self):
        return self._api_client.get_private_spaces(self.id)


class Entitlements:
    def __init__(self, raw_json: dict):
        self.create_environments: bool = raw_json.get("createEnvironments")
        self.global_deployment: bool = raw_json.get("globalDeployment")
        self.create_sub_orgs: bool = raw_json.get("createSubOrgs")
        self.hybrid: dict = raw_json.get("hybrid", {})
        self.hybrid_insight: bool = raw_json.get("hybridInsight")
        self.hybrid_auto_discover_properties: bool = raw_json.get("hybridAutoDiscoverProperties")
        self.v_cores_production: dict = raw_json.get("vCoresProduction", {})
        self.v_cores_sandbox: dict = raw_json.get("vCoresSandbox", {})
        self.v_cores_design: dict = raw_json.get("vCoresDesign", {})
        self.static_ips: dict = raw_json.get("staticIps", {})
        self.vpcs: dict = raw_json.get("vpcs", {})
        self.vpns: dict = raw_json.get("vpns", {})
        self.network_connections: dict = raw_json.get("networkConnections", {})
        self.worker_logging_override: dict = raw_json.get("workerLoggingOverride", {})
        self.mq_messages: dict = raw_json.get("mqMessages", {})
        self.mq_requests: dict = raw_json.get("mqRequests", {})
        self.object_store_request_units: dict = raw_json.get("objectStoreRequestUnits", {})
        self.object_store_keys: dict = raw_json.get("objectStoreKeys", {})
        self.mq_advanced_features: dict = raw_json.get("mqAdvancedFeatures", {})
        self.gateways: dict = raw_json.get("gateways", {})
        self.design_center: dict = raw_json.get("designCenter", {})
        self.partners_production: dict = raw_json.get("partnersProduction", {})
        self.partners_sandbox: dict = raw_json.get("partnersSandbox", {})
        self.trading_partners_production: dict = raw_json.get("tradingPartnersProduction", {})
        self.trading_partners_sandbox: dict = raw_json.get("tradingPartnersSandbox", {})
        self.load_balancer: dict = raw_json.get("loadBalancer", {})
        self.external_identity: bool = raw_json.get("externalIdentity", {})
        self.autoscaling: bool = raw_json.get("autoscaling", {})
        self.arm_alerts: bool = raw_json.get("armAlerts", {})
        self.apis: dict = raw_json.get("apis", {})
        self.api_monitoring: dict = raw_json.get("apiMonitoring", {})
        self.api_community_manager: dict = raw_json.get("apiCommunityManager", {})
        self.api_experience_hub: dict = raw_json.get("apiExperienceHub", {})
        self.monitoring_center: dict = raw_json.get("monitoringCenter", {})
        self.api_query: dict = raw_json.get("apiQuery", {})
        self.api_query_c360: dict = raw_json.get("apiQueryC360", {})
        self.api_governance: dict = raw_json.get("apiGovernance", {})
        self.crowd: dict = raw_json.get("crowd", {})
        self.cam: dict = raw_json.get("cam", {})
        self.exchange2: dict = raw_json.get("exchange2", {})
        self.crowd_self_service_migration: dict = raw_json.get("crowdSelfServiceMigration", {})
        self.kpi_dashboard: dict = raw_json.get("kpiDashboard", {})
        self.pcf: bool = raw_json.get("pcf", {})
        self.app_viz: bool = raw_json.get("appViz", {})
        self.runtime_fabric: bool = raw_json.get("runtimeFabric", {})
        self.anypoint_security_tokenization: dict = raw_json.get("anypointSecurityTokenization", {})
        self.anypoint_security_edge_policies: dict = raw_json.get("anypointSecurityEdgePolicies", {})
        self.runtime_fabric_cloud: dict = raw_json.get("runtimeFabricCloud", {})
        self.service_mesh: dict = raw_json.get("serviceMesh", {})
        self.flex_gateway: dict = raw_json.get("flexGateway", {})
        self.api_catalog: dict = raw_json.get("apiCatalog", {})
        self.composer: dict = raw_json.get("composer", {})
        self.mule_dx_web_ide: dict = raw_json.get("muleDxWebIde", {})
        self.messaging: dict = raw_json.get("messaging", {})
        self.worker_clouds: dict = raw_json.get("workerClouds", {})
