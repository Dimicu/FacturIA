def throw_json_error(error_message:str , status_code:int):
        return {"error": error_message, "status_code":status_code}