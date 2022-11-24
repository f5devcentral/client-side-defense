variable "api_cert" {
	type = string
	default = "certificate.cert"
}
        
variable "api_key" {
  	type = string
  	default = "private_key.key"
}

variable "api_url" {
	type = string
	default = "https://treino.console.ves.volterra.io/api"
}

variable "namespace" {
	type = string
	default = "automation-apisec"
}

variable "lbname" {
	type = string
	default = "automation-csd-httpslb"
}

variable "domain" {
	type = string
	default = "automation-csd.f5-hyd-demo.com"
}

variable "originname" {
	type = string
	default = "automation-csd-originpool"	
}

variable "originip" {
	type = string
	default = "3.22.164.153"	
}

variable "originport" {
	type = string
	default = "80"	
}
