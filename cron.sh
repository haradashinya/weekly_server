
curl -X POST \
	-H "X-Parse-Application-Id: 7PSeQSEFDqZ3ekegLUspyBXcK0IprmJJEliPYzAi"\
	-H "X-Parse-REST-API-Key: RfavVzrrkFA8cPFdl0EDMn55KVBNd1HXWbAKDvZq"\
	-H "Content-Type: application/json" \
	-d '{
		"where": {
			"channels":"",
			"deviceType":"ios"
		},
		"data": {
			"alert":"affff."
		}
	}'\
		https://api.parse.com/1/push
