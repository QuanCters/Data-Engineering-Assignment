def format_response(data, message="Success", status=200):
    return {
        "status": status,
        "message": message,
        "data": data
    }, status