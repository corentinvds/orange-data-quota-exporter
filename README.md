# orange-data-quota-exporter
Prometheus exporter to expose current internet quota usage with Orange.be

## Behavior:
1) Login to https://sso.orange.be/auth/sm/login.fcc
2) Extract usage from https://e-services.orange.be/fr/ajax/overview/postpaid_usage_dashboard/MY_NUMBER
3) Export the result as prometheus metrics
