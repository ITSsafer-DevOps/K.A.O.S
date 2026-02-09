#!/usr/bin/env python3
"""
K.A.O.S. Arm Client - Hybrid Agent
Acts as the frontend CLI for the distributed system. Replicates the Kali Linux environment.
"""

import os
import time
import subprocess
import shlex
import shutil
import requests
from datetime import datetime
import colorama
from colorama import Fore, Style

# Initialize colorama for ANSI escape codes
colorama.init()

# Configuration
SESSION_LOG = "/opt/arm/session.log"
BRAIN_HOST = os.getenv("BRAIN_HOST", "127.0.0.1")
BRAIN_PORT = os.getenv("BRAIN_PORT", "5000")


def print_banner():
    """Displays the startup banner in Red (English System Log)."""
    print(
        f"{Fore.RED}⚡ Starting Kali Linux AI environment...{Style.RESET_ALL}"
    )
    time.sleep(0.5)


def ensure_persistence():
    """
    Writes a timestamp to the session log to verify volume mounting on the host.
    If this fails, the container is likely not mounted correctly to the host.
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(SESSION_LOG, "a") as f:
            f.write(
                f"[{timestamp}] Session started. Brain: {BRAIN_HOST}:{BRAIN_PORT}\n"
            )
    except IOError as e:
        print(
            f"{Fore.RED}ERROR: Failed to write to persistent storage: {e}{Style.RESET_ALL}"
        )


def brain_analysis(command_input):
    """
    Sends the command to the Brain backend for analysis.
    Falls back to local rules if the Brain is offline.
    """
    url = f"http://{BRAIN_HOST}:{BRAIN_PORT}/api/v1/analyze"
    payload = {"command": command_input, "session_id": "cli-user"}

    try:
        response = requests.post(url, json=payload, timeout=2)
        response.raise_for_status()
        data = response.json()

        # Parse Backend Schema
        llm_layer = data.get("llm_layer", {})
        return {
            "proposed_command": llm_layer.get("command"),
            "reasoning": llm_layer.get("reasoning"),
        }
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}⚠️ Brain offline: {e}{Style.RESET_ALL}")

        # Fallback Logic
        proposed_cmd = f"echo 'Analysis failed: {command_input}'"
        lower_input = command_input.lower()

        if "scan" in lower_input:
            proposed_cmd = "nmap -sV localhost"
        elif "ip" in lower_input or "address" in lower_input:
            proposed_cmd = "ip a"

        return {
            "proposed_command": proposed_cmd,
            "reasoning": "Offline fallback rule applied.",
        }


def get_kali_prompt():
    """
    Renders the exact 2-line Kali Linux zsh prompt visual style.
    Line 1: ┌──(root㉿kaos-ai)-[~/host_home]
    Line 2: └─#
    """
    # Line 1: Blue bracket, Red user, White host, Blue path
    line1 = f"{Fore.BLUE}┌──({Fore.RED}root㉿kaos-ai{Fore.BLUE})-[{Style.RESET_ALL}~/host_home{Fore.BLUE}]{Style.RESET_ALL}"
    print(line1)
    # Line 2: Blue bracket, Hash, Reset
    return f"{Fore.BLUE}└─#{Style.RESET_ALL} "


def main():
    print_banner()
    ensure_persistence()

    while True:
        try:
            # 1. The Prompt (Visual Replica)
            user_input = input(get_kali_prompt()).strip()

            if not user_input:
                continue

            # 2. Exit Trap (Slovak UI)
            if user_input == "exit":
                print(
                    f"{Fore.RED}🔴 Invalid command. To exit use: kali-exit{Style.RESET_ALL}"
                )
                continue

            if user_input == "kali-exit":
                print(
                    f"{Fore.YELLOW}Session ended. Shutting down container...{Style.RESET_ALL}"
                )
                break

            # 3. Command Heuristics & Dispatch
            first_word = user_input.split()[0] if user_input else ""

            if shutil.which(first_word):
                # Reflex Loop: Trusted Execution (No Confirmation)
                print(
                    f"{Fore.GREEN}⚡ Executing: {user_input}{Style.RESET_ALL}"
                )
                try:
                    args = shlex.split(user_input)
                    subprocess.run(args, check=True)
                except subprocess.CalledProcessError as e:
                    print(
                        f"{Fore.RED}Error executing command: {e}{Style.RESET_ALL}"
                    )
                except ValueError:
                    print(
                        f"{Fore.RED}Failed to parse command.{Style.RESET_ALL}"
                    )
                continue

            # Cognition Loop: Natural Language -> Brain API
            response = brain_analysis(user_input)
            proposed_cmd = response.get("proposed_command")
            reasoning = response.get("reasoning", "No reasoning provided.")

            print(f"🤖 AI Reasoning: {Fore.CYAN}{reasoning}{Style.RESET_ALL}")
            print(
                f"🤖 AI Suggests: {Fore.CYAN}{proposed_cmd}{Style.RESET_ALL}"
            )

            # 4. Safety Loop (Human-in-the-Loop / English UI)
            confirm = input(f"Execute this command? [Y/n]: ").strip().upper()

            if confirm == "Y":  # 'Y' stands for 'Yes'
                # 5. Execution Phase
                try:
                    args = shlex.split(proposed_cmd)
                    subprocess.run(args, check=True)
                except subprocess.CalledProcessError as e:
                    print(
                        f"{Fore.RED}Error executing command: {e}{Style.RESET_ALL}"
                    )
                except ValueError:
                    print(
                        f"{Fore.RED}Failed to parse proposed command.{Style.RESET_ALL}"
                    )
            else:
                print(f"{Fore.YELLOW}Command cancelled.{Style.RESET_ALL}")

        except EOFError:
            print(
                f"\n{Fore.YELLOW}Use 'kali-exit' to terminate.{Style.RESET_ALL}"
            )
            continue
        except KeyboardInterrupt:
            print(
                f"\n{Fore.YELLOW}Use 'kali-exit' to terminate.{Style.RESET_ALL}"
            )


if __name__ == "__main__":
    main()
