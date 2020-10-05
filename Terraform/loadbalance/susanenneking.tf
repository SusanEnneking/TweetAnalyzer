resource "digitalocean_domain" "default" {
   name = "susanenneking.dev"
   ip_address = digitalocean_loadbalancer.www-lb.ip
}
resource "digitalocean_record" "CNAME-www" {
  domain = digitalocean_domain.default.name
  type = "CNAME"
  name = "www"
  value = "@"
}
