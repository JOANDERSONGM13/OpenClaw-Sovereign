#!/usr/bin/env python3
import argparse
import time
import json
import sys
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from mcp_client import MCPClient

def format_currency(value_str):
    if not value_str: return "N/A"
    try:
        val = float(value_str)
        return f"${val:,.4f}"
    except:
        return value_str

def format_number(value_str):
    if not value_str: return "N/A"
    try:
        val = float(value_str)
        return f"{val:,.2f}"
    except:
        return value_str

def main():
    parser = argparse.ArgumentParser(description="Check Bittensor Subnet Metrics via Taostats MCP")
    parser.add_argument("netuid", type=int, help="The Subnet NetUID (e.g., 33 for ReadyAI)")
    args = parser.parse_args()

    load_dotenv()
    url = os.getenv("TAOSTATS_MCP_URL")
    if not url:
        print("Error: TAOSTATS_MCP_URL not set in .env")
        sys.exit(1)

    console = Console()
    console.print(f"[bold blue]Connecting to Taostats MCP...[/bold blue] (Target: Subnet {args.netuid})")
    
    client = MCPClient(url)
    
    if client.connect():
        # Give it a moment to stabilize the connection
        time.sleep(1)
        
        with console.status(f"[bold green]Fetching data for Subnet {args.netuid}...[/bold green]"):
            result = client.call_tool("GetLatestSubnetPool", {"netuid": args.netuid})
            time.sleep(1) # simulate/wait for network slightly if needed, though call_tool is blocking now

        if result and "content" in result and len(result["content"]) > 0:
            content = result["content"][0]
            if content.get("type") == "text":
                data_obj = content["text"] # already parsed by client
                if isinstance(data_obj, dict) and "data" in data_obj and len(data_obj["data"]) > 0:
                    data = data_obj["data"][0]
                    
                    # Create Layout
                    console.print("\n")
                    
                    # Header Panel
                    title = f"[bold gold1]{data.get('name', 'Unknown')}[/bold gold1] [white](Subnet {data.get('netuid')})[/white]"
                    symbol = data.get('symbol', '')
                    console.print(Panel(title, subtitle=f"Symbol: {symbol}", expand=False, border_style="blue"))
                    
                    # Key Metrics Table
                    table = Table(title="Key Metrics", box=box.ROUNDED, show_header=True, header_style="bold magenta")
                    table.add_column("Metric", style="cyan")
                    table.add_column("Value", style="bold white")
                    
                    # Highlighted metrics
                    price = format_currency(data.get('price', '0'))
                    price_change = data.get('price_change_1_day', '0%')
                    p_color = "green" if not price_change.startswith("-") else "red"
                    
                    table.add_row("Price", f"[gold1]{price}[/gold1] ([{p_color}]{price_change}[/{p_color}])")
                    table.add_row("Market Cap", format_currency(data.get('market_cap', '0')))
                    table.add_row("Liquidity", format_currency(data.get('liquidity', '0')))
                    table.add_row("24h Volume", format_currency(data.get('tao_volume_24_hr', '0')))
                    
                    # 24h Activity
                    table.add_row("24h Buys", str(data.get('buys_24_hr', '0')))
                    table.add_row("24h Sells", str(data.get('sells_24_hr', '0')))
                    table.add_row("24h Buyers", str(data.get('buyers_24_hr', '0')))
                    table.add_row("24h Sellers", str(data.get('sellers_24_hr', '0')))
                    
                    console.print(table)
                    
                    # Details Table
                    grid = Table.grid(expand=True)
                    grid.add_column()
                    grid.add_column(justify="right")
                    
                    d_table = Table(title="Network Details", box=box.SIMPLE)
                    d_table.add_column("Property", style="dim")
                    d_table.add_column("Value")
                    
                    d_table.add_row("Block Number", str(data.get('block_number')))
                    d_table.add_row("Total TAO", format_number(data.get('total_tao')))
                    d_table.add_row("Total Alpha", format_number(data.get('total_alpha')))
                    d_table.add_row("Recycle/Registered", f"{data.get('start_block')}/{data.get('registered')}" if 'registered' in data else "N/A")
                    
                    console.print(d_table)
                    print("\n")

                else:
                    console.print("[red]No data found for this subnet.[/red]")
                    console.print(data_obj)
        else:
            console.print("[bold red]Failed to retrieve data.[/bold red]")
            if result:
                console.print(result)

    else:
        console.print("[bold red]Failed to connect to MCP server.[/bold red]")

if __name__ == "__main__":
    main()
