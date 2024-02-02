from datetime import datetime, timedelta


def forecast_tool(module_info, module_data):
    if not module_info["commodities"]:
        raise ValueError("Commodities field cannot be empty")

    module_data["commodities"] = {}
    
    for commodity_name, commodity_info in module_info["commodities"].items():
            days_to_subscribe_commodity = commodity_info.get("days_to_subscribe", 0)
            original_end_date = commodity_info.get("endDate")

            new_end_date = calculate_new_end_date(original_end_date, days_to_subscribe_commodity)
            
            module_data["commodities"][commodity_name] = {
                "endDate": new_end_date.strftime("%Y-%m-%d")
            }

def other_tools(module_info, module_data):
    days_to_subscribe_module = module_info.get("days_to_subscribe", 0)
    original_end_date = module_info.get("endDate")

    new_end_date = calculate_new_end_date(original_end_date, days_to_subscribe_module)
    
    module_data["endDate"] = new_end_date.strftime("%Y-%m-%d")

def calculate_new_end_date(original_end_date, days_to_subscribe):
    if original_end_date:
        original_end_date = datetime.strptime(original_end_date, "%Y-%m-%d")
        if original_end_date > datetime.now():
            return original_end_date + timedelta(days=days_to_subscribe)
    
    return datetime.now() + timedelta(days=days_to_subscribe)