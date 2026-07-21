

def analisar_e_disparar(game, stats, p, m, sh, sa, odd_h, odd_a, sent_vistos):
    # IDENTIFICAÇÃO DO FAVORITO PRÉ-LIVE (OBRIGATÓRIO)
    try:
        oh = float(odd_h) if odd_h else 3.0
        oa = float(odd_a) if odd_a else 3.0
        fav_side = "h" if oh < oa else "a"
    except:
        fav_side = "h"

    # DADOS DO FAVORITO
    fav_gols = sh if fav_side == "h" else sa
    adv_gols = sa if fav_side == "h" else sh
    red_fav = stats.get(f"red_cards_{fav_side}", 0)
    
    # MERCADOS
    
    # 1. OVER GOL INTERVALO (HT)
    if p == 1 and 15 <= m <= 27:
        if sh == 0 and sa == 0 and red_fav == 0:
            return "HT", "Over 0.5 Gols HT"

    # 2. OVER GOL PARTIDA (FT)
    if p == 2 and 55 <= m <= 75:
        if (fav_gols <= adv_gols) and (adv_gols - fav_gols <= 1) and red_fav == 0:
            total_gols = sh + sa
            return "OVERGOAL", f"Mais de {total_gols + 0.5} Gols"

    # 3. AMBAS MARCAM (BTTS)
    if p == 2 and 55 <= m <= 75:
        if (sh + sa == 1) and (fav_gols == 0 and adv_gols == 1) and red_fav == 0:
            return "BTTS", "Ambas Marcam"

    # 4. OVER 1.5 GOLS PARTIDA
    if p == 2 and 55 <= m <= 75:
        if (sh + sa == 1) and (fav_gols == 0 and adv_gols == 1) and red_fav == 0:
            return "OFT", "Mais de 1.5 Gols Partida"

    # 5. ESCANTEIO LIMITE HT
    if p == 1 and 28 <= m <= 38:
        if (fav_gols <= adv_gols) and (adv_gols - fav_gols <= 1) and red_fav == 0:
            return "CORNER_HT", "Escanteio Limite HT"

    # 6. ESCANTEIO LIMITE FT
    if p == 2 and 78 <= m <= 88:
        if (fav_gols <= adv_gols) and (adv_gols - fav_gols <= 1) and red_fav == 0:
            return "CORNER_FT", "Escanteio Limite FT"

    return (None, None, None), None

def gerar_layout_relatorio(greens, reds, data_str):
    sep = "━━━━━━━━━━━━━━━━━━━━"
    total = greens + reds
    taxa = (greens / total * 100) if total > 0 else 0.0
    return (
        f"{sep}\n"
        f"<b>📊 RELATÓRIO DIÁRIO — {data_str}</b>\n"
        f"{sep}\n"
        f"✅ GREEN: <b>{greens}</b>\n"
        f"🔴 RED: <b>{reds}</b>\n"
        f"📈 TOTAL DE ENTRADAS: <b>{total}</b>\n"
        f"🎯 ASSERTIVIDADE: <b>{taxa:.1f}%</b>\n"
        f"{sep}\n"
        f"⚠️👆Resultados do dia👆⚠️"
    )

def gerar_layout_relatorio_mensal(greens, reds, mes_nome, dias_ativos):
    sep = "\u2501" * 20
    total = greens + reds
    taxa = (greens / total * 100) if total > 0 else 0.0
    msg = f"{sep}\n"
    msg += f"<b>\U0001f4ca RELAT\u00d3RIO MENSAL \u2014 {mes_nome}</b>\n"
    msg += f"{sep}\n"
    msg += f"\u2705 GREEN: <b>{greens}</b>\n"
    msg += f"\U0001f534 RED: <b>{reds}</b>\n"
    msg += f"\U0001f4c8 TOTAL DE ENTRADAS: <b>{total}</b>\n"
    msg += f"\U0001f3af ASSERTIVIDADE: <b>{taxa:.1f}%</b>\n"
    msg += f"{sep}\n"
    msg += f"\U0001f4c5 Dias com entradas: <b>{dias_ativos}</b>\n"
    msg += "\u26a0\ufe0f\U0001f446Resultados do m\u00eas\U0001f446\u26a0\ufe0f"
    return msg

def gerar_layout_radar(jogos_ao_vivo, jogos_na_janela):
    sep = "━━━━━━━━━━━━━━━━━━━━"
    texto_jan = ""
    for j in jogos_na_janela:
        h = j.get("home","") or getattr(j,"home","")
        a = j.get("away","") or getattr(j,"away","")
        m = j.get("minuto","") or getattr(j,"minuto","")
        sh = j.get("sh",0) or getattr(j,"sh",0)
        sa = j.get("sa",0) or getattr(j,"sa",0)
        liga = j.get("liga","") or getattr(j,"liga","")
        texto_jan += f"🎯 <b>{h} x {a}</b> | {m}' | {sh}x{sa} | {liga}\n"
    if not texto_jan:
        texto_jan = "Nenhum jogo na janela no momento."
    corpo = (
        f"{sep}\n"
        f"📡 RADAR — JOGOS AO VIVO\n"
        f"{sep}\n"
        f"🔴 Jogos na Janela:\n"
        f"{texto_jan}"
        f"{sep}\n"
        f"🟢 Ao Vivo: <b>{len(jogos_ao_vivo)}</b>"
    )
    return corpo

import requests

def obter_nome_liga(game, fonte):
    # FotMob: game['league']['name']
    # Bzzoiro: game['league_name']
    liga = "Liga Não Identificada"
    
    if fonte == "fotmob":
        liga = game.get('name', "Liga Não Identificada")
    elif fonte == "bzzoiro":
        liga = game.get('league_name', "Liga Não Identificada")
    
    # Se ainda estiver vazio, busca em campos genéricos que as APIs costumam usar
    if liga == "Liga Não Identificada":
        liga = game.get('league_name') or game.get('competition_name') or game.get('league') or "Liga Não Identificada"
        
    return liga
# ═══════════════════════════════════════════════════════════════════════════════
# BOT MÁQUINA DE GREENS / ZAPIA - VERSÃO ELITE 100% AUTOMÁTICA
# FONTES: BZZOIRO + FOTMOB (fallback)
# ═══════════════════════════════════════════════════════════════════════════════
import os, json, requests, time
from datetime import datetime, timezone, timedelta
import hashlib, re, unicodedata

# ─── Normalização de nomes de times (acentos, abreviações, prefixos) ────────────
def norm_nome_time(nome):
    """Remove acentos, expande abreviações e limpa prefixos/sufixos de nome de time."""
    n = unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore').decode().lower().strip()
    # Remove prefixos comuns: msk, hnk, nk, fk, sk, fc, etc
    n = re.sub(r'\b(msk|hnk|nk|fk|sk|fc|ac|ec|se|cf)\b', '', n)
    # Expande abreviações comuns
    n = n.replace('u.', 'universitatea').replace('dyn.', 'dynamo').replace('s.n.', '').replace('c.s.', '')
    # Remove siglas de estados e outros prefixos genéricos
    n = re.sub(r'\b(rj|sp|mg|rs|pr|sc|ba|pe|ce|go|mt|ms|df|es|rn|pb|al|se|pi|ma|pa|am|ro|rr|ap|to|fr|ac|ec|se|cf)\b', '', n)
    return re.sub(r'\s+', ' ', n).strip()

# ─── Caminhos e Fuso ───────────────────────────────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
SENT_FILE       = os.path.join(BASE_DIR, "sent_live_signals.json")
SINAIS_FILE     = os.path.join(BASE_DIR, "sinais_pendentes.json")
RESULTADO_FILE  = os.path.join(BASE_DIR, "resultados.json")
PERFORMANCE_FILE= os.path.join(BASE_DIR, "performance.json")
LAST_UPDATE_FILE= os.path.join(BASE_DIR, "last_update.json")
BRT             = timezone(timedelta(hours=-3))

# ─── Credenciais ───────────────────────────────────────────────────────────────
TELEGRAM_TOKEN  = os.getenv("TG_TOKEN", "")
TG_TOKEN = TELEGRAM_TOKEN
CHAT_IDS = [os.environ.get("TG_GROUP_ID", "")]
CHAT_ID = CHAT_IDS[0] if CHAT_IDS else ""  # BOOT IA INTELIGENTE (Zapia)

# Bzzoiro (principal — com token, dados completos ao vivo)
BZZOIRO_URL   = "https://sports.bzzoiro.com"
BZZOIRO_TOKEN = os.getenv("BZZOIRO_TOKEN", "")

# FotMob (fallback — API pública, sem chave, sem limite)
FOTMOB_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.fotmob.com/"
}

# ═══════════════+++
# TELEGRAM
# ═══════════════════════════════════════════════════════════════════════════════
def send_telegram(msg_data, reply_to=None, marca=None, home="", away="", odd_b365_val=None, odd_bano_val=None):
    """Envia mensagem formatada com botões inline."""
    if isinstance(msg_data, tuple):
        text, keyboard = msg_data
    else:
        text = msg_data
        keyboard = None

    url_send = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    last_mid = None
    for chat_id in CHAT_IDS:
        payload = {
            "chat_id": chat_id, 
            "text": text, 
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        if reply_to:
            payload["reply_to_message_id"] = reply_to
        if keyboard:
            payload["reply_markup"] = json.dumps(keyboard)
            
        try:
            r = requests.post(url_send, json=payload, timeout=10)
            res = r.json()
            if res.get("ok"):
                last_mid = res.get("result", {}).get("message_id")
        except:
            pass
    return last_mid

# ═══════════════════════════════════════════════════════════════════════════════
# ARQUIVOS LOCAIS
# ═══════════════════════════════════════════════════════════════════════════════
GITHUB_TOKEN = os.environ.get("GH_PAT", "")
GITHUB_REPO  = os.environ.get("GITHUB_REPOSITORY", "cleubianodasilva-png/boot-ia-inteligente-bot")
SENT_API_PATH        = "sent_live_signals.json"
RESULTADO_API_PATH   = "resultados.json"
PERFORMANCE_API_PATH = "performance.json"

def _github_headers():
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

def load_sent():
    """Carrega sent do GitHub (fonte de verdade) + arquivo local como fallback."""
    # Tenta GitHub API primeiro
    if GITHUB_TOKEN and GITHUB_REPO:
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{SENT_API_PATH}"
            r = requests.get(url, headers=_github_headers(), timeout=8)
            if r.status_code == 200:
                import base64 as _b64
                data = json.loads(_b64.b64decode(r.json()["content"]).decode())
                sent = set(data)
                # Limpa chaves antigas (> 2 dias) para não crescer infinito
                hoje = datetime.now(BRT).strftime('%Y%m%d')
                ontem = (datetime.now(BRT) - timedelta(days=1)).strftime('%Y%m%d')
                sent = {k for k in sent if hoje in k or ontem in k}
                # Salva localmente também
                with open(SENT_FILE, 'w') as f: json.dump(list(sent), f)
                print(f"[SENT] Carregado do GitHub: {len(sent)} chaves")
                return sent
        except Exception as e:
            print(f"[SENT] Erro GitHub load: {e}")
    # Fallback: arquivo local
    if os.path.exists(SENT_FILE):
        try:
            with open(SENT_FILE, 'r') as f: return set(json.load(f))
        except: pass
    return set()

def save_sent(sent):
    """Salva sent localmente E no GitHub (fonte de verdade)."""
    with open(SENT_FILE, 'w') as f: json.dump(list(sent), f)
    if GITHUB_TOKEN and GITHUB_REPO:
        try:
            import base64 as _b64
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{SENT_API_PATH}"
            # Pega SHA atual
            r = requests.get(url, headers=_github_headers(), timeout=8)
            sha = r.json().get("sha", "") if r.status_code == 200 else ""
            content_b64 = _b64.b64encode(json.dumps(list(sent)).encode()).decode()
            payload = {"message": "state: atualiza sent [skip ci]", "content": content_b64}
            if sha: payload["sha"] = sha
            r2 = requests.put(url, headers=_github_headers(), json=payload, timeout=10)
            if r2.status_code in (200, 201):
                print(f"[SENT] Salvo no GitHub: {len(sent)} chaves")
            else:
                print(f"[SENT] Erro GitHub save: {r2.status_code}")
        except Exception as e:
            print(f"[SENT] Erro GitHub save: {e}")

def _load_sinais_github():
    """Carrega sinais_pendentes.json do GitHub."""
    import base64 as _b64
    if GITHUB_TOKEN and GITHUB_REPO:
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/sinais_pendentes.json"
            r = requests.get(url, headers=_github_headers(), timeout=8)
            if r.status_code == 200:
                return json.loads(_b64.b64decode(r.json()["content"]).decode())
        except Exception as e:
            print(f"[SINAIS] Erro load GitHub: {e}")
    if os.path.exists(SINAIS_FILE):
        try:
            with open(SINAIS_FILE, 'r') as f: return json.load(f)
        except: pass
    return []

def _save_sinais_github(sinais):
    """Salva sinais_pendentes.json no GitHub E localmente."""
    import base64 as _b64
    with open(SINAIS_FILE, 'w') as f: json.dump(sinais, f)
    if GITHUB_TOKEN and GITHUB_REPO:
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/sinais_pendentes.json"
            r = requests.get(url, headers=_github_headers(), timeout=8)
            sha = r.json().get("sha", "") if r.status_code == 200 else ""
            content_b64 = _b64.b64encode(json.dumps(sinais).encode()).decode()
            payload = {"message": "state: atualiza sinais_pendentes [skip ci]", "content": content_b64}
            if sha: payload["sha"] = sha
            r2 = requests.put(url, headers=_github_headers(), json=payload, timeout=10)
            if r2.status_code in (200, 201):
                print(f"[SINAIS] Salvo no GitHub: {len(sinais)} pendentes")
            else:
                print(f"[SINAIS] Erro GitHub save: {r2.status_code}")
        except Exception as e:
            print(f"[SINAIS] Erro save GitHub: {e}")

def registrar_sinal(fid, mercado, home, away, message_id, extra_val=None):
    sinais = _load_sinais_github()
    sinais.append({
        "fixture_id": fid, "mercado": mercado,
        "home": home, "away": away,
        "message_id": message_id, "extra_val": extra_val,
        "timestamp": datetime.now(BRT).isoformat()
    })
    _save_sinais_github(sinais)

def _load_resultados_github():
    """Carrega resultados.json do GitHub. Retorna lista de registros."""
    import base64 as _b64
    if GITHUB_TOKEN and GITHUB_REPO:
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{RESULTADO_API_PATH}"
            r = requests.get(url, headers=_github_headers(), timeout=8)
            if r.status_code == 200:
                data = json.loads(_b64.b64decode(r.json()["content"]).decode())
                if isinstance(data, list):
                    return data
        except Exception as e:
            print(f"[RESULTADO] Erro load GitHub: {e}")
    # Fallback local
    if os.path.exists(RESULTADO_FILE):
        try:
            with open(RESULTADO_FILE, 'r') as f:
                return json.load(f)
        except: pass
    return []

def _save_resultados_github(registros):
    """Salva resultados.json no GitHub E localmente."""
    import base64 as _b64
    with open(RESULTADO_FILE, 'w') as f: json.dump(registros, f, indent=2)
    if GITHUB_TOKEN and GITHUB_REPO:
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{RESULTADO_API_PATH}"
            r = requests.get(url, headers=_github_headers(), timeout=8)
            sha = r.json().get("sha", "") if r.status_code == 200 else ""
            content_b64 = _b64.b64encode(json.dumps(registros, indent=2).encode()).decode()
            payload = {"message": "state: atualiza resultados [skip ci]", "content": content_b64}
            if sha: payload["sha"] = sha
            r2 = requests.put(url, headers=_github_headers(), json=payload, timeout=10)
            if r2.status_code in (200, 201):
                print(f"[RESULTADO] Salvo no GitHub: {len(registros)} registros")
            else:
                print(f"[RESULTADO] Erro GitHub save: {r2.status_code}")
        except Exception as e:
            print(f"[RESULTADO] Erro save GitHub: {e}")

def salvar_resultado(resultado, mercado=None):
    hoje = datetime.now(BRT).strftime("%Y-%m-%d")
    registros = _load_resultados_github()
    registros.append({
        "data": hoje, "resultado": resultado,
        "mercado": mercado,
        "timestamp": datetime.now(BRT).isoformat()
    })
    _save_resultados_github(registros)


def get_relatorio_mensal():
    hoje = datetime.now(BRT)
    mes_str = hoje.strftime("%Y-%m")
    greens, reds = 0, 0
    registros = _load_resultados_github()
    dias_ativos = set()
    for r in registros:
        data_reg = r.get("data", "")
        if data_reg.startswith(mes_str):
            dias_ativos.add(data_reg)
            if r.get("resultado") == "green": greens += 1
            else: reds += 1
    return greens, reds, len(dias_ativos)

def get_relatorio_hoje():
    hoje = datetime.now(BRT).strftime("%Y-%m-%d")
    greens, reds = 0, 0
    registros = _load_resultados_github()
    for r in registros:
        if r.get("data") == hoje:
            if r.get("resultado") == "green": greens += 1
            else: reds += 1
    return greens, reds


def enviar_relatorio_mensal():
    hoje = datetime.now(BRT)
    meses_pt = ["Janeiro","Fevereiro","Mar\u00e7o","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
    mes_nome = f"{meses_pt[hoje.month-1]}/{hoje.year}"
    greens, reds, dias_ativos = get_relatorio_mensal()
    msg = gerar_layout_relatorio_mensal(greens, reds, mes_nome, dias_ativos)
    return msg

def enviar_relatorio_diario():
    hoje_key = f"relatorio_{datetime.now(BRT).strftime('%Y-%m-%d')}"
    hoje = datetime.now(BRT).strftime("%d/%m/%Y")
    greens, reds = get_relatorio_hoje()
    msg = gerar_layout_relatorio(greens, reds, hoje)
    if send_telegram(msg):
        sent_ctrl.add(hoje_key)
        save_sent(sent_ctrl)
        print(f"[Relatório] Enviado ({hoje_key})")

# ─── Performance por Mercado ────────────────────────────────────────────────────
MAPA_MERCADO = {
    "HT": "🔥 Over 0.5 Gols HT",
    "LIMITEHT": "🔥 Over Gol Limite HT",
    "BTTS": "⚽ BTTS",
    "OFT": "⚽ Over 1.5 FT",
    "OVERGOAL": "⚽ Over Gol FT",
    "CORNER_HT": "⛳️ Escanteio Limite HT",
    "CORNER_FT": "⛳️ Escanteio Limite FT"
}

def _load_performance_github():
    """Carrega performance.json do GitHub. Retorna dict {mercado: {green, red, total}}."""
    import base64 as _b64
    if GITHUB_TOKEN and GITHUB_REPO:
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{PERFORMANCE_API_PATH}"
            r = requests.get(url, headers=_github_headers(), timeout=8)
            if r.status_code == 200:
                data = json.loads(_b64.b64decode(r.json()["content"]).decode())
                if isinstance(data, dict):
                    return data
        except Exception as e:
            print(f"[PERFORMANCE] Erro load GitHub: {e}")
    if os.path.exists(PERFORMANCE_FILE):
        try:
            with open(PERFORMANCE_FILE, 'r') as f:
                return json.load(f)
        except: pass
    return {}

def _save_performance_github(perf):
    """Salva performance.json no GitHub E localmente."""
    with open(PERFORMANCE_FILE, 'w') as f:
        json.dump(perf, f, indent=2)
    if GITHUB_TOKEN and GITHUB_REPO:
        try:
            import base64 as _b64
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{PERFORMANCE_API_PATH}"
            r = requests.get(url, headers=_github_headers(), timeout=8)
            sha = r.json().get("sha", "") if r.status_code == 200 else ""
            content_b64 = _b64.b64encode(json.dumps(perf, indent=2).encode()).decode()
            payload = {"message": "state: atualiza performance [skip ci]", "content": content_b64}
            if sha: payload["sha"] = sha
            r2 = requests.put(url, headers=_github_headers(), json=payload, timeout=10)
            if r2.status_code in (200, 201):
                print(f"[PERFORMANCE] Salvo no GitHub: {sum(v.get('total',0) for v in perf.values())} registros")
            else:
                print(f"[PERFORMANCE] Erro GitHub save: {r2.status_code}")
        except Exception as e:
            print(f"[PERFORMANCE] Erro save GitHub: {e}")

def registrar_performance(mercado, resultado):
    """Registra resultado de um mercado específico no performance.json."""
    perf = _load_performance_github()
    if mercado not in perf:
        perf[mercado] = {"green": 0, "red": 0, "total": 0}
    perf[mercado]["total"] += 1
    if resultado == "green":
        perf[mercado]["green"] += 1
    else:
        perf[mercado]["red"] += 1
    _save_performance_github(perf)
    total = perf[mercado]["total"]
    greens = perf[mercado]["green"]
    pct = greens / total * 100 if total > 0 else 0
    print(f"[PERFORMANCE] {MAPA_MERCADO.get(mercado, mercado)}: {resultado} ({greens}/{total} = {pct:.1f}%)")

def get_performance():
    """Retorna dict com performance e % por mercado, e validação 70%/1000."""
    perf = _load_performance_github()
    resultado = {}
    for cod, nome in MAPA_MERCADO.items():
        p = perf.get(cod, {"green": 0, "red": 0, "total": 0})
        total = p["total"]
        greens = p["green"]
        reds = p["red"]
        pct = (greens / total * 100) if total > 0 else 0
        valido = total >= 1000 and pct >= 70
        resultado[cod] = {
            "nome": nome, "green": greens, "red": reds,
            "total": total, "pct": pct, "valido": valido
        }
    return resultado

def get_performance_24h():
    """Retorna performance por mercado nas últimas 24h a partir dos resultados salvos."""
    registros = _load_resultados_github()
    agora = datetime.now(BRT)
    corte = agora - timedelta(hours=24)
    
    perf = {}
    for cod, nome in MAPA_MERCADO.items():
        perf[cod] = {"nome": nome, "green": 0, "red": 0, "total": 0}
    
    for r in registros:
        ts_str = r.get("timestamp", "")
        mercado = r.get("mercado", "")
        resultado = r.get("resultado", "")
        if not ts_str or not mercado or not resultado:
            continue
        if mercado not in perf:
            continue
        try:
            ts = datetime.fromisoformat(ts_str)
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone(timedelta(hours=-3)))
            if ts < corte:
                continue
        except:
            continue
        perf[mercado]["total"] += 1
        if resultado == "green":
            perf[mercado]["green"] += 1
        else:
            perf[mercado]["red"] += 1
    
    for cod, info in perf.items():
        t = info["total"]
        g = info["green"]
        info["pct"] = (g / t * 100) if t > 0 else 0
    
    return perf

def gerar_layout_performance():
    """Gera layout do relatório de performance por mercado."""
    dados = get_performance()
    sep = "━" * 20
    linhas = []
    for cod, info in dados.items():
        nome = info["nome"]
        g = info["green"]
        r = info["red"]
        t = info["total"]
        pct = info["pct"]
        valido = info["valido"]
        barra = ""
        if t > 0:
            g_pct = int(g / t * 10)
            barra = "🟢" * g_pct + "🔴" * (10 - g_pct)
        status = "✅" if valido else "⏳"
        linhas.append(
            f"{nome}\n"
            f"   {status} Total: {t} | 🟢 {g} | 🔴 {r}\n"
            f"   🎯 Acerto: <b>{pct:.1f}%</b>\n"
            f"   {barra}"
        )
    total_g = sum(d["green"] for d in dados.values())
    total_r = sum(d["red"] for d in dados.values())
    total_t = total_g + total_r
    total_pct = (total_g / total_t * 100) if total_t > 0 else 0

    msg = (
        f"{sep}\n"
        f"📊<b>RELATÓRIO DE PERFORMANCE</b>📊\n"
        f"{sep}\n"
        f"{chr(10).join(linhas)}\n"
        f"{sep}\n"
        f"📌 <b>GERAL: {total_t} sinais | 🟢 {total_g} | 🔴 {total_r} | {total_pct:.1f}%</b>\n"
        f"{sep}\n"
        f"<b>Regras de Validação:</b>\n"
        f"✅ Mínimo 1000 entradas + ≥70% acerto = Mercado <b>VÁLIDO</b>\n"
        f"⏳ Ainda não atingiu os critérios\n"
        f"{sep}"
    )
    return msg

def enviar_relatorio_performance():
    """Gera o relatório de performance. Retorna o texto da mensagem (sem enviar)."""
    return gerar_layout_performance()

def gerar_layout_mercados24h():
    """Gera layout do relatório de performance por mercado nas últimas 24h."""
    dados = get_performance_24h()
    sep = "━" * 20
    linhas = []
    for cod, info in dados.items():
        nome = info["nome"]
        g = info["green"]
        r = info["red"]
        t = info["total"]
        pct = info["pct"]
        barra = ""
        if t > 0:
            g_pct = int(g / t * 10)
            barra = "🟢" * g_pct + "🔴" * (10 - g_pct)
        linhas.append(
            f"{nome}\n"
            f"   Total: {t} | 🟢 {g} | 🔴 {r}\n"
            f"   🎯 Acerto: <b>{pct:.1f}%</b>\n"
            f"   {barra}"
        )
    total_g = sum(d["green"] for d in dados.values())
    total_r = sum(d["red"] for d in dados.values())
    total_t = total_g + total_r
    total_pct = (total_g / total_t * 100) if total_t > 0 else 0

    msg = (
        f"{sep}\n"
        f"📊<b>MERCADOS — ÚLTIMAS 24H</b>📊\n"
        f"{sep}\n"
        f"{chr(10).join(linhas)}\n"
        f"{sep}\n"
        f"📌 <b>GERAL: {total_t} sinais | 🟢 {total_g} | 🔴 {total_r} | {total_pct:.1f}%</b>\n"
        f"{sep}"
    )
    return msg

def enviar_relatorio_mercados24h():
    """Gera o relatório de mercados 24h. Retorna o texto da mensagem (sem enviar)."""
    return gerar_layout_mercados24h()

# ═══════════════════════════════════════════════════════════════════════════════
# API 1 — BZZOIRO: lista de jogos ao vivo
# ═══════════════════════════════════════════════════════════════════════════════
def get_jogos_bzzoiro(fids_existentes):
    """Busca jogos ao vivo via /events/ com date_from+date_to, filtrando por status.
    Mais confiável que /events/live/ que tem cache instável e janela apertada."""
    try:
        headers = {"Authorization": "Token " + BZZOIRO_TOKEN}
        hoje = datetime.now().strftime("%Y-%m-%d")
        url = f"{BZZOIRO_URL}/api/v2/events/?date_from={hoje}T00:00:00Z&date_to={hoje}T23:59:59Z&limit=200"
        r = requests.get(url, headers=headers, timeout=15)
        data = r.json()
        results = data.get("results", [])
        # Monta mapa liga_id → nome
        try:
            rl = requests.get(f"{BZZOIRO_URL}/api/v2/leagues/?limit=100", headers=headers, timeout=8)
            ld = rl.json()
            league_map = {l.get("id"): l.get("name", "?") for l in ld.get("results", [])}
        except:
            league_map = {}
        STATUS_LIVE = {"1st_half", "2nd_half", "halftime", "inprogress", "extratime", "penalties"}
        jogos = []
        for ev in results:
            status = str(ev.get("status", "") or "")
            if status not in STATUS_LIVE:
                continue
            fid = "bzz_" + str(ev.get("id", ""))
            if fid in fids_existentes: continue
            sh, sa = int(ev.get("home_score") or 0), int(ev.get("away_score") or 0)
            minuto = ev.get("current_minute") or 0
            if not isinstance(minuto, int):
                try: minuto = int(str(minuto).split("'")[0])
                except: minuto = 0
            liga_nome = league_map.get(ev.get("league_id"), "") or ""
            if not liga_nome:
                liga_nome = "Desconhecida"
            p_raw = str(ev.get("period", "") or "")
            period = 1 if "1" in p_raw or minuto <= 45 else 2
            jogos.append({
                "fid": fid, "fid_raw": str(ev.get("id", "")),
                "home": ev.get("home_team", ""), "away": ev.get("away_team", ""),
                "sh": sh, "sa": sa, "minuto": minuto,
                "period": period, "liga": liga_nome, "source": "bzzoiro"
            })
        print(f"[Bzzoiro] {len(jogos)} novos jogos")
        return jogos
    except Exception as e:
        print(f"[Bzzoiro ERRO] {e}")
        return []


# ═══════════════════════════════════════════════════════════════════════════════
# API 1B — FotMob: jogos ao vivo (preenche o que o Bzzoiro não cobre)
# ═══════════════════════════════════════════════════════════════════════════════
def get_jogos_fotmob(fids_existentes):
    """Busca jogos ao vivo via FotMob (API pública, sem chave). Preenche o que o Bzzoiro não cobre."""
    try:
        from datetime import datetime
        hoje = datetime.now().strftime("%Y%m%d")
        params = {"date": hoje, "timezone": "America/Bahia", "ccode3": "BRA"}
        r = requests.get("https://www.fotmob.com/api/data/matches", params=params, headers=FOTMOB_HEADERS, timeout=15)
        if r.status_code != 200:
            print(f"[FotMob] Erro: status {r.status_code}")
            return []
        data = r.json()

        # Status IDs do FotMob: 2=ao vivo (1T/2T), 7=segundo tempo, 8=final, 9=prorrogação, 10=intervalo
        # ATENÇÃO: sid=6 é FINALIZADO (started=True, finished=True) — NÃO incluir
        STATUS_LIVE = {2, 7, 8, 9, 10}
        jogos = []

        for league in data.get("leagues", []):
            liga_nome = league.get("name", "Desconhecida")
            for match in league.get("matches", []):
                if match.get("statusId") not in STATUS_LIVE:
                    continue
                mid = match["id"]
                fid = "fotmob_" + str(mid)
                if fid in fids_existentes:
                    continue

                home = match.get("home", {})
                away = match.get("away", {})
                sh = int(home.get("score", 0) or 0)
                sa = int(away.get("score", 0) or 0)

                # Extrai minuto real do liveTime
                status = match.get("status", {})
                lt = status.get("liveTime", {}) or {}
                short = lt.get("short", "").replace("\u200e", "").replace("'", "").strip()
                try:
                    if short == "HT":
                        minuto = 45
                        period = 1
                    elif "+" in short:
                        minuto = int(short.split("+")[0])
                        period = 1 if minuto <= 45 else 2
                    elif short.isdigit():
                        minuto = int(short)
                        period = 1 if minuto <= 45 else 2
                    else:
                        raise ValueError
                except:
                    # Fallback pelo statusId
                    minuto = 0
                    period = 1

                jogos.append({
                    "fid": fid, "fid_raw": str(mid),
                    "home": home.get("name", ""), "away": away.get("name", ""),
                    "sh": sh, "sa": sa, "minuto": minuto,
                    "period": period, "liga": liga_nome, "source": "fotmob"
                })

        print(f"[FotMob] {len(jogos)} novos jogos ao vivo")
        return jogos
    except Exception as e:
        print(f"[FotMob ERRO] {e}")
        return []


# ═══════════════════════════════════════════════════════════════════════════════
# FotMob: busca ID do jogo pelo nome dos times (cruzamento)
# ═══════════════════════════════════════════════════════════════════════════════
_FOTMOB_MATCH_CACHE = {}
def get_fotmob_match_id(home, away):
    """Busca o match ID do FotMob para um jogo pelos nomes dos times.
    Usa cache pra não bater na API toda hora."""
    import unicodedata
    def norm(s):
        return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower().strip()
    
    h_norm = norm(home)
    a_norm = norm(away)
    chave = f"{h_norm}|{a_norm}"
    
    if chave in _FOTMOB_MATCH_CACHE:
        return _FOTMOB_MATCH_CACHE[chave]
    
    try:
        from datetime import datetime as _dt
        hoje = _dt.now().strftime("%Y%m%d")
        r = requests.get(f"https://www.fotmob.com/api/data/matches?date={hoje}",
                         headers=FOTMOB_HEADERS, timeout=15)
        if r.status_code != 200:
            return None
        
        data = r.json()
        for league in data.get("leagues", []):
            for match in league.get("matches", []):
                m_home = norm(match.get("home", {}).get("name", ""))
                m_away = norm(match.get("away", {}).get("name", ""))
                # Match por nome (tenta correspondência exata ou parcial)
                if (h_norm == m_home and a_norm == m_away) or \
                   (h_norm in m_home and a_norm in m_away) or \
                   (m_home in h_norm and m_away in a_norm):
                    mid = str(match.get("id"))
                    _FOTMOB_MATCH_CACHE[chave] = mid
                    print(f"[FotMob-ID] {home} x {away} -> matchId={mid}")
                    return mid
        return None
    except Exception as e:
        print(f"[FotMob-ID ERRO] {e}")
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# FotMob: estatísticas de um jogo específico (aceita match ID direto)
# ═══════════════════════════════════════════════════════════════════════════════
def get_stats_fotmob(fid):
    """Busca stats ao vivo via FotMob (API pública, sem chave).
    fid pode ser 'fotmob_XXXX' ou ID numérico direto.
    Nova estrutura: content.stats.Periods.All.stats (desde meados 2026)."""
    try:
        fid_raw = str(fid).replace("fotmob_", "").replace("bzz_", "")
        r = requests.get(f"https://www.fotmob.com/api/data/matchDetails?matchId={fid_raw}", headers=FOTMOB_HEADERS, timeout=15)
        if r.status_code != 200:
            return {}
        md = r.json()
        content = md.get("content", {})
        
        # NOVA estrutura: content.stats.Periods.All.stats
        # Antiga: content.matchFacts.stats.{firstHalf,secondHalf,fullTime}
        stats_container = content.get("stats", {})
        periods = stats_container.get("Periods", {})
        all_stats_list = []
        for period_name in ["All", "firstHalf", "secondHalf", "fullTime"]:
            if period_name in periods:
                top_stats = periods[period_name].get("stats", [])
                for item in top_stats:
                    inner = item.get("stats", [])
                    if isinstance(inner, list):
                        all_stats_list.extend(inner)
                break
        
        # Fallback: antiga estrutura
        if not all_stats_list:
            fotmob_stats = content.get("matchFacts", {}).get("stats", {})
            for p in ["fullTime", "secondHalf", "firstHalf"]:
                if p in fotmob_stats:
                    for sg in fotmob_stats[p]:
                        title = sg.get("title", "").lower()
                        items = sg.get("stats", [])
                        if len(items) >= 2:
                            all_stats_list.append({
                                "title": title,
                                "stats": [
                                    items[0].get("value", "0") if isinstance(items[0], dict) else items[0],
                                    items[1].get("value", "0") if isinstance(items[1], dict) else items[1]
                                ]
                            })
                    break
        
        if not all_stats_list:
            return {}
        
        stats = {}
        for stat_item in all_stats_list:
            title = stat_item.get("title", "").lower() if isinstance(stat_item, dict) else ""
            key = stat_item.get("key", "").lower() if isinstance(stat_item, dict) else ""
            raw_stats = stat_item.get("stats", []) if isinstance(stat_item, dict) else []
            if len(raw_stats) < 2:
                continue
            try:
                h_val = int(str(raw_stats[0] if not isinstance(raw_stats[0], dict) else raw_stats[0].get("value", "0")).replace("%", "").replace(",", "").strip() or "0")
                a_val = int(str(raw_stats[1] if not isinstance(raw_stats[1], dict) else raw_stats[1].get("value", "0")).replace("%", "").replace(",", "").strip() or "0")
            except:
                continue
            
            # Match por key (mais confiável) ou título
            if "corner" in key or "corner" in title:
                stats["escanteios_h"], stats["escanteios_a"] = h_val, a_val
            elif "shot" in key and "target" in key or ("shot" in title and "on" in title and "target" in title):
                stats["chutes_gol_h"], stats["chutes_gol_a"] = h_val, a_val
            elif "total" in key and "shot" in key or ("total shot" in title or ("shot" in title and "total" not in key and "on" not in title and "target" not in title)):
                stats["chutes_tot_h"] = max(stats.get("chutes_tot_h", 0), h_val)
                stats["chutes_tot_a"] = max(stats.get("chutes_tot_a", 0), a_val)
            elif "red" in key and "card" in key or "red card" in title:
                stats["red_cards_h"], stats["red_cards_a"] = h_val, a_val
            elif "possession" in key or "ball" in key or "possession" in title or "ball" in title:
                stats["posse_h"], stats["posse_a"] = h_val, a_val
            elif "danger" in key and "attack" in key or ("danger" in title and "attack" in title):
                stats["ataques_perigosos_h"], stats["ataques_perigosos_a"] = h_val, a_val
            elif "attack" in key or "attack" in title:
                stats["ataques_h"], stats["ataques_a"] = h_val, a_val
        
        if not stats.get("chutes_tot_h") and stats.get("chutes_gol_h"):
            stats["chutes_tot_h"] = stats["chutes_gol_h"]
            stats["chutes_tot_a"] = stats["chutes_gol_a"]
        for side in ["h", "a"]:
            for k in ["chutes_tot", "chutes_gol", "red_cards", "ataques", "ataques_perigosos", "posse"]:
                stats.setdefault(f"{k}_{side}", 0)
            stats.setdefault(f"escanteios_{side}", -1)
        print(f"[FotMob Stats] fid {fid} | chutes: {stats.get('chutes_tot_h',0)}x{stats.get('chutes_tot_a',0)} | atq_perig: {stats.get('ataques_perigosos_h',0)}x{stats.get('ataques_perigosos_a',0)} | esc: {stats.get('escanteios_h',0)}x{stats.get('escanteios_a',0)}")
        return stats
    except Exception as e:
        print(f"[FotMob Stats ERRO] {e}")
        return {}


    return get_stats_fotmob(match_id)

def get_stats_bzzoiro(fid_raw, home, away):
    """Busca estatísticas completas ao vivo da Bzzoiro v2.
    A API v2 retorna estruturas diferentes por tipo de liga:
    - Ligas principais (MX, USL, etc.): total_shots, shots_on_target, attack, dangerous_attack + shotmap
    - K League: attack, dangerous_attack, ball_safe (sem shots, sem corner_kicks)
    - Friendlies: corner_kicks, ball_possession, free_kicks (sem shots, sem ataques)
    Adapta-se ao que cada liga oferece."""
    try:
        headers = {"Authorization": "Token " + BZZOIRO_TOKEN}
        r = requests.get(f"{BZZOIRO_URL}/api/v2/events/{fid_raw}/stats/", headers=headers, timeout=10)
        data = r.json()
        raw_stats = data.get("stats", {})
        stats = {}
        any_nonzero = False

        for side, key in [("home", "h"), ("away", "a")]:
            side_data = raw_stats.get(side, {})
            if not isinstance(side_data, dict):
                continue

            # 1) Chutes — tenta total_shots direto (ligas principais), depois shotmap, depois 0
            shotmap = data.get("shotmap", [])
            total_shots_direct = int(side_data.get("total_shots", 0) or 0)
            on_target_direct = int(side_data.get("shots_on_target", 0) or 0)
            total_shots_sm = sum(1 for s in shotmap if s.get("team") == side)
            on_target_sm = sum(1 for s in shotmap if s.get("team") == side and s.get("on_target"))

            if total_shots_direct > 0:
                val, val_ot = total_shots_direct, on_target_direct
            elif total_shots_sm > 0:
                val, val_ot = total_shots_sm, on_target_sm
            else:
                val, val_ot = 0, 0

            stats[f"chutes_tot_{key}"] = val
            if val > 0: any_nonzero = True
            stats[f"chutes_gol_{key}"] = val_ot
            if val_ot > 0: any_nonzero = True

            # 2) Escanteios (formato friendlies e ligas principais)
            val = int(side_data.get("corner_kicks", 0) or 0)
            stats[f"escanteios_{key}"] = val
            if val > 0: any_nonzero = True

            # 3) Ataques perigosos (formato K League e ligas principais)
            val = int(side_data.get("dangerous_attack", 0) or 0)
            stats[f"ataques_perigosos_{key}"] = val
            if val > 0: any_nonzero = True

            # 4) Posse de bola (formato friendlies e ligas principais)
            val = int(side_data.get("ball_possession", 0) or 0)
            stats[f"posse_{key}"] = val
            if val > 0: any_nonzero = True

            # 5) Total de ataques (formato K League e ligas principais)
            val = int(side_data.get("attack", 0) or 0)
            stats[f"ataques_{key}"] = val
            if val > 0: any_nonzero = True

            # 6) Cartões vermelhos
            val = int(side_data.get("red_cards", 0) or 0)
            if val > 0:
                stats[f"red_cards_{key}"] = val
                any_nonzero = True

            # 7) Chutes bloqueados (info extra)
            val = int(side_data.get("blocked_shots", 0) or 0)
            if val > 0:
                stats[f"blocked_shots_{key}"] = val

        if not any_nonzero:
            return {}
        print(f"[BZZ Stats] {home} x {away} | chutes: {stats.get('chutes_tot_h',0)}/{stats.get('chutes_tot_a',0)} | atq_perig: {stats.get('ataques_perigosos_h',0)}x{stats.get('ataques_perigosos_a',0)} | esc: {stats.get('escanteios_h',0)}x{stats.get('escanteios_a',0)} | posse: {stats.get('posse_h',0)}%x{stats.get('posse_a',0)}%")
        return stats
    except: return {}

def get_stats_bzzoiro_by_name(home, away):
    """Fallback: busca stats no Bzzoiro pelo nome dos times."""
    import unicodedata
    def norm(s):
        return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower().strip()
    try:
        headers = {"Authorization": "Token " + BZZOIRO_TOKEN}
        hoje = datetime.now().strftime("%Y-%m-%d")
        url = f"{BZZOIRO_URL}/api/v2/events/?date_from={hoje}T00:00:00Z&date_to={hoje}T23:59:59Z&limit=200"
        r = requests.get(url, headers=headers, timeout=15)
        data = r.json()
        events = data.get("results", [])
        h_busca = norm(home)
        a_busca = norm(away)
        for ev in events:
            h_nome = norm(ev.get("home_team", ""))
            a_nome = norm(ev.get("away_team", ""))
            if (h_busca in h_nome or h_nome in h_busca) and (a_busca in a_nome or a_nome in a_busca):
                eid = ev.get("id")
                rs = requests.get(BZZOIRO_URL + f"/api/v2/events/{eid}/stats/", headers=headers, timeout=10)
                sd = rs.json()
                raw_stats = sd.get("stats", {})
                stats = {}
                for side_label, side_key in [("home", "h"), ("away", "a")]:
                    side_data = raw_stats.get(side_label, {})
                    stats[f"chutes_tot_{side_key}"] = int(side_data.get("total_shots", 0) or 0)
                    stats[f"chutes_gol_{side_key}"] = int(side_data.get("shots_on_target", 0) or 0)
                    stats[f"escanteios_{side_key}"] = int(side_data.get("corner_kicks", 0) or 0)
                    stats[f"ataques_perigosos_{side_key}"] = int(side_data.get("dangerous_attack", 0) or 0)
                    stats[f"posse_{side_key}"] = int(side_data.get("ball_possession", 0) or 0)
                    cards = side_data.get("cards", {})
                    if isinstance(cards, dict):
                        stats[f"red_cards_{side_key}"] = int(cards.get("red", 0) or 0)
                if stats.get("chutes_tot_h", 0) > 0 or stats.get("escanteios_h", -1) >= 0:
                    print(f"[BZZ-NAME] Stats por nome OK: {ev.get('home_team')}x{ev.get('away_team')} | esc {stats.get('escanteios_h')}x{stats.get('escanteios_a')}")
                    return stats
        return {}
    except Exception as e:
        print(f"[BZZ-NAME] Erro: {e}")
        return {}



def get_favorito_odds(home, away, fid=None, league=None):
    """Retorna ('h'|'a', odd_h, odd_a) baseado na menor odd. Usa Bzzoiro primeiro."""
    # Tenta Bzzoiro odds (principal)
    if fid and str(fid).startswith("bzz_"):
        try:
            fid_raw = str(fid).replace("bzz_", "")
            headers = {"Authorization": "Token " + BZZOIRO_TOKEN}
            r = requests.get(BZZOIRO_URL + f"/api/v2/events/{fid_raw}/odds/", headers=headers, timeout=8)
            if r.status_code == 200:
                bz = r.json().get("odds", {})
                odd_h = float(bz.get("home_win", 0) or 0)
                odd_a = float(bz.get("away_win", 0) or 0)
                if odd_h > 1 and odd_a > 1:
                    fav = "h" if odd_h <= odd_a else "a"
                    print(f"[ODDS-BZZ] {home} x {away} | Casa:{odd_h} Fora:{odd_a} -> Fav:{fav}")
                    return (fav, odd_h, odd_a)
        except Exception as e:
            print(f"[ODDS-BZZ] Erro: {e}")

    # Fallback: The Odds API
    try:
        r = requests.get("https://api.the-odds-api.com/v4/sports/soccer/odds/",
                         params={"apiKey": ODDS_API_KEY, "regions": "eu",
                                 "markets": "h2h", "oddsFormat": "decimal"}, timeout=10)
        if r.status_code == 200:
            for evento in r.json():
                nomes = [evento.get("home_team","").lower(), evento.get("away_team","").lower()]
                if home.lower() in nomes and away.lower() in nomes:
                    for book in evento.get("bookmakers", []):
                        for mkt in book.get("markets", []):
                            if mkt["key"] == "h2h":
                                outcomes = {o["name"].lower(): o["price"] for o in mkt["outcomes"]}
                                odd_h = outcomes.get(home.lower(), 99)
                                odd_a = outcomes.get(away.lower(), 99)
                                fav = "h" if odd_h <= odd_a else "a"
                                print(f"[ODDS-API] {home} x {away} | Casa:{odd_h} Fora:{odd_a} → Fav:{fav}")
                                return (fav, odd_h, odd_a)
    except:
        pass
    return (None, None, None)

# ═══════════════════════════════════════════════════════════════════════════════
# FILTRO DE JANELAS
# ═══════════════════════════════════════════════════════════════════════════════
def get_odd_favorito_num(home, away, fid=None, league=None, fid_raw=None):
    """Retorna a odd decimal do favorito (numero). Usa Bzzoiro primeiro, depois Odds API."""
    # Tenta Bzzoiro odds (principal)
    if fid and str(fid).startswith("bzz_"):
        try:
            fid_raw = str(fid).replace("bzz_", "")
            headers = {"Authorization": "Token " + BZZOIRO_TOKEN}
            r = requests.get(BZZOIRO_URL + f"/api/v2/events/{fid_raw}/odds/", headers=headers, timeout=8)
            if r.status_code == 200:
                bz = r.json().get("odds", {})
                odd_h = float(bz.get("home_win", 0) or 0)
                odd_a = float(bz.get("away_win", 0) or 0)
                if odd_h > 1 and odd_a > 1:
                    return min(odd_h, odd_a)
        except:
            pass
    # Fallback: The Odds API
    try:
        r = requests.get("https://api.the-odds-api.com/v4/sports/soccer/odds/",
                         params={"apiKey": ODDS_API_KEY, "regions": "eu",
                                 "markets": "h2h", "oddsFormat": "decimal"}, timeout=10)
        if r.status_code == 200:
            for evento in r.json():
                nomes = [evento.get("home_team","").lower(), evento.get("away_team","").lower()]
                if home.lower() in nomes and away.lower() in nomes:
                    for book in evento.get("bookmakers", []):
                        for mkt in book.get("markets", []):
                            if mkt["key"] == "h2h":
                                outcomes = {o["name"].lower(): o["price"] for o in mkt["outcomes"]}
                                odd_h = outcomes.get(home.lower(), 99)
                                odd_a = outcomes.get(away.lower(), 99)
                                return min(odd_h, odd_a)
    except:
        pass
    return 99

def calcular_prob_gols_ht(chutes_tot, chutes_gol, minuto):
    """Estima prob de gols usando taxa de chutes como proxy de xG."""
    import math as _math
    taxa_conversao = 0.10
    xg = chutes_gol * taxa_conversao + chutes_tot * 0.04
    min_restantes_ht = max(45 - minuto, 1)
    min_restantes_ft = max(90 - minuto, 1)
    taxa_por_min = xg / max(minuto, 1)
    xg_rest_ht = taxa_por_min * min_restantes_ht
    xg_rest_ft = taxa_por_min * min_restantes_ft
    xg_total_ft = xg + xg_rest_ft
    prob_05_ht = round((1 - _math.exp(-max(xg_rest_ht, 0.05))) * 100, 1)
    prob_15_ft = round((1 - _math.exp(-max(xg_total_ft - 1, 0.1))) * 100, 1)
    return prob_15_ft, prob_05_ht

def filtrar_janelas(jogos):
    resultado = []
    for j in jogos:
        m = j["minuto"]
        p_raw = j["period"]
        if isinstance(p_raw, str):
            p = 2 if '2' in p_raw else 1
        else:
            p = p_raw
            
        em_janela = (
            (p == 1 and 15 <= m <= 27) or
            (p == 1 and 28 <= m <= 38) or
            (p == 2 and 55 <= m <= 77) or
            (p == 2 and 78 <= m <= 88)
        )
        if em_janela:
            resultado.append(j)
    return resultado

# ═══════════════════════════════════════════════════════════════════════════════
# MENSAGEM PADRÃO
# ═══════════════════════════════════════════════════════════════════════════════
def gerar_motivo(mercado, stats, sh, sa, fav_final, minuto, cantos_atual=0):
    chutes_h          = stats.get("chutes_tot_h", 0) if stats else 0
    chutes_a          = stats.get("chutes_tot_a", 0) if stats else 0
    chutes_gol_h      = stats.get("chutes_gol_h", 0) if stats else 0
    chutes_gol_a      = stats.get("chutes_gol_a", 0) if stats else 0
    cantos_h          = max(0, stats.get("escanteios_h", 0)) if stats else 0
    cantos_a          = max(0, stats.get("escanteios_a", 0)) if stats else 0
    red_h             = stats.get("red_cards_h", 0) if stats else 0
    red_a             = stats.get("red_cards_a", 0) if stats else 0
    posse_h_raw       = stats.get("posse_h", 0.0) if stats else 0.0
    posse_a_raw       = stats.get("posse_a", 0.0) if stats else 0.0
    atq_perig_h       = stats.get("ataques_perigosos_h", 0) if stats else 0
    atq_perig_a       = stats.get("ataques_perigosos_a", 0) if stats else 0
    posse_h = int(round(float(posse_h_raw) * 100)) if float(posse_h_raw) <= 1 else int(round(float(posse_h_raw)))
    posse_a = int(round(float(posse_a_raw) * 100)) if float(posse_a_raw) <= 1 else int(round(float(posse_a_raw)))
    total_chutes      = chutes_h + chutes_a
    total_cantos      = cantos_h + cantos_a
    total_atq_perig   = atq_perig_h + atq_perig_a
    tem_dados         = total_chutes > 0 or total_cantos > 0 or total_atq_perig > 0

    if not tem_dados:
        return "Estatísticas não disponíveis para esta liga"

    # Labels
    if fav_final == "h":
        fav_label   = "Favorito"
        zebra_label = "Zebra"
        fav_chutes  = chutes_h; fav_gol = chutes_gol_h
        adv_chutes  = chutes_a; adv_gol = chutes_gol_a
        fav_atq     = atq_perig_h
        adv_atq     = atq_perig_a
    elif fav_final == "a":
        fav_label   = "Favorito"
        zebra_label = "Zebra"
        fav_chutes  = chutes_a; fav_gol = chutes_gol_a
        adv_chutes  = chutes_h; adv_gol = chutes_gol_h
        fav_atq     = atq_perig_a
        adv_atq     = atq_perig_h
    else:
        fav_label   = "Casa"
        zebra_label = "Fora"
        fav_chutes  = chutes_h; fav_gol = chutes_gol_h
        adv_chutes  = chutes_a; adv_gol = chutes_gol_a
        fav_atq     = atq_perig_h
        adv_atq     = atq_perig_a

    jogo_aberto    = sh == 0 and sa == 0
    fav_perdendo   = (fav_final == "h" and sh < sa) or (fav_final == "a" and sa < sh)
    fav_ganhando   = (fav_final == "h" and sh > sa) or (fav_final == "a" and sa > sh)
    zebra_dominando = adv_chutes > fav_chutes
    minuto_seguro  = max(minuto, 1)
    fav_atq_por_min = round(fav_atq / minuto_seguro, 2)
    adv_atq_por_min = round(adv_atq / minuto_seguro, 2)
    fav_amassando   = fav_atq_por_min >= 0.70 and adv_atq_por_min < 0.70
    adv_amassando   = adv_atq_por_min >= 0.70 and fav_atq_por_min < 0.70
    ambos_pressionando = fav_atq_por_min >= 0.70 and adv_atq_por_min >= 0.70

    vermelho = ""
    if red_h > 0 or red_a > 0:
        vermelho = " 🟥 Vermelho: " + ("Casa" if red_h > 0 else "Fora")

    posse_txt = ""
    if posse_h >= 55:
        posse_txt = f", Casa com {posse_h}% de posse"
    elif posse_a >= 55:
        posse_txt = f", Fora com {posse_a}% de posse"

    # ════════════════════════════════════════════════════════════════
    # ALERTAS POR MERCADO — motivo da entrada
    # ════════════════════════════════════════════════════════════════

    if "CORNER" in mercado or "ESCANTEIO" in mercado:
        if "HT" in mercado:
            if total_atq_perig >= 12:
                return f"Pressão ofensiva muito alta no 1º tempo{vermelho}"
            elif total_atq_perig >= 8:
                return f"Pressão ofensiva elevada no 1º tempo{vermelho}"
            return f"Pressão ofensiva em crescimento no 1º tempo{vermelho}"
        else:
            if total_atq_perig >= 25:
                return f"Pressão ofensiva constante durante a partida{vermelho}"
            elif total_atq_perig >= 15:
                return f"Pressão ofensiva sustentada na partida{vermelho}"
            return f"Pressão ofensiva contínua na partida{vermelho}"

    if mercado == "HT":
        if chutes_gol_h >= 1 and chutes_gol_a >= 1:
            return f"Ambas equipes finalizando no alvo{vermelho}"
        if chutes_gol_h >= 1:
            return f"{fav_label if fav_final=='h' else 'Casa'} finalizando no alvo{vermelho}"
        if chutes_gol_a >= 1:
            return f"{fav_label if fav_final=='a' else 'Fora'} finalizando no alvo{vermelho}"
        if total_chutes >= 8:
            return f"Alta intensidade de chutes no 1º tempo{vermelho}"
        if fav_amassando:
            return f"{fav_label} dominando as ações ofensivas no 1º tempo{vermelho}"
        if ambos_pressionando:
            return f"Ambas equipes pressionando no campo de ataque{vermelho}"
        return f"Jogo movimentado com chances nos dois lados{vermelho}"

    if mercado == "LIMITEHT":
        if jogo_aberto and total_chutes >= 8:
            return f"Jogo aberto com muitas finalizações e sem gols{vermelho}"
        if fav_perdendo and fav_chutes >= 6:
            return f"{fav_label} perdendo e pressionando no campo ofensivo{vermelho}"
        if fav_amassando:
            return f"{fav_label} amassando em busca do empate{vermelho}"
        if total_atq_perig >= 8:
            return f"Alta pressão ofensiva nos minutos finais do 1º tempo{vermelho}"
        return f"Pressão ofensiva para gol antes do intervalo{vermelho}"

    if mercado == "BTTS":
        if chutes_gol_h >= 2 and chutes_gol_a >= 1:
            return f"Ambas equipes com finalizações no alvo{vermelho}"
        if fav_chutes >= 6 and adv_chutes >= 4:
            return f"Ambas equipes atacando com frequência{vermelho}"
        if ambos_pressionando:
            return f"Pressão ofensiva dos dois lados{vermelho}"
        if fav_amassando and adv_chutes >= 4:
            return f"{fav_label} dominando mas {zebra_label} também responde no ataque{vermelho}"
        return f"Ambas equipes com volume de ataque{vermelho}"

    if mercado == "OFT":
        if sh + sa == 1:
            return f"Placar em {sh}x{sa} com movimentação — {total_chutes} chutes | Mais um gol esperado para Over 1.5{vermelho}"
        if total_chutes >= 12:
            return f"Jogo com {total_chutes} finalizações — forte tendência de mais gols no 2º tempo{vermelho}"
        if ambos_pressionando:
            return f"Pressão total — {total_atq_perig} ataques perigosos | Over 1.5 FT com boa projeção{vermelho}"
        if total_atq_perig >= 10:
            return f"{total_atq_perig} ataques perigosos — placar deve se mover para Over 1.5{vermelho}"
        return f"Partida com bons números ofensivos — {total_chutes} chutes em {minuto}' | Over 1.5{vermelho}"

    if mercado == "OVERGOAL":
        if jogo_aberto:
            return f"Jogo 0x0 mas aberto — {total_chutes} chutes, {total_atq_perig} ataques perigosos | Gol esperado{vermelho}"
        if fav_amassando or adv_amassando:
            return f"Time amassando e placar ainda baixo — {total_atq_perig} atq. perigosos | Over Gol Partida{vermelho}"
        if total_atq_perig >= 12:
            return f"Pressão ofensiva muito alta — {total_atq_perig} ataques perigosos | Gol no FT{vermelho}"
        return f"Expectativa de gol com base no volume — {total_chutes} chutes, {total_atq_perig} ataques{vermelho}"

    # ── Fallback: análise geral (pra segurança) ──
    if jogo_aberto:
        if chutes_gol_h >= 3 and chutes_gol_a >= 3:
            return f"Jogo aberto com grandes chances de gol dos dois lados — {chutes_gol_h} finalizações de Casa, {chutes_gol_a} de Fora{posse_txt}{vermelho}"
        if fav_chutes >= 8 and fav_gol >= 3:
            return f"Jogo aberto, {fav_label} criando grandes chances — {fav_chutes} chutes, {fav_gol} no alvo{posse_txt}{vermelho}"
        if zebra_dominando and adv_chutes >= 6 and adv_gol >= 2:
            return f"Jogo aberto, {zebra_label} surpreendendo — {adv_chutes} chutes, {adv_gol} no alvo{posse_txt}{vermelho}"
        if total_chutes >= 12:
            return f"Jogo aberto e bastante movimentado — {chutes_h} chutes de Casa, {chutes_a} de Fora, sem gols ainda{posse_txt}{vermelho}"
        if fav_chutes > adv_chutes and fav_gol > 0:
            return f"Jogo aberto, {fav_label} dominando com {fav_chutes} chutes ({fav_gol} no alvo){posse_txt}{vermelho}"
        if fav_amassando:
            return f"Jogo aberto, {fav_label} amassando — {fav_atq} ataques perigosos x {adv_atq}{posse_txt}{vermelho}"
        if adv_amassando:
            return f"Jogo aberto, {zebra_label} pressionando muito — {adv_atq} ataques perigosos x {fav_atq}{posse_txt}{vermelho}"
        if ambos_pressionando:
            return f"Jogo aberto, ambas equipes pressionando forte — {total_atq_perig} ataques perigosos no total{posse_txt}{vermelho}"
        return f"Jogo aberto, ambas buscando o primeiro gol — {chutes_h} chutes x {chutes_a}{posse_txt}{vermelho}"

    if fav_perdendo:
        if fav_chutes >= 8 and fav_gol >= 3:
            return f"Grandes chances do {fav_label} empatar — chegando constantemente com {fav_chutes} chutes, {fav_gol} no alvo{posse_txt}{vermelho}"
        if fav_chutes >= 6 and fav_gol >= 2:
            return f"{fav_label} em busca do empate, criando boas chances — {fav_chutes} chutes, {fav_gol} no alvo{posse_txt}{vermelho}"
        if fav_amassando:
            return f"{fav_label} perdendo mas amassando! — {fav_atq} ataques perigosos x {adv_atq}{posse_txt}{vermelho}"
        if zebra_dominando and adv_chutes >= 8:
            return f"{zebra_label} dominando e ameaçando ampliar — {adv_chutes} chutes, {adv_gol} no alvo{posse_txt}{vermelho}"
        if adv_amassando:
            return f"{zebra_label} com mais volume de ataque — {adv_atq} ataques perigosos x {fav_atq}{posse_txt}{vermelho}"
        if ambos_pressionando:
            return f"Ambas pressionando — {total_atq_perig} ataques perigosos, jogo aberto{posse_txt}{vermelho}"
        if fav_chutes > adv_chutes:
            return f"{fav_label} em busca do empate, pressionando com {fav_chutes} chutes x {adv_chutes}{posse_txt}{vermelho}"
        return f"{fav_label} perdendo e tentando reagir — {fav_chutes} chutes x {adv_chutes} da {zebra_label}{posse_txt}{vermelho}"

    if fav_ganhando:
        if adv_chutes >= 8 and adv_gol >= 3:
            return f"{zebra_label} pressionando forte em busca do empate — {adv_chutes} chutes, {adv_gol} no alvo{posse_txt}{vermelho}"
        if adv_amassando:
            return f"{zebra_label} amassando mesmo perdendo — {adv_atq} ataques perigosos x {fav_atq}{posse_txt}{vermelho}"
        if fav_chutes >= 8:
            return f"{fav_label} controlando e ampliando a pressão — {fav_chutes} chutes, {fav_gol} no alvo{posse_txt}{vermelho}"
        if fav_amassando:
            return f"{fav_label} na frente e amassando — {fav_atq} ataques perigosos x {adv_atq}{posse_txt}{vermelho}"
        if ambos_pressionando:
            return f"Ambas pressionando, placar aberto — {total_atq_perig} ataques perigosos{posse_txt}{vermelho}"
        return f"{fav_label} vencendo, jogo controlado — {chutes_h} chutes de Casa x {chutes_a} de Fora{posse_txt}{vermelho}"

    if chutes_gol_h >= 3 and chutes_gol_a >= 3:
        return f"Jogo bastante movimentado, ambas chutando no alvo — {chutes_gol_h} finalizações de Casa, {chutes_gol_a} de Fora{posse_txt}{vermelho}"
    if chutes_h >= 8 and chutes_a >= 8:
        return f"Jogo intenso dos dois lados — {chutes_h} chutes de Casa, {chutes_a} de Fora{posse_txt}{vermelho}"
    if fav_chutes >= 8 and fav_gol >= 3:
        return f"{fav_label} chegando constantemente na área — {fav_chutes} chutes, {fav_gol} no alvo{posse_txt}{vermelho}"
    if zebra_dominando and adv_chutes >= 6:
        return f"{zebra_label} surpreendendo com mais volume — {adv_chutes} chutes ({adv_gol} no alvo) x {fav_chutes} do {fav_label}{posse_txt}{vermelho}"
    if fav_chutes > adv_chutes and fav_gol > 0:
        return f"{fav_label} criando mais chances — {fav_chutes} chutes ({fav_gol} no alvo) x {adv_chutes}{posse_txt}{vermelho}"
    if fav_amassando:
        return f"{fav_label} amassando em busca da virada — {fav_atq} ataques perigosos x {adv_atq}{posse_txt}{vermelho}"
    if adv_amassando:
        return f"{zebra_label} pressionando para virar — {adv_atq} ataques perigosos x {fav_atq}{posse_txt}{vermelho}"
    if ambos_pressionando:
        return f"Jogo eletrizante, ambas pressionando — {total_atq_perig} ataques perigosos{posse_txt}{vermelho}"
    if total_cantos >= 6:
        return f"Jogo bastante movimentado pelas laterais — {total_cantos} escanteios, {total_chutes} chutes{posse_txt}{vermelho}"
    return f"Jogo equilibrado, ambas criando chances — {chutes_h} chutes de Casa x {chutes_a} de Fora{posse_txt}{vermelho}"

def msg_universal(home, away, minuto, liga, n, mercado, entrada, placar, extra_val=None, cantos_atual=0, stats=None, sh=0, sa=0, fav_final="h", odd_h=None, odd_a=None, odd_b365=None, odd_bano=None):
    # Definir a entrada conforme os layouts das imagens
    if "CORNER" in mercado or "ESCANTEIO" in mercado:
        linha = cantos_atual + 0.5
        entrada = f"Mais de {linha}🚩"
    elif mercado in ("HT", "LIMITEHT", "BTTS", "OFT", "OVERGOAL"):
        if "Over" not in str(entrada) and "Ambas" not in str(entrada):
            if mercado == "OFT": entrada = "Over 1.5"
            elif mercado == "BTTS": entrada = "Ambas Marcam"
            elif mercado == "HT": entrada = "Over 0.5"
        entrada = f"{entrada}⚽️"

    # Extração de estatísticas
    chutes_h = stats.get("chutes_tot_h", 0) if stats else 0
    chutes_a = stats.get("chutes_tot_a", 0) if stats else 0
    alvo_h   = stats.get("chutes_gol_h", 0) if stats else 0
    alvo_a   = stats.get("chutes_gol_a", 0) if stats else 0
    cant_h   = stats.get("escanteios_h", 0) if stats else 0
    cant_a   = stats.get("escanteios_a", 0) if stats else 0
    atq_per_h = stats.get("ataques_perigosos_h", 0) if stats else 0
    atq_per_a = stats.get("ataques_perigosos_a", 0) if stats else 0
    
    # ════════════════════════════════════════════════════════════════
    # SISTEMA DE ALERTAS UNIFICADO
    # ════════════════════════════════════════════════════════════════
    # Cleubiano thresholds (APPM puro) — definem a intensidade da pressão
    # Zapia thresholds (APPM + mercado + stats) — refinam o contexto
    # ════════════════════════════════════════════════════════════════
    
    atq_max = max(atq_per_h, atq_per_a)
    appm_val = round(atq_max / minuto, 2) if minuto > 0 else 0
    
    # — Quem está pressionando —
    if atq_per_h > atq_per_a:
        quem = "do Mandante"
        dominante = home
    elif atq_per_a > atq_per_h:
        quem = "do Visitante"
        dominante = away
    else:
        quem = "de ambas equipes"
        dominante = "Ambos"
    
    periodo = "1º tempo" if minuto <= 45 else "2º tempo"
    
    # — Variáveis auxiliares —
    total_chutes = chutes_h + chutes_a
    total_alvo = alvo_h + alvo_a
    total_atq = atq_per_h + atq_per_a
    total_cant = cant_h + cant_a
    jogo_aberto = placar == "0x0"
    fav_nome = home if fav_final == "h" else (away if fav_final == "a" else "—")
    
    # ════════════════════════════════════════════════════════════════
    # THRESHOLDS CLEUBIANO — APPM PURO (ÚNICO SISTEMA DE ALERTA)
    # ════════════════════════════════════════════════════════════════
    if appm_val >= 2.0:
        alerta = "Partida Com Pressão Constante."
    elif appm_val >= 1.5:
        alerta = "Partida Pegando Fogo."
    elif appm_val >= 1.0:
        alerta = "Partida Com Ritmo Intenso."
    elif appm_val >= 0.8:
        alerta = f"Partida com pressão {quem}."
    elif appm_val >= 0.7:
        alerta = "Partida Com Ritmo Moderado."
    elif appm_val >= 0.5:
        alerta = "Partida Com Ritmo Médio."
    elif appm_val >= 0.3:
        alerta = "Partida Com Ritmo Fraco."
    else:
        alerta = "Partida Com Ritmo Muito Baixo."

    # APPM para exibição no layout
    appm = appm_val

    # Emojis EXATOS do print 1784355796901
    seta = "🚩" # No print é a seta vermelha que o Telegram renderiza como o emoji 🚩 ou similar
    seta_v = "🚩" 

    if "CORNER" in mercado or "ESCANTEIO" in mercado:
        nome_m = mercado.replace('CORNER_', 'ESCANTEIO ÁSIAT/LMT ')
        title = f"🚩🔥{nome_m}🔥🚩"
    else:
        titles_map = {
            "HT": "OVER GOL INTERVALO",
            "LIMITEHT": "OVER GOL LIMITE HT",
            "BTTS": "AMBAS MARCAM",
            "OFT": "OVER 1.5 GOLS PARTIDA",
            "OVERGOAL": "OVER GOL PARTIDA"
        }
        title = f"⚽️🔥{titles_map.get(mercado, mercado)}🔥⚽️"

    odd_rec = "1.70"
    sep = "━━━━━━━━━━━━━━━━━━━━"

    # Layout EXATO dos 6 templates - tudo em negrito, sem "OPORTUNIDADE IDENTIFICADA"
    msg = (
        f"{sep}\n"
        f"<b>{title}</b>\n"
        f"{sep}\n"
        f"<b>⚽️ Placar: {placar}</b>\n"
        f"<b>🌍 Liga: {liga}</b>\n"
        f"<b>📡 {home} x {away}</b>\n"
        f"<b>👀 ODDs: Casa {odd_h or '—'} / Fora {odd_a or '—'}</b>\n"
        f"<b>⏰️ Minuto: {minuto}'</b>\n"
        f"{sep}\n"
        f"<b>📊 Estatísticas ao Vivo da Partida:</b>\n"
        f"<b>🚀 Chutes Totais: {chutes_h} | {chutes_a}</b>\n"
        f"<b>🎯 Chutes No Alvo: {alvo_h} | {alvo_a}</b>\n"
        f"<b>⚔️ Ataques Perigosos: {atq_per_h} | {atq_per_a}</b>\n"
        f"<b>🚩 Escanteios: {cant_h} | {cant_a}</b>\n"
        f"{sep}\n"
        f"<b>💡 Análise Técnica da Partida:</b>\n"
        f"<b>🎯 Favorito: {fav_nome}</b>\n"
        f"<b>🔥 Pressão APPM:⚠️{appm}⚠️</b>\n"
        f"<b>🚨 Alerta: {alerta}</b>\n"
        f"{sep}\n"
        f"<b>📌 Entrada: {entrada}</b>\n"
        f"<b>💰 ODD Recomendada: {odd_rec}+</b>\n"
        f"{sep}\n"
        "<b>🔔Jogue com Responsabilidade🔔</b>"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🟣BET365🟣", "url": "https://www.bet365.bet.br/#/AX/"},
                {"text": "🔵PARIPESA🔵", "url": "https://paripesa.com/en/live/football/"}
            ]
        ]
    }
    return msg, keyboard
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🟣BET365🟣", "url": "https://www.bet365.bet.br/#/AX/"},
                {"text": "🔵PARIPESA🔵", "url": "https://paripesa.com/en/live/football/"}
            ]
        ]
    }
    
    return msg, keyboard

def checar_resultado(sinal):
    """Verifica se um sinal já enviado deu green ou red usando Bzzoiro."""
    try:
        eid_raw = str(sinal.get("fixture_id", "")).replace("bzz_", "")
        mercado = sinal.get("mercado")
        
        # 1. Busca detalhes do evento via Bzzoiro
        headers = {"Authorization": "Token " + BZZOIRO_TOKEN}
        r = requests.get(BZZOIRO_URL + f"/api/v2/events/{eid_raw}/", headers=headers, timeout=10)
        data = r.json()
        status = data.get("status", "")
        period = data.get("period", "")
        
        # Só audita se o jogo acabou ou se estamos checando HT e o jogo já está no 2T
        is_final = (status == "finished")
        is_2h = (status == "live" and period == "2H")
        
        if not (is_final or (mercado in ["HT", "LIMITEHT", "CORNER_HT"] and is_2h)):
            return None

        # Placar Final
        gh = int(data.get("home_score", 0) or 0)
        ga = int(data.get("away_score", 0) or 0)
        total_final = gh + ga

        # Placar HT
        gh_ht = int(data.get("home_score_ht", 0) or 0)
        ga_ht = int(data.get("away_score_ht", 0) or 0)
        total_ht = gh_ht + ga_ht

        # Lógica por Mercado
        if mercado in ["HT", "LIMITEHT"]:
            return "green" if total_ht >= 1 else ("red" if (is_2h or is_final) else None)
        
        elif mercado == "BTTS":
            return "green" if (gh >= 1 and ga >= 1) else ("red" if is_final else None)
        
        elif mercado == "OFT":
            return "green" if total_final >= 2 else ("red" if is_final else None)
            
        elif mercado == "OVERGOAL":
            gols_entrada = sinal.get("extra_val", 0)
            return "green" if total_final > gols_entrada else ("red" if is_final else None)
            
        elif mercado in ["CORNER_HT", "CORNER_FT"]:
            # Busca estatísticas de escanteios via Bzzoiro
            rs = requests.get(BZZOIRO_URL + f"/api/v2/events/{eid_raw}/stats/", headers=headers, timeout=10)
            sd = rs.json()
            raw_stats = sd.get("stats", {})
            esc_h = int(raw_stats.get("home", {}).get("corner_kicks", 0) or 0)
            esc_a = int(raw_stats.get("away", {}).get("corner_kicks", 0) or 0)
            c_final = esc_h + esc_a
            c_entrada = sinal.get("extra_val", 0)
            if c_final > c_entrada: return "green"
            return "red" if is_final else None

        return None
    except: return None




# ═══════════════════════════════════════════════════════════════════════════════
# COMANDOS TELEGRAM (/relatoriodiario e /radar)
# ═══════════════════════════════════════════════════════════════════════════════
def check_status_command(total_jogos_live=0, jogos_live=None, jogos_na_janela=None):
    import base64 as _b64
    last_id = 0
    # Lê last_update do GitHub para persistir entre execuções
    if GITHUB_TOKEN and GITHUB_REPO:
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/last_update.json"
            r = requests.get(url, headers=_github_headers(), timeout=6)
            if r.status_code == 200:
                last_id = json.loads(_b64.b64decode(r.json()["content"]).decode()).get("last_id", 0)
        except: pass
    elif os.path.exists(LAST_UPDATE_FILE):
        try:
            with open(LAST_UPDATE_FILE, 'r') as f: last_id = json.load(f).get("last_id", 0)
        except: pass
    try:
        sep = "━━━━━━━━━━━━━━━━━━━━"
        r   = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates",
                           params={"offset": last_id + 1, "timeout": 5}, timeout=10).json()
        if not r.get("ok"): return
        new_last_id = last_id
        radar_respondido = False
        relatorio_respondido = False
        agora_ts = datetime.now(timezone.utc).timestamp()
        for update in r.get("result", []):
            new_last_id = update["update_id"]
            msg     = update.get("message", {})
            text    = msg.get("text", "")
            chat_orig = msg.get("chat", {}).get("id", 0)
            msg_ts  = msg.get("date", 0)
            # Ignora comandos com mais de 30 minutos (evita processar acúmulo muito antigo)
            if agora_ts - msg_ts > 600: # Ignora comandos com mais de 10 minutos
                continue
            pass  # responde em qualquer chat
            if ("/relatoriomensal" in text or text.startswith("/relatoriomensal@")) and not relatorio_respondido:
                msg = enviar_relatorio_mensal()
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                              json={"chat_id": chat_orig, "text": msg, "parse_mode": "HTML"})
                relatorio_respondido = True
            if ("/relatoriodiario" in text or text.startswith("/relatoriodiario@")) and not relatorio_respondido:
                enviar_relatorio_diario()
                relatorio_respondido = True
            elif ("/mercados" in text or text.startswith("/mercados@")) and not relatorio_respondido:
                try:
                    # Se for "/mercados24h", chama o relatório 24h
                    if "/mercados24h" in text:
                        msg = enviar_relatorio_mercados24h()
                        if msg is None:
                            msg = "Ainda sem dados de mercado nas últimas 24h."
                    else:
                        msg = enviar_relatorio_performance()
                    if msg:
                        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                                      json={"chat_id": chat_orig, "text": msg, "parse_mode": "HTML"})
                    else:
                        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                                      json={"chat_id": chat_orig, "text": "Ainda sem dados de performance registrados.", "parse_mode": "HTML"})
                except Exception as e:
                    print(f"[PERFORMANCE] Erro: {e}")
                relatorio_respondido = True
            elif ("/radar" in text or text.startswith("/radar@")) and not radar_respondido:
                jogos_live = jogos_live or []
                jogos_na_janela = jogos_na_janela or []
                # Monta lista de jogos na janela
                if jogos_na_janela:
                    linhas_janela = ""
                    for j in jogos_na_janela:
                        h = j.get("home", "")
                        a = j.get("away", "")
                        m = j.get("minuto", 0)
                        sh = j.get("sh", 0)
                        sa = j.get("sa", 0)
                        liga = j.get("liga", "")
                        linhas_janela += f"🎯 <b>{h} x {a}</b> | {m}' | {sh}x{sa} | {liga}\n"
                else:
                    linhas_janela = "Nenhum jogo na janela no momento."
                # Monta lista de jogos ao vivo fora da janela (até 10)
                fora_janela = [j for j in jogos_live if j not in jogos_na_janela]
                if fora_janela:
                    linhas_fora = ""
                    for j in fora_janela[:10]:
                        h = j.get("home", "")
                        a = j.get("away", "")
                        m = j.get("minuto", 0)
                        sh = j.get("sh", 0)
                        sa = j.get("sa", 0)
                        linhas_fora += f"⏳ {h} x {a} | {m}' | {sh}x{sa}\n"
                    if len(fora_janela) > 10:
                        linhas_fora += f"... e mais {len(fora_janela)-10} jogos"
                else:
                    linhas_fora = "—"
                msg_radar = (
                    f"{sep}\n"
                    f"📡👉<b>RADAR DE JOGOS AO VIVO</b>👈📡\n"
                    f"{sep}\n"
                    f"🔴 <b>{total_jogos_live} jogos ao vivo</b>\n"
                    f"🎯 <b>{len(jogos_na_janela)} na janela alvo</b>\n"
                    f"{sep}\n"
                    f"🚨<b>JOGOS NO ALVO:</b>\n{linhas_janela}"
                    f"{sep}\n"
                    f"<b>⏳ FORA DA JANELA:</b>\n{linhas_fora}"
                    f"{sep}"
                )
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": chat_orig, "text": msg_radar, "parse_mode": "HTML"}, timeout=10)
                radar_respondido = True
        if new_last_id > last_id:
            with open(LAST_UPDATE_FILE, 'w') as f: json.dump({"last_id": new_last_id}, f)
            # Salva no GitHub para persistir entre execuções
            import base64 as _b64
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/last_update.json"
            r_get = requests.get(url, headers=_github_headers(), timeout=6)
            sha_lu = r_get.json().get("sha", "") if r_get.status_code == 200 else ""
            content_b64 = _b64.b64encode(json.dumps({"last_id": new_last_id}).encode()).decode()
            payload = {"message": "state: last_update [skip ci]", "content": content_b64}
            if sha_lu: payload["sha"] = sha_lu
            r_put = requests.put(url, headers=_github_headers(), json=payload, timeout=8)
            print(f"[CMD] last_id salvo: {new_last_id} | status: {r_put.status_code} | token_ok: {bool(GITHUB_TOKEN)}")
    except Exception as e:
        print(f"[CMD] Erro ao processar comandos: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# HISTÓRICO — Média de gols (desativado, sem apifootball)
# ═══════════════════════════════════════════════════════════════════════════════
_HIST_CACHE = {}
def get_media_gols_historica(home_id, away_id):
    """Retorna média histórica de gols. Desativado sem apifootball."""
    return -1.0

# ═══════════════════════════════════════════════════════════════════════════════
# LOOP PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════
def run():
    # ─── ISOLAMENTO POR REPOSITÓRIO: cada bot usa SÓ sua fonte ───
    _repo_atual = os.environ.get("GITHUB_REPOSITORY", "").lower()
    if "bot-bzzoiro" in _repo_atual:
        BOT_SOURCE = "bzzoiro"
    else:
        BOT_SOURCE = "fotmob"

    print(f"[Iniciando monitoramento — Fonte: {BOT_SOURCE.upper()} | Repo: {_repo_atual}]")
    sent      = load_sent()
    total_env = 0
    janela_id = datetime.now(BRT).strftime('%Y%m%d%H')

    # ─────────────────────────────────────────────────────────────
    # PASSO 1: Bzzoiro (principal) + FotMob (fallback)
    # ─────────────────────────────────────────────────────────────
    jogos_live = []
    jogos_live = get_jogos_bzzoiro(set())
    print(f"[Bzzoiro] {len(jogos_live)} jogos ao vivo")

    # Fallback: se Bzzoiro retornou poucos, complementa com FotMob
    if len(jogos_live) < 3:
        fids_bzz = {j["fid"] for j in jogos_live}
        jogos_fotmob = get_jogos_fotmob(fids_bzz)
        if jogos_fotmob:
            print(f"[FotMob] Complementando com {len(jogos_fotmob)} jogos")
            jogos_live.extend(jogos_fotmob)

    # PASSO 2: Filtra janelas alvo
    jogos_na_janela = filtrar_janelas(jogos_live)
    print(f"[Janela] {len(jogos_na_janela)} jogos nas janelas alvo")

    check_status_command(total_jogos_live=len(jogos_live), jogos_live=jogos_live, jogos_na_janela=jogos_na_janela)

    if not jogos_na_janela:
        print("[OK] Nenhum jogo na janela — aguardando próximo ciclo")
        save_sent(sent)
        print("Finalizado. Enviados: 0")
        return

    # PASSO 3: Dedup simples (dentro da própria fonte — remove duplicatas do mesmo jogo)
    jogos_dedup = []
    vistos_chaves = set()
    for j in jogos_na_janela:
        hn_j = norm_nome_time(j["home"])
        an_j = norm_nome_time(j["away"])
        chave = hashlib.md5(f"{hn_j}-{an_j}".encode()).hexdigest()[:16]
        if chave not in vistos_chaves:
            vistos_chaves.add(chave)
            jogos_dedup.append(j)
    print(f"[Dedup] {len(jogos_na_janela)} -> {len(jogos_dedup)} jogos unicos")
    
    for j in jogos_dedup:
        fid    = j["fid"]
        h, a   = j["home"], j["away"]
        # Normaliza nomes pra chave estável entre APIs diferentes
        hn = norm_nome_time(h)
        an = norm_nome_time(a)
        dedup_id = hashlib.md5(f"{hn}-{an}".encode()).hexdigest()[:12]
        m, p   = j["minuto"], j["period"]
        sh, sa = j["sh"], j["sa"]
        liga   = str(j["liga"])
        stot   = sh + sa
        placar = f"{sh}x{sa}"

        print(f"[Analisando] {h} x {a} | {placar} | {m}min")

        # ─── Stats: Bzzoiro (base) + FotMob (complemento) ───
        # Bzzoiro: ataques_perigosos, ataques, chutes, escanteios, posse (fonte principal)
        # FotMob: complementa chutes, escanteios, posse onde Bzzoiro não tem
        fid_raw = j.get("fid_raw", fid)
        stats = {}
        
        # 1) Bzzoiro: fonte PRINCIPAL (tem TUDO: ataques_perigosos, ataques, chutes, escanteios, posse)
        try:
            if fid_raw:
                sb = get_stats_bzzoiro(fid_raw, h, a)
                if isinstance(sb, dict) and sb:
                    stats = sb  # Bzzoiro é a BASE
                    print(f"[STATS-BZZ] {h} x {a} — Bzzoiro base (ataq_perig: {sb.get('ataques_perigosos_h',0)}x{sb.get('ataques_perigosos_a',0)} | chutes: {sb.get('chutes_tot_h',0)}x{sb.get('chutes_tot_a',0)} | esc: {sb.get('escanteios_h',0)}x{sb.get('escanteios_a',0)} | posse: {sb.get('posse_h',0)}%x{sb.get('posse_a',0)}%)")
        except: pass
        
        # 2) FotMob: só complementa campos que Bzzoiro não preencheu (chutes, escanteios, posse)
        # NUNCA sobrescreve ataques_perigosos ou ataques
        try:
            fm_id = get_fotmob_match_id(h, a)
            if fm_id:
                sa_fm = get_stats_fotmob(f"fotmob_{fm_id}")
                if isinstance(sa_fm, dict) and sa_fm:
                    for k, v in sa_fm.items():
                        if k.startswith("chutes") and v > 0 and stats.get(k, 0) == 0:
                            stats[k] = v
                        elif k.startswith("escanteios") and v >= 0:
                            # Aceita escanteios da FotMob se Bzzoiro não tem (0) ou tem negativo
                            if stats.get(k, -1) < 0 or v > stats.get(k, 0):
                                stats[k] = v
                        elif k.startswith("posse") and v > 0 and stats.get(k, 0) == 0:
                            stats[k] = v
                    print(f"[STATS-FM] {h} x {a} — FotMob complementou (chutes: {sa_fm.get('chutes_tot_h',0)}x{sa_fm.get('chutes_tot_a',0)} | esc: {sa_fm.get('escanteios_h',-1)}x{sa_fm.get('escanteios_a',-1)} | posse: {sa_fm.get('posse_h',0)}%x{sa_fm.get('posse_a',0)}%)")
        except: pass
        
        # 3) Se não tem stats de NENHUMA fonte, tenta Bzzoiro por nome
        if not stats:
            try:
                sb_name = get_stats_bzzoiro_by_name(h, a)
                if isinstance(sb_name, dict) and sb_name:
                    stats = sb_name
            except: pass
        
        # 4) Último fallback: FotMob com fid_raw
        if not stats:
            try:
                sa_fm = get_stats_fotmob(fid_raw)
                if isinstance(sa_fm, dict) and sa_fm: stats = sa_fm
            except: pass

        # Preenche defaults para campos que faltam
        for k in ["chutes_tot_h","chutes_tot_a","chutes_gol_h","chutes_gol_a"]:
            stats.setdefault(k, 0)
        for k in ["escanteios_h","escanteios_a"]:
            stats.setdefault(k, -1)
        for k in ["red_cards_h","red_cards_a"]:
            stats.setdefault(k, 0)

        if stats:
            print(f"[STATS-{BOT_SOURCE.upper()}] {h} x {a} | chutes: {stats.get('chutes_tot_h',0)}/{stats.get('chutes_tot_a',0)} | cantos: {stats.get('escanteios_h',-1)}/{stats.get('escanteios_a',-1)} | atq_perig: {stats.get('ataques_perigosos_h',0)}/{stats.get('ataques_perigosos_a',0)}")

        # Verifica se tem dados reais — sem stats E sem odds, pula o jogo
        tem_stats = stats and (
            stats.get("chutes_tot_h", 0) > 0 or
            stats.get("chutes_tot_a", 0) > 0 or
            stats.get("escanteios_h", -1) > 0 or
            stats.get("escanteios_a", -1) > 0 or
            stats.get("ataques_perigosos_h", 0) > 0 or
            stats.get("ataques_perigosos_a", 0) > 0
        )
        if not tem_stats:
            print(f"[SKIP] {h} x {a} — sem stats reais (chutes, cantos ou ataques perigosos) em nenhuma API, pulando jogo")
            continue

        # Favorito via odds: Bzzoiro (principal), sem fallback externo
        odd_h = j.get("odd_h")
        odd_a = j.get("odd_a")
        fav_por_odds = False

        if odd_h and odd_a and odd_h > 1 and odd_a > 1:
            fav_final = "h" if odd_h <= odd_a else "a"
            fav_por_odds = True
            print(f"[ODDS] {h} x {a} — odd Casa:{odd_h:.2f} Fora:{odd_a:.2f}")

        if not fav_por_odds:
            try:
                fav_t, odd_h, odd_a = get_favorito_odds(h, a, fid=j.get("fid"), league=liga)
                if fav_t:
                    fav_final = fav_t
                    fav_por_odds = True
            except: pass

        # Bzzoiro odds
        if not fav_por_odds:
            try:
                fav_final, odd_h, odd_a = get_favorito_odds(h, a, fid=fid)
                fav_por_odds = fav_final in ("h", "a")
                if fav_por_odds:
                    print(f"[ODDS-BZZ] {h} x {a} — Casa:{odd_h:.2f} Fora:{odd_a:.2f} Fav:{fav_final}")
            except: pass

        # Sem odds = usa stats (chutes) como fallback para definir favorito
        if not fav_por_odds:
            if stats and stats.get("fav_side") in ("h", "a"):
                fav_final = stats["fav_side"]
                print(f"[FAV-STATS] {h} x {a} — sem odds, favorito pelo chutes: {fav_final}")
            elif stats and (stats.get("chutes_tot_h", 0) > 0 or stats.get("chutes_tot_a", 0) > 0):
                fav_final = "h" if stats.get("chutes_tot_h", 0) >= stats.get("chutes_tot_a", 0) else "a"
                print(f"[FAV-STATS] {h} x {a} — sem odds, favorito pelo chutes: {fav_final}")
            else:
                fav_final = "h"
                print(f"[FAV-HOME] {h} x {a} — sem odds e sem stats, assumindo mandante como favorito")

        # Se NENHUMA fonte retornou odds válidas, pula o jogo
        if not (odd_h and odd_h > 1 and odd_a and odd_a > 1):
            print(f"[SKIP-SEM-ODDS] {h} x {a} — nenhuma odd válida (Casa:{odd_h} Fora:{odd_a}), pulando sinal")
            continue

        red_fav = stats.get(f"red_cards_{fav_final}", 0) if stats else 0

        # Placar do favorito e adversário
        fav_gols = sh if fav_final == "h" else sa
        adv_gols = sa if fav_final == "h" else sh

        # ─── DIAGNÓSTICO INICIAL DO JOGO ───
        print(f"[DIAG] {h} x {a} | placar={placar} | min={m} | periodo={p} | fav={fav_final} | gols_fav={fav_gols} gols_adv={adv_gols} | odds_casa={odd_h} odds_fora={odd_a} | chutes_totais={stats.get('chutes_tot_h',0)}x{stats.get('chutes_tot_a',0)} | chutes_gol={stats.get('chutes_gol_h',0)}x{stats.get('chutes_gol_a',0)} | atq_perig={stats.get('ataques_perigosos_h',0)}x{stats.get('ataques_perigosos_a',0)} | escanteios={stats.get('escanteios_h','?')}x{stats.get('escanteios_a','?')} | red_fav={red_fav}")

        # Favorito empatando = placar igual
        fav_empatando = (sh == sa)
        # Favorito perdendo por exatamente 1 gol — SOMENTE placares 0x1 ou 1x0 (total = 1 gol) — usado em OFT
        fav_perdendo_1 = (adv_gols - fav_gols) == 1 and (sh + sa) == 1
        # Favorito perdendo por exatamente 1 gol sem restrição de total — usado em escanteios e overgoal
        fav_perdendo_1_livre = (adv_gols - fav_gols) == 1
        # Condição escanteio: fav empatando OU perdendo por 1 (qualquer placar)
        corner_valido = fav_empatando or fav_perdendo_1_livre
        # Over 1.5 FT: placares válidos APENAS 1x0 ou 0x1 (fav perdendo por 1, total = 1 gol)
        fav_gols_oft = sh if fav_final == "h" else sa
        adv_gols_oft = sa if fav_final == "h" else sh
        oft_valido = (
            (adv_gols_oft - fav_gols_oft) == 1 and
            (sh + sa) == 1
        )

        # APPM — Ataques Perigosos Por Minuto (filtro geral anti-jogo morno)
        _aph_val = stats.get("ataques_perigosos_h", 0) if stats else 0
        _apa_val = stats.get("ataques_perigosos_a", 0) if stats else 0
        _apt_val = _aph_val + _apa_val
        _appm_total = round(_apt_val / m, 2) if m > 0 else 0
        _appm_h = round(_aph_val / m, 2) if m > 0 else 0
        _appm_a = round(_apa_val / m, 2) if m > 0 else 0
        # APPM seletiva por repositório
        # maquina-de-greens-bot (Grupo GITHUB): APPM ativo
        #   - OVER GOLS: casa ≥ 0.8 OU fora ≥ 0.8 OU total ≥ 1.5
        #   - ESCANTEIOS: casa ≥ 0.7 OU fora ≥ 0.7 OU total ≥ 1.4
        # boot-ia-inteligente-bot (Grupo ZAPIA): livre
        if BOT_SOURCE == "bzzoiro":
            # Bzzoiro tem ataques_perigosos, então APPM é válido
            appm_valido   = True
            appm_gols_ok  = True
            if not appm_valido:
                print(f"[APPM-BLOQUEADO] {h} x {a} — APPM casa={_appm_h} fora={_appm_a} total={_appm_total} (mín: 0.7/time ou 1.4 total)")
            if not appm_gols_ok:
                print(f"[APPM-GOLS-BLOQUEADO] {h} x {a} — APPM casa={_appm_h} fora={_appm_a} total={_appm_total} (mín: 0.8/time ou 1.5 total)")
        else:
            appm_valido   = True
            appm_gols_ok  = True

        # HISTÓRICO — Média de gols por partida (jogo todo) ≥ 2.0
        # Req. para: Over Gol HT, Over Gol FT e BTTS
        home_id = j.get("home_id", "")
        away_id = j.get("away_id", "")
        media_hist = 0.0
        if home_id and away_id:
            media_hist = get_media_gols_historica(home_id, away_id)
        # Bzzoiro usa IDs próprios, apifootball não reconhece → hist retorna 0.0
        # 0.0 = sem dados disponíveis (não bloqueia), igual ao -1.0
        hist_ok = media_hist < 0 or media_hist >= 2.0 or media_hist == 0.0
        if not hist_ok:
            print(f"[HIST-BLOQUEADO] {h} x {a} — média {media_hist:.1f} < 2.0, pulando mercados de gol")

        # MERCADO 1: OVER 0.5 HT (15-27 min, 0x0, favorito empatando, sem vermelho do fav, média hist ≥ 2.0)
        if p == 1 and 15 <= m <= 27:
            if not (sh == 0 and sa == 0):
                print(f"[DIAG-HT-BARRA] {h} x {a} — placar não é 0x0 ({placar}), pulando")
            elif not fav_empatando:
                print(f"[DIAG-HT-BARRA] {h} x {a} — favorito não empatando (fav={fav_final}, gols_fav={fav_gols} adv={adv_gols}), pulando")
            elif red_fav != 0:
                print(f"[DIAG-HT-BARRA] {h} x {a} — favorito com cartão vermelho ({red_fav}), pulando")
            elif not appm_gols_ok:
                print(f"[DIAG-HT-BARRA] {h} x {a} — APPM insuficiente (casa={_appm_h} fora={_appm_a} total={_appm_total}), pulando")
            elif not hist_ok:
                print(f"[DIAG-HT-BARRA] {h} x {a} — média histórica {media_hist:.1f} < 2.0, pulando")
            else:
                hoje = datetime.now(BRT).strftime('%Y%m%d')
                key = f"{dedup_id}_ht_{hoje}"
                if key in sent:
                    print(f"[DIAG-HT-DUP] {h} x {a} — já enviado hoje ({key}), pulando")
                else:
                    ob365 = j.get("odds_b365", {}).get("o+0.5") if j.get("odds_b365") else None
                    obano = j.get("odds_bano", {}).get("o+0.5") if j.get("odds_bano") else None
                    mid = send_telegram(msg_universal(h, a, m, liga, 3, "HT", "Over 0.5", placar, stats=stats, sh=sh, sa=sa, fav_final=fav_final, odd_h=odd_h, odd_a=odd_a, odd_b365=ob365, odd_bano=obano), marca=key, home=h, away=a, odd_b365_val=ob365, odd_bano_val=obano)
                    if mid:
                        sent.add(key); total_env += 1
                        registrar_sinal(fid, "HT", h, a, mid)

        # MERCADO 1B: OVER GOL LIMITE HT (15-27 min, 0x0, odd fav ≤ 1.80, prob 1.5 FT ≥ 60%, prob 0.5 HT ≥ 50%, APPM casa/fora ≥ 0.8)
        if p == 1 and 15 <= m <= 27 and sh == 0 and sa == 0 and red_fav == 0:
            fid_raw = j.get("fid_raw")
            odd_fav_num = get_odd_favorito_num(h, a, fid=fid, league=j.get("liga_slug", j.get("liga", "")), fid_raw=fid_raw)
            
            # Cálculo de probabilidades via chutes (se tiver)
            chutes_tot_total = (stats.get("chutes_tot_h", 0) + stats.get("chutes_tot_a", 0)) if stats else 0
            chutes_gol_total = (stats.get("chutes_gol_h", 0) + stats.get("chutes_gol_a", 0)) if stats else 0
            prob_15_ft, prob_05_ht = calcular_prob_gols_ht(chutes_tot_total, chutes_gol_total, m)
            
            # Fallback: se não tem stats de chutes nem ataques, usa odd do favorito como proxy
            if chutes_tot_total == 0 and odd_fav_num <= 1.80:
                prob_15_ft = max(prob_15_ft, 65)
                prob_05_ht = max(prob_05_ht, 55)
            
            print(f"[LIMITE-HT] {h} x {a} | odd_fav={odd_fav_num} | prob_15ft={prob_15_ft}% | prob_05ht={prob_05_ht}% | appm_casa={_appm_h} appm_fora={_appm_a}")
            
            # Diagnóstico detalhado
            limite_ht_ok = True
            if odd_fav_num > 1.80:
                print(f"[DIAG-LIMITEHT-BARRA] {h} x {a} — odd do favorito {odd_fav_num} > 1.80, pulando")
                limite_ht_ok = False
            elif prob_15_ft < 60:
                print(f"[DIAG-LIMITEHT-BARRA] {h} x {a} — prob 1.5 FT {prob_15_ft}% < 60%, pulando")
                limite_ht_ok = False
            elif prob_05_ht < 50:
                print(f"[DIAG-LIMITEHT-BARRA] {h} x {a} — prob 0.5 HT {prob_05_ht}% < 50%, pulando")
                limite_ht_ok = False
            elif not appm_gols_ok:
                print(f"[DIAG-LIMITEHT-BARRA] {h} x {a} — APPM gols insuficiente (casa={_appm_h} fora={_appm_a} total={_appm_total}), pulando")
                limite_ht_ok = False
            elif not hist_ok:
                print(f"[DIAG-LIMITEHT-BARRA] {h} x {a} — média histórica {media_hist:.1f} < 2.0, pulando")
                limite_ht_ok = False
            if limite_ht_ok:
                hoje = datetime.now(BRT).strftime('%Y%m%d')
                key = f"{dedup_id}_limiteht_{hoje}"
                if key not in sent:
                    ob365 = j.get("odds_b365", {}).get("o+0.5") if j.get("odds_b365") else None
                    obano = j.get("odds_bano", {}).get("o+0.5") if j.get("odds_bano") else None
                    mid = send_telegram(msg_universal(h, a, m, liga, 4, "LIMITEHT", "Over 0.5", placar, stats=stats, sh=sh, sa=sa, fav_final=fav_final, odd_h=odd_h, odd_a=odd_a, odd_b365=ob365, odd_bano=obano), marca=key, home=h, away=a, odd_b365_val=ob365, odd_bano_val=obano)
                    if mid:
                        sent.add(key); total_env += 1
                        registrar_sinal(fid, "LIMITEHT", h, a, mid)

        # MERCADO 2: AMBAS MARCAM BTTS (55-75 min, fav perdendo por 1, sem vermelho do fav, média hist ≥ 2.0)
        if p == 2 and 55 <= m <= 75 and ((sh == 1 and sa == 0) or (sh == 0 and sa == 1)):
            if not fav_perdendo_1:
                print(f"[DIAG-BTTS-BARRA] {h} x {a} — favorito não perdendo por 1 (fav_gols={fav_gols} adv={adv_gols}), pulando")
            elif red_fav != 0:
                print(f"[DIAG-BTTS-BARRA] {h} x {a} — favorito com cartão vermelho ({red_fav}), pulando")
            elif not appm_gols_ok:
                print(f"[DIAG-BTTS-BARRA] {h} x {a} — APPM insuficiente (casa={_appm_h} fora={_appm_a} total={_appm_total}), pulando")
            elif not hist_ok:
                print(f"[DIAG-BTTS-BARRA] {h} x {a} — média histórica {media_hist:.1f} < 2.0, pulando")
            else:
                hoje = datetime.now(BRT).strftime('%Y%m%d')
                key = f"{dedup_id}_btts_{hoje}"
                if key in sent:
                    print(f"[DIAG-BTTS-DUP] {h} x {a} — já enviado hoje, pulando")
                else:
                    ob365 = j.get("odds_b365", {}).get("bts_yes") if j.get("odds_b365") else None
                    obano = j.get("odds_bano", {}).get("bts_yes") if j.get("odds_bano") else None
                    mid = send_telegram(msg_universal(h, a, m, liga, 4, "BTTS", "Ambas Marcam", placar, stats=stats, sh=sh, sa=sa, fav_final=fav_final, odd_h=odd_h, odd_a=odd_a, odd_b365=ob365, odd_bano=obano), marca=key, home=h, away=a, odd_b365_val=ob365, odd_bano_val=obano)
                    if mid:
                        sent.add(key); total_env += 1
                        registrar_sinal(fid, "BTTS", h, a, mid)

        # MERCADO 3: OVER 1.5 FT (55-75 min, fav perdendo por 1, placar 1x0/0x1, sem vermelho do fav, média hist ≥ 2.0)
        if p == 2 and 55 <= m <= 75 and ((sh == 1 and sa == 0) or (sh == 0 and sa == 1)):
            if not fav_perdendo_1:
                print(f"[DIAG-OFT-BARRA] {h} x {a} — favorito não perdendo por 1 (fav_gols={fav_gols} adv={adv_gols}), pulando")
            elif red_fav != 0:
                print(f"[DIAG-OFT-BARRA] {h} x {a} — favorito com cartão vermelho ({red_fav}), pulando")
            elif not appm_gols_ok:
                print(f"[DIAG-OFT-BARRA] {h} x {a} — APPM insuficiente (casa={_appm_h} fora={_appm_a} total={_appm_total}), pulando")
            elif not hist_ok:
                print(f"[DIAG-OFT-BARRA] {h} x {a} — média histórica {media_hist:.1f} < 2.0, pulando")
            else:
                hoje = datetime.now(BRT).strftime('%Y%m%d')
                key = f"{dedup_id}_oft_{hoje}"
                mid = None
                if key in sent:
                    print(f"[DIAG-OFT-DUP] {h} x {a} — já enviado hoje, pulando")
                else:
                    ob365 = j.get("odds_b365", {}).get("o+1.5") if j.get("odds_b365") else None
                    obano = j.get("odds_bano", {}).get("o+1.5") if j.get("odds_bano") else None
                    mid = send_telegram(msg_universal(h, a, m, liga, 4, "OFT", "Over 1.5", placar, stats=stats, sh=sh, sa=sa, fav_final=fav_final, odd_h=odd_h, odd_a=odd_a, odd_b365=ob365, odd_bano=obano), marca=key, home=h, away=a, odd_b365_val=ob365, odd_bano_val=obano)
                if mid:
                    sent.add(key); total_env += 1
                    registrar_sinal(fid, "OFT", h, a, mid)

        # MERCADO 4: OVER GOL PARTIDA (55-75 min, placares 0x0/1x1/0x1/1x0, favorito empatando ou perdendo por 1, média hist ≥ 2.0)
        overgoal_valido = (fav_empatando or fav_perdendo_1)
        if p == 2 and 55 <= m <= 75:
            if not overgoal_valido:
                print(f"[DIAG-OVERGOAL-BARRA] {h} x {a} — favorito não empata nem perde por 1 (fav_empatando={fav_empatando} fav_perdendo_1={fav_perdendo_1}), pulando")
            elif red_fav != 0:
                print(f"[DIAG-OVERGOAL-BARRA] {h} x {a} — favorito com cartão vermelho ({red_fav}), pulando")
            elif not appm_gols_ok:
                print(f"[DIAG-OVERGOAL-BARRA] {h} x {a} — APPM insuficiente (casa={_appm_h} fora={_appm_a} total={_appm_total}), pulando")
            elif not hist_ok:
                print(f"[DIAG-OVERGOAL-BARRA] {h} x {a} — média histórica {media_hist:.1f} < 2.0, pulando")
            else:
                hoje = datetime.now(BRT).strftime('%Y%m%d')
                key = f"{dedup_id}_overgoal_{hoje}"
                # Linha dinâmica: sempre acima do total de gols atual
                total_gols = sh + sa
                if total_gols == 0:
                    linha_over = "Over 0.5"
                elif total_gols == 1:
                    linha_over = "Over 1.5"
                elif total_gols == 2:
                    linha_over = "Over 2.5"
                elif total_gols == 3:
                    linha_over = "Over 3.5"
                else:
                    linha_over = f"Over {total_gols + 0.5:.1f}"
                mid = None
                if key in sent:
                    print(f"[DIAG-OVERGOAL-DUP] {h} x {a} — já enviado hoje ({key}), pulando")
                else:
                    ob365 = j.get("odds_b365", {}).get("o+0.5") if j.get("odds_b365") else None
                    obano = j.get("odds_bano", {}).get("o+0.5") if j.get("odds_bano") else None
                    mid = send_telegram(msg_universal(h, a, m, liga, 4, "OVERGOAL", linha_over, placar, stats=stats, sh=sh, sa=sa, fav_final=fav_final, odd_h=odd_h, odd_a=odd_a, odd_b365=ob365, odd_bano=obano), marca=key, home=h, away=a, odd_b365_val=ob365, odd_bano_val=obano)
                if mid:
                    sent.add(key); total_env += 1
                    registrar_sinal(fid, "OVERGOAL", h, a, mid, extra_val=total_gols)

        # MERCADO 5: ESCANTEIO LIMITE HT (32-38 min, fav confirmado, empatando ou perdendo por 1, sem vermelho, APPM ≥ 1)
        if p == 1 and 32 <= m <= 38:
            corner_cond = (fav_empatando or fav_perdendo_1)
            if not corner_cond:
                print(f"[DIAG-CORNER-HT-BARRA] {h} x {a} — favorito não empata nem perde por 1 (fav_empatando={fav_empatando} fav_perdendo_1={fav_perdendo_1}), pulando")
            elif red_fav != 0:
                print(f"[DIAG-CORNER-HT-BARRA] {h} x {a} — favorito com cartão vermelho ({red_fav}), pulando")
            elif not appm_valido:
                print(f"[DIAG-CORNER-HT-BARRA] {h} x {a} — APPM insuficiente (casa={_appm_h} fora={_appm_a} total={_appm_total}, precisa ≥0.7/time ou ≥1.4 total), pulando")
            else:
                hoje = datetime.now(BRT).strftime('%Y%m%d')
                key = f"{dedup_id}_cht_{hoje}"
                cantos_h = stats.get("escanteios_h", -1) if stats else -1
                cantos_a = stats.get("escanteios_a", -1) if stats else -1
                cantos = (max(0, cantos_h) + max(0, cantos_a)) if (cantos_h >= 0 and cantos_a >= 0) else -1
                mid = None
                if cantos < 0:
                    print(f"[DIAG-CORNER-HT-BARRA] {h} x {a} — cantos={cantos} sem dados, pulando")
                elif key in sent:
                    print(f"[DIAG-CORNER-HT-DUP] {h} x {a} — já enviado hoje, pulando")
                else:
                    ob365_e = j.get("odds_b365", {}).get("o+0.5") if j.get("odds_b365") else None
                    obano_e = j.get("odds_bano", {}).get("o+0.5") if j.get("odds_bano") else None
                    mid = send_telegram(msg_universal(h, a, m, liga, 5, "CORNER_HT", "", placar, cantos_atual=cantos, stats=stats, sh=sh, sa=sa, fav_final=fav_final, odd_h=odd_h, odd_a=odd_a, odd_b365=ob365_e, odd_bano=obano_e), marca=key, home=h, away=a, odd_b365_val=ob365_e, odd_bano_val=obano_e)
                if mid:
                    sent.add(key); total_env += 1
                    registrar_sinal(fid, "CORNER_HT", h, a, mid, extra_val=cantos)

        # MERCADO 6: ESCANTEIO LIMITE FT (82-88 min, fav confirmado, empatando ou perdendo por 1, sem vermelho)
        if p == 2 and 82 <= m <= 88:
            corner_ft_cond = (fav_empatando or fav_perdendo_1)
            if not corner_ft_cond:
                print(f"[DIAG-CORNER-FT-BARRA] {h} x {a} — favorito não empata nem perde por 1 (fav_empatando={fav_empatando} fav_perdendo_1={fav_perdendo_1}), pulando")
            elif red_fav != 0:
                print(f"[DIAG-CORNER-FT-BARRA] {h} x {a} — favorito com cartão vermelho ({red_fav}), pulando")
            elif not appm_valido:
                print(f"[DIAG-CORNER-FT-BARRA] {h} x {a} — APPM insuficiente (casa={_appm_h} fora={_appm_a} total={_appm_total}), pulando")
            else:
                hoje = datetime.now(BRT).strftime('%Y%m%d')
                key = f"{dedup_id}_cft_{hoje}"
                cantos_h = stats.get("escanteios_h", -1) if stats else -1
                cantos_a = stats.get("escanteios_a", -1) if stats else -1
                if cantos_h >= 0 and cantos_a >= 0:
                    cantos = max(0, cantos_h) + max(0, cantos_a)
                else:
                    cantos = -1
                mid = None
                if cantos < 0:
                    print(f"[DIAG-CORNER-FT-BARRA] {h} x {a} — cantos={cantos} sem dados, pulando")
                elif key in sent:
                    print(f"[DIAG-CORNER-FT-DUP] {h} x {a} — já enviado hoje, pulando")
                else:
                    ob365_e = j.get("odds_b365", {}).get("o+0.5") if j.get("odds_b365") else None
                    obano_e = j.get("odds_bano", {}).get("o+0.5") if j.get("odds_bano") else None
                    mid = send_telegram(msg_universal(h, a, m, liga, 5, "CORNER_FT", "", placar, cantos_atual=cantos, stats=stats, sh=sh, sa=sa, fav_final=fav_final, odd_h=odd_h, odd_a=odd_a, odd_b365=ob365_e, odd_bano=obano_e), marca=key, home=h, away=a, odd_b365_val=ob365_e, odd_bano_val=obano_e)
                if mid:
                    sent.add(key); total_env += 1
                    registrar_sinal(fid, "CORNER_FT", h, a, mid, extra_val=cantos)

    save_sent(sent)

    # Validação de resultados pendentes — lê e salva via GitHub
    try:
        sinais_p = _load_sinais_github()
        rest = []
        for s in sinais_p:
            res = checar_resultado(s)
            if res:
                emoji = "🟢GREEN CONFIRMADO🟢" if res == "green" else "🔴RED CONFIRMADO🔴"
                send_telegram(emoji, reply_to=s.get("message_id"))
                salvar_resultado(res, mercado=s.get("mercado"))
                registrar_performance(s.get("mercado"), res)
            else:
                rest.append(s)
        _save_sinais_github(rest)
        print(f"[SINAIS] {len(sinais_p) - len(rest)} resultados confirmados, {len(rest)} ainda pendentes")
    except Exception as e:
        print(f"[SINAIS] Erro validação: {e}")

    # Processa comandos pendentes com dados reais
    try:
        processar_comandos_pendentes(TG_TOKEN, CHAT_ID, jogos_live, jogos_na_janela)
    except Exception as e:
        print(f"[CMD] Erro chamando comandos: {e}")
    # Processa comandos pendentes com dados reais
    try:
        processar_comandos_pendentes(TG_TOKEN, CHAT_ID, jogos_live, jogos_na_janela)
    except Exception as e:
        print(f"[CMD] Erro chamando comandos: {e}")
    # ═══════════════════════════════════════════════════════════════════════════
    # AUTO-DISPATCH: /relatoriodiario + /mercados24h às 23:55
    # ═══════════════════════════════════════════════════════════════════════════
    try:
        agora_hora = datetime.now(BRT)
        if agora_hora.hour == 23 and agora_hora.minute >= 55:
            print(f"[AUTO] 23:55 — disparando relatório diário + mercados 24h")
            enviar_relatorio_diario()
            msg_mercados = enviar_relatorio_mercados24h()
            if msg_mercados:
                send_telegram(msg_mercados)
    except Exception as e:
        print(f"[AUTO] Erro auto-dispatch: {e}")
    print(f"Finalizado. Enviados: {total_env}")



def processar_comandos_pendentes(token, chat_id, jogos_live=None, jogos_na_janela=None):
    """Processa comandos /relatoriodiario e /radar com checkpoint de update_id."""
    if jogos_live is None: jogos_live = []
    if jogos_na_janela is None: jogos_na_janela = []
    max_id = 0
    try:
        r = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", timeout=10).json()
        if r.get("ok"):
            for update in r.get("result", []):
                uid = update.get("update_id", 0)
                if uid > max_id: max_id = uid
                msg = update.get("message", {})
                text = (msg.get("text", "") or "").strip()
                chat_orig = msg.get("chat", {}).get("id", 0)
                sep = "━" * 20
                if "/radar" in text:
                    linhas_jan = ""
                    for j in jogos_na_janela:
                        h = j.get("home",""); a = j.get("away","")
                        m = j.get("minuto",""); sh = j.get("sh",0); sa = j.get("sa",0)
                        liga = j.get("liga","")
                        linhas_jan += f"\U0001f3af <b>{h} x {a}</b> | {m}' | {sh}x{sa} | {liga}\n"
                    if not linhas_jan:
                        linhas_jan = "Nenhum jogo na janela no momento."
                    fora = [j for j in jogos_live if j not in jogos_na_janela][:10]
                    linhas_fora = ""
                    for j in fora:
                        h = j.get("home",""); a = j.get("away","")
                        m = j.get("minuto",""); sh = j.get("sh",0); sa = j.get("sa",0)
                        linhas_fora += f"\u23f3 {h} x {a} | {m}' | {sh}x{sa}\n"
                    if not linhas_fora: linhas_fora = "\u2014"
                    msg_radar = (
                        f"{sep}\n"
                        f"📡👉<b>RADAR DE JOGOS AO VIVO</b>👈📡\n"
                        f"{sep}\n"
                        f"🔴 <b>{len(jogos_live)} jogos ao vivo</b>\n"
                        f"🎯 <b>{len(jogos_na_janela)} na janela alvo</b>\n"
                        f"{sep}\n"
                        f"🚨<b>JOGOS NO ALVO:</b>\n{linhas_jan}"
                        f"{sep}\n"
                        f"<b>⏳ FORA DA JANELA:</b>\n{linhas_fora}"
                        f"{sep}"
                    )
                    requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                  json={"chat_id": chat_orig, "text": msg_radar, "parse_mode": "HTML"})
                    print(f"[CMD] Radar respondido com {len(jogos_live)} jogos live, {len(jogos_na_janela)} na janela")
                elif "/relatoriomensal" in text:
                    try:
                        msg = enviar_relatorio_mensal()
                        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                      json={"chat_id": chat_orig, "text": msg, "parse_mode": "HTML"})
                    except Exception as e:
                        print(f"[REL-MENSAL] Erro: {e}")
                elif "/relatoriodiario" in text:
                    try: enviar_relatorio_diario()
                    except: pass
                elif "/mercados" in text:
                    try:
                        if "/mercados24h" in text:
                            msg = gerar_layout_mercados24h()
                        else:
                            msg = enviar_relatorio_performance()
                        if msg:
                            requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                          json={"chat_id": chat_orig, "text": msg, "parse_mode": "HTML"})
                        else:
                            requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                                          json={"chat_id": chat_orig, "text": "Ainda sem dados de performance registrados.", "parse_mode": "HTML"})
                    except Exception as e:
                        print(f"[PERFORMANCE] Erro: {e}")
        if max_id > 0:
            try:
                off = max_id
                requests.get(f"https://api.telegram.org/bot{token}/getUpdates?offset={off+1}", timeout=5)
            except: pass
    except Exception as e:
        print(f"[CMD] Erro processar comandos: {e}")
if __name__ == "__main__":
    run()
