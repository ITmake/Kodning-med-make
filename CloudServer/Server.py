#!/usr/bin/env python3
import asyncio, sys, ipaddress
from socket import IPPROTO_TCP, TCP_NODELAY

import os
PORT = int(os.environ.get("PORT", 5000))
HOST = "0.0.0.0"

# writer -> {"username": str, "ip": str, "last_pm_partner": str|None}
clients = {}
muted_reasons = {}   # ip -> reason
banned_reasons = {}  # ip -> reason

# for server console /reply
last_server_pm_target: str | None = None

# ---------- utils ----------
def server_log(msg: str):
    print(msg, flush=True)

def get_ip_from_writer(writer: asyncio.StreamWriter) -> str:
    peer = writer.get_extra_info("peername")
    if isinstance(peer, tuple) and len(peer) >= 1:
        return str(peer[0])
    return "unknown"

def norm_name(name: str) -> str:
    return name.strip().lower()

def find_writer_by_username(name: str) -> asyncio.StreamWriter | None:
    tgt = norm_name(name)
    for w, info in clients.items():
        if norm_name(info["username"]) == tgt:
            return w
    return None

async def send_line(writer: asyncio.StreamWriter, text: str):
    try:
        writer.write((text.rstrip("\n") + "\n").encode("utf-8", "ignore"))
        await writer.drain()
    except Exception:
        pass

async def broadcast(line: str):
    data = (line.rstrip("\n") + "\n").encode("utf-8", "ignore")
    dead = []
    for w in list(clients.keys()):
        try:
            w.write(data)
        except Exception:
            dead.append(w)
    await asyncio.gather(
        *(w.drain() for w in list(clients.keys()) if not w.is_closing()),
        return_exceptions=True
    )
    for w in dead:
        clients.pop(w, None)
        try: w.close()
        except: pass

async def announce_join(username: str):
    await broadcast(f"*** {username} joined ***")

async def announce_leave(username: str):
    await broadcast(f"*** {username} left ***")

def list_online() -> str:
    rows = []
    for _, info in clients.items():
        name, ip = info["username"], info["ip"]
        tags = []
        if ip in muted_reasons: tags.append("muted")
        if ip in banned_reasons: tags.append("banned")
        suffix = f" ({', '.join(tags)})" if tags else ""
        rows.append(f"{name}@{ip}{suffix}")
    rows.sort()
    return ", ".join(rows) if rows else "(none)"

async def disconnect_ip(ip: str, reason: str = ""):
    to_close = [w for w, info in list(clients.items()) if info["ip"] == ip]
    for w in to_close:
        try:
            if reason:
                await send_line(w, reason)
        except Exception:
            pass
        uname = clients.get(w, {}).get("username")
        try:
            w.close()
            await w.wait_closed()
        except Exception:
            pass
        if uname:
            await announce_leave(uname)

# ---------- client connection ----------
async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    global last_server_pm_target
    ip = get_ip_from_writer(writer)

    # banned on arrival?
    if ip in banned_reasons:
        msg = f"You are banned. Reason: {banned_reasons[ip]}"
        await send_line(writer, msg)
        writer.close()
        try: await writer.wait_closed()
        except: pass
        return

    try:
        sock = writer.get_extra_info("socket")
        if sock: sock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
    except Exception:
        pass

    try:
        await send_line(writer, "ENTER_USERNAME")
        name_bytes = await reader.readline()
        if not name_bytes:
            writer.close(); await writer.wait_closed(); return
        username = name_bytes.decode("utf-8", "ignore").strip() or f"user_{ip.replace('.', '_')}"

        # ensure unique
        existing = {info["username"] for info in clients.values()}
        base = username; i = 2
        while username in existing:
            username = f"{base}{i}"; i += 1

        clients[writer] = {"username": username, "ip": ip, "last_pm_partner": None}
        await send_line(writer, "Welcome! Use /all <msg>, /msg <user> <msg>, /reply <msg>, /list, /quit.")
        await announce_join(username)
        server_log(f"[+] {username} connected from {ip}")

        while True:
            raw = await reader.readline()
            if not raw: break
            msg = raw.decode("utf-8", "ignore").strip()
            if not msg: continue

            # simple commands
            if msg == "/quit":
                await send_line(writer, "Goodbye!")
                break

            if msg == "/list":
                await send_line(writer, f"Online: {list_online()}")
                continue

            # muted can't send (except /quit, /list)
            if ip in muted_reasons:
                await send_line(writer, f"[Server]: You are muted. Reason: {muted_reasons[ip]}")
                continue

            # /all
            if msg.startswith("/all "):
                text = msg[5:].strip()
                if not text: continue
                out = f"{username}: {text}"
                server_log(out)
                await broadcast(out)
                continue

            # /msg
            if msg.lower().startswith("/msg "):
                parts = msg.split(" ", 2)
                if len(parts) < 3:
                    await send_line(writer, "[usage] /msg <username> <message>")
                    continue
                target_name = parts[1].strip()
                text = parts[2].strip()
                if not text:
                    await send_line(writer, "[usage] /msg <username> <message>")
                    continue

                # PM to server?
                if norm_name(target_name.strip("[]")) == "server":
                    server_log(f"(PM) {username} -> [Server]: {text}")
                    await send_line(writer, f"You -> [Server] (PM): {text}")
                    clients[writer]["last_pm_partner"] = "[Server]"
                    last_server_pm_target = username
                    continue

                # PM to client
                target_w = find_writer_by_username(target_name)
                if not target_w:
                    await send_line(writer, f"[Server]: user '{target_name}' not found.")
                    continue

                tinfo = clients.get(target_w, {})
                tname = tinfo.get("username", target_name)
                server_log(f"(PM) {username} -> {tname}: {text}")
                await send_line(target_w, f"{username} (PM): {text}")
                await send_line(writer, f"You -> {tname} (PM): {text}")

                # set last partners
                clients[writer]["last_pm_partner"] = tname
                if target_w in clients:
                    clients[target_w]["last_pm_partner"] = username
                continue

            # /reply
            if msg.lower().startswith("/reply"):
                # allow "/reply <message>"
                text = msg[6:].strip() if msg.strip().startswith("/reply") else ""
                if not text:
                    await send_line(writer, "[usage] /reply <message>")
                    continue
                partner = clients[writer].get("last_pm_partner")
                if not partner:
                    await send_line(writer, "[Server]: No one to reply to yet.")
                    continue

                if norm_name(partner.strip("[]")) == "server":
                    server_log(f"(PM) {username} -> [Server]: {text}")
                    await send_line(writer, f"You -> [Server] (PM): {text}")
                    last_server_pm_target = username
                    continue

                target_w = find_writer_by_username(partner)
                if not target_w:
                    await send_line(writer, f"[Server]: '{partner}' is no longer online.")
                    continue

                await send_line(target_w, f"{username} (PM): {text}")
                await send_line(writer, f"You -> {partner} (PM): {text}")
                # update partner on target
                if target_w in clients:
                    clients[target_w]["last_pm_partner"] = username
                continue

            # default -> treat as /all
            out = f"{username}: {msg}"
            server_log(out)
            await broadcast(out)

    except Exception:
        pass
    finally:
        info = clients.pop(writer, None)
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass
        if info:
            await announce_leave(info["username"])
            server_log(f"[-] {info['username']} disconnected ({info['ip']})")

# ---------- server console ----------
SERVER_PROMPT = "SERVER> "
HELP_TEXT = (
    "Server commands:\n"
    "  /all <message>                 - broadcast as [Server]\n"
    "  /msg <username> <message>      - PM a user\n"
    "  /reply <message>               - reply to last PM target\n"
    "  /warn <username|ip> <reason...>- send warning (by user or IP)\n"
    "  /list                          - list online users\n"
    "  /mute <ip> [reason...]         - mute IP (reason optional)\n"
    "  /unmute <ip>                   - unmute IP\n"
    "  /kick <ip>                     - disconnect IP\n"
    "  /ban <ip> [reason...]          - ban IP (disconnect + block)\n"
    "  /unban <ip>                    - remove IP from ban list\n"
    "  /mutes | /bans                 - show muted/banned with reasons\n"
    "  /help                          - show this help\n"
    "Anything else (no slash) is broadcast to everyone as [Server]."
)

async def server_console():
    global last_server_pm_target
    server_log(HELP_TEXT)
    while True:
        try:
            line = await asyncio.to_thread(input, SERVER_PROMPT)
        except (EOFError, KeyboardInterrupt):
            server_log("\n[Server console closed]")
            return
        if not line: continue
        cmd = line.strip()

        if cmd.startswith("/"):
            parts = cmd.split(" ", 2)
            op = parts[0].lower()

            if op == "/help":
                server_log(HELP_TEXT); continue

            if op == "/list":
                server_log("Online: " + list_online()); continue

            if op == "/mutes":
                if muted_reasons:
                    rows = [f"{ip} — {reason}" for ip, reason in sorted(muted_reasons.items())]
                    server_log("Muted:\n  " + "\n  ".join(rows))
                else:
                    server_log("Muted: (none)")
                continue

            if op == "/bans":
                if banned_reasons:
                    rows = [f"{ip} — {reason}" for ip, reason in sorted(banned_reasons.items())]
                    server_log("Banned:\n  " + "\n  ".join(rows))
                else:
                    server_log("Banned: (none)")
                continue

            if op == "/all":
                if len(parts) < 2 or not parts[1].strip():
                    server_log("Usage: /all <message>"); continue
                msg = parts[1].strip()
                server_log(f"[Server]: {msg}")
                await broadcast(f"[Server]: {msg}")
                continue

            if op == "/msg":
                if len(parts) < 3 or not parts[1].strip() or not parts[2].strip():
                    server_log("Usage: /msg <username> <message>"); continue
                target = parts[1].strip()
                text = parts[2].strip()
                w = find_writer_by_username(target)
                if not w:
                    server_log(f"[Server]: user '{target}' not found.")
                    continue
                await send_line(w, f"[Server] (PM): {text}")
                server_log(f"(PM) [Server] -> {clients[w]['username']}: {text}")
                last_server_pm_target = clients[w]["username"]
                continue

            if op == "/reply":
                if len(parts) < 2 or not parts[1].strip():
                    server_log("Usage: /reply <message>"); continue
                if not last_server_pm_target:
                    server_log("[Server]: No one to reply to yet.")
                    continue
                text = parts[1].strip()
                w = find_writer_by_username(last_server_pm_target)
                if not w:
                    server_log(f"[Server]: '{last_server_pm_target}' is no longer online.")
                    last_server_pm_target = None
                    continue
                await send_line(w, f"[Server] (PM): {text}")
                server_log(f"(PM) [Server] -> {clients[w]['username']}: {text}")
                continue

            # ---- FIXED: /warn supports username OR IP ----
            if op == "/warn":
                if len(parts) < 3 or not parts[1].strip() or not parts[2].strip():
                    server_log("Usage: /warn <username|ip> <reason>"); continue
                target_raw = parts[1].strip()
                reason = parts[2].strip()

                # Try username first
                w = find_writer_by_username(target_raw)
                if w:
                    await send_line(w, f"[Server] (WARNING): {reason}")
                    server_log(f"[admin] warned {clients[w]['username']}@{clients[w]['ip']}: {reason}")
                    last_server_pm_target = clients[w]['username']
                    continue

                # Otherwise interpret as IP and warn all sessions from that IP
                try:
                    ip = str(ipaddress.ip_address(target_raw))
                except ValueError:
                    server_log(f"[Server]: user or IP '{target_raw}' not found.")
                    continue

                delivered = 0
                for w2, info in list(clients.items()):
                    if info["ip"] == ip:
                        await send_line(w2, f"[Server] (WARNING): {reason}")
                        delivered += 1
                if delivered:
                    server_log(f"[admin] warned IP {ip} ({delivered} session(s)): {reason}")
                else:
                    server_log(f"[admin] warn: no connected clients at IP {ip}; (warning not delivered)")
                continue
            # ----------------------------------------------

            if op in {"/mute", "/ban"}:
                # /mute <ip> [reason...], /ban <ip> [reason...]
                if len(parts) < 2 or not parts[1].strip():
                    server_log(f"Usage: {op} <ip> [reason]"); continue
                ip = parts[1].strip()
                reason = ""
                if len(parts) == 3:
                    reason = parts[2].strip()
                if op == "/mute":
                    muted_reasons[ip] = reason or "Muted by admin"
                    await broadcast(f"[Server]: {ip} has been muted. Reason: {muted_reasons[ip]}")
                    # notify online users at that IP
                    for w, info in list(clients.items()):
                        if info["ip"] == ip:
                            await send_line(w, f"[Server]: You are muted. Reason: {muted_reasons[ip]}")
                    server_log(f"[admin] muted {ip} — {muted_reasons[ip]}")
                else:  # /ban
                    banned_reasons[ip] = reason or "Banned by admin"
                    await disconnect_ip(ip, f"[Server]: You are banned. Reason: {banned_reasons[ip]}")
                    await broadcast(f"[Server]: {ip} has been banned. Reason: {banned_reasons[ip]}")
                    server_log(f"[admin] banned {ip} — {banned_reasons[ip]}")
                continue

            if op == "/unmute":
                if len(parts) < 2 or not parts[1].strip():
                    server_log("Usage: /unmute <ip>"); continue
                ip = parts[1].strip()
                if ip in muted_reasons:
                    muted_reasons.pop(ip, None)
                    await broadcast(f"[Server]: {ip} has been unmuted.")
                server_log(f"[admin] unmuted {ip}")
                continue

            if op == "/kick":
                if len(parts) < 2 or not parts[1].strip():
                    server_log("Usage: /kick <ip>"); continue
                ip = parts[1].strip()
                await disconnect_ip(ip, "[Server]: You were kicked.")
                server_log(f"[admin] kicked {ip}")
                continue

            if op == "/unban":
                if len(parts) < 2 or not parts[1].strip():
                    server_log("Usage: /unban <ip>"); continue
                ip = parts[1].strip()
                if ip in banned_reasons:
                    banned_reasons.pop(ip, None)
                    await broadcast(f"[Server]: {ip} has been unbanned.")
                server_log(f"[admin] unbanned {ip}")
                continue

            server_log("Unknown command. Type /help.")
            continue

        # no slash: broadcast as [Server]
        msg = cmd
        server_log(f"[Server]: {msg}")
        await broadcast(f"[Server]: {msg}")

# ---------- main ----------
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    try:
        sock = server.sockets[0]
        sock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
    except Exception:
        pass

    addr = ", ".join(str(s.getsockname()) for s in server.sockets)
    server_log(f"Chat server listening on {addr}")

    async with server:
        await asyncio.gather(
            server.serve_forever(),
            server_console(),
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        server_log("\n[server stopped]")