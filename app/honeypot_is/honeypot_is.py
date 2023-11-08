import requests
from datetime import datetime
from fake_headers import Headers


HEADERS = Headers(os="mac", headers=True).generate()


def get_token_pair(token_address, chain_id):
    response = requests.get(
        f"https://api.honeypot.is/v1/GetPairs?address={token_address}&chainID={chain_id}"
    ).json()
    return response[0].get("Pair").get("Address")


def get_holder_analysis(server_response):
    holder_analysis = server_response.get("holderAnalysis")
    return (
        {
            "number_of_holders": holder_analysis.get("holders"),
            "number_of_successful_holders": holder_analysis.get("successful"),
            "average_tax": round(holder_analysis.get("averageTax"), 2),
            "highest_tax": holder_analysis.get("highestTax"),
        }
        if holder_analysis
        else {}
    )


def get_token_taxes(server_response):
    taxes_details = server_response.get("simulationResult")
    return {
        "buy_tax": round(taxes_details.get("buyTax"), 2),
        "sell_tax": round(taxes_details.get("sellTax"), 2),
        "buy_gas": taxes_details.get("buyGas"),
        "sell_gas": taxes_details.get("sellGas"),
    }


def get_pair_details(server_response):
    pair_details = server_response.get("pair")
    return {
        "pair_name": pair_details.get("pair").get("name"),
        "pair_address": pair_details.get("pair").get("address"),
        "pair_type": pair_details.get("pair").get("type"),
        "chain": server_response.get("chain").get("name"),
        "creation_datetime": str(
            datetime.fromtimestamp(int(pair_details.get("createdAtTimestamp")))
        ),
        "liquidity": round(pair_details.get("liquidity"), 4),
    }


def token_is_honeypot(server_response):
    return server_response.get("honeypotResult").get("isHoneypot")


def get_token_data(server_response):
    token_details = server_response.get("token")
    return {
        "name": token_details.get("name"),
        "address": token_details.get("address"),
        "decimals": token_details.get("decimals"),
        "symbol": token_details.get("symbol"),
    }


def get_token_details(token_address, pair_address, chain_id):
    print(
        "Token details:",
        f"https://api.honeypot.is/v2/IsHoneypot?address={token_address}&pair={pair_address}&chainID={chain_id}",
    )
    data = {}
    response = requests.get(
        f"https://api.honeypot.is/v2/IsHoneypot?address={token_address}&pair={pair_address}&chainID={chain_id}",
        headers=HEADERS,
    ).json()

    data["token"] = get_token_data(response)
    data["holders"] = get_holder_analysis(response)
    data["pair"] = get_pair_details(response)
    data["is_honeypot"] = token_is_honeypot(response)
    data["taxes"] = get_token_taxes(response)
    return data
