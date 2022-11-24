resource "volterra_origin_pool" "op-ip-internal" {
  name                   = var.originname
  //Name of the namespace where the origin pool must be deployed
  namespace              = var.namespace
   origin_servers {
    public_ip {
      ip= var.originip
    }
    labels= {}
  }

  no_tls = true
  port = var.originport
  endpoint_selection     = "LOCALPREFERED"
  loadbalancer_algorithm = "LB_OVERRIDE"
}

resource "volterra_http_loadbalancer" "lb-https-tf" {
  depends_on = [volterra_origin_pool.op-ip-internal]
  //Mandatory "Metadata"
  name      = var.lbname
  //Name of the namespace where the origin pool must be deployed
  namespace              = var.namespace
  domains = [var.domain]
  https_auto_cert {
    add_hsts = true
    http_redirect = true
    no_mtls = true
    enable_path_normalize = true
    tls_config {
      default_security = true
      }
  }
  default_route_pools {
      pool {
        name       = var.originname
        namespace  = var.namespace
      }
      weight = 1
    }
  //Mandatory "VIP configuration"
  advertise_on_public_default_vip = true
  //End of mandatory "VIP configuration"
  //Mandatory "Security configuration"
  no_service_policies = true
  client_side_defense  {
    policy {
      js_insert_all_pages = true
    }
  }
  no_challenge = true
  disable_rate_limit = true
  disable_waf = true
  multi_lb_app = true
  user_id_client_ip = true
  source_ip_stickiness = true
}
