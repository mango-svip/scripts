var body = $response.body.replace(/isfree":0/g, 'isfree":1')
$done({ body })