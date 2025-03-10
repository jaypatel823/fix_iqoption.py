import os
import asyncio
import json
import websockets
from iqoptionapi.stable_api import IQ_Option

# ✅ IQ Option Login Credentials (From Environment Variables)
IQ_USERNAME = os.getenv("IQ_USERNAME")
IQ_PASSWORD = os.getenv("IQ_PASSWORD")

if not IQ_USERNAME or not IQ_PASSWORD:
    raise ValueError("❌ ERROR: Please set IQ_USERNAME and IQ_PASSWORD in environment variables!")

# ✅ Connect to IQ Option API
iq = IQ_Option(IQ_USERNAME, IQ_PASSWORD)
iq.connect()

if iq.check_connect():
    print("✅ Successfully connected to IQ Option API")
else:
    raise Exception("❌ Connection failed! Please check your credentials.")

# ✅ WebSocket Server for Live Trading Signals
connected_clients = set()

async def send_signals(websocket, path):
    connected_clients.add(websocket)
    try:
        while True:
            # Example: Fetch Current Balance
            balance = iq.get_balance()
            signal_data = json.dumps({"balance": balance})
            
            # Send signal to all clients
            await asyncio.wait([client.send(signal_data) for client in connected_clients])
            await asyncio.sleep(5)  # Send updates every 5 seconds

    except websockets.exceptions.ConnectionClosed:
        connected_clients.remove(websocket)

# ✅ Start WebSocket Server
async def start_server():
    async with websockets.serve(send_signals, "0.0.0.0", 8000):
        print("🚀 WebSocket Server Running on ws://0.0.0.0:8000")
        await asyncio.Future()  # Keep running

# ✅ Run Server
if __name__ == "__main__":
    asyncio.run(start_server())
