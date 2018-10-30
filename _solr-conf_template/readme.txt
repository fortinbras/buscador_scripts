

# Subir configuracao:
 /opt/solr-6.6.2/bin/solr zk -n <collection>  -upconfig -z 192.168.0.35:2181 -d  ./ 

# Criar collection
curl -XGET
'http://localhost:8983/solr/admin/collections?action=CREATE&name=<collection>&numShards=4&replicationFactor=2&maxShardsPerNode=1&collection.configName=<collection_conf> '

