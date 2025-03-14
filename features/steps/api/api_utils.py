

def raise_http_error(response):
    status_code = response.status_code
    message = response.text
    request = response.request
    request_msg = "\n-url: {}\n-headers: {},\n-body: {}".format(request.url,
                                                                request.headers,
                                                                request.body)
    response_msg = "\n-code: {},\n-text: {}".format(status_code, message)
    raise Exception("\nREQUEST: {}\n\nRESPONSE: {}".format(request_msg, response_msg))
