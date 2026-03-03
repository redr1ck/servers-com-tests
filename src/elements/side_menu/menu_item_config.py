"""Menu item configuration classes."""
from typing import Dict, List, Optional


class MenuItemConfig:
    """Menu item configuration."""

    def __init__(
        self,
        name: str,
        url_pattern: str,
        has_submenu: bool,
        submenu_items: Optional[List[str]] = None
    ):
        self.name = name
        self.url_pattern = url_pattern
        self.has_submenu = has_submenu
        self.submenu_items = submenu_items or []


# All main menu items configuration
MENU_ITEMS: Dict[str, MenuItemConfig] = {
    # Direct navigation items
    'scalable_bare_metal': MenuItemConfig('Scalable Bare Metal', '/sbm', False),
    'ai_compute': MenuItemConfig('AI compute', '/ai-compute', False),
    'cloud_storage': MenuItemConfig('Cloud Storage', '/cloud-storage', False),
    'managed_kubernetes': MenuItemConfig('Managed Kubernetes', '/k8s', False),
    'load_balancers': MenuItemConfig('Load Balancers', '/lb', False),
    'firewalls': MenuItemConfig('Firewalls', '/firewalls', False),
    'private_racks': MenuItemConfig('Private Racks', '/private-racks', False),
    'ssl_certificates': MenuItemConfig('SSL certificates', '/ssl', False),
    'account_settings': MenuItemConfig('Account settings', '/account', False),
    'requests': MenuItemConfig('Requests', '/requests', False),

    # Submenu only items
    'enterprise_bare_metal': MenuItemConfig('Enterprise Bare Metal', '/enterprise', True),
    'cloud_servers': MenuItemConfig('Cloud Servers', '/cloud/servers', True),
    'networks': MenuItemConfig('Networks', '/networks', True),
    'monitoring': MenuItemConfig('Monitoring', '/monitoring', True),
    'identity_and_access': MenuItemConfig('Identity and Access', '/iam', True),
    'billing': MenuItemConfig('Billing', '/billing', True),
    'reports': MenuItemConfig('Reports', '/reports', True),
}

