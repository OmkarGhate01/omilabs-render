"""Shared paths, curriculum and pronunciation rules for the Omilabs bulk pipeline."""
import os, re, runpy

ROOT = "/home/claude/Bolna-AI-Masterclass/"
PROD = ROOT + "Production/"
PROJ = ROOT + "Video-Projects/omilabs-remotion/"
BUILD = PROD + "build/"
SPECS = PROD + "specs/"
FPS = 30

_ns = {}
exec(open(ROOT + "Documentation-Coverage/build_matrix.py").read().split("rows=[];seen=set()")[0].replace("import re, csv, collections", "import re"), _ns)
EPS = _ns["EPS"]  # (n, module, title)
MODULES = ["Foundations", "Agent Creation", "Graph Agents", "Speech and Models", "Telephony", "APIs and Development", "Tools and Automation", "Production", "Open Source"]
MODULE_N = {m: i + 1 for i, m in enumerate(MODULES)}
CURR = {n: (mod, title) for n, mod, title in EPS}


def spec_path(n):
    return SPECS + "ep%02d.py" % n


def load_spec(n):
    p = spec_path(n)
    if not os.path.exists(p):
        return None
    return runpy.run_path(p)["EP"]


def short_title(n):
    sp = load_spec(n)
    if sp:
        return sp.get("short") or CURR[n][1]
    return CURR[n][1]


PRON = [
    (r"\bIVRs\b", "I V Rs"), (r"\bIVR\b", "I V R"), (r"\bDTMF\b", "D T M F"), (r"\bLLMs\b", "L L Ms"), (r"\bLLM\b", "L L M"),
    (r"\bSTT\b", "S T T"), (r"\bTTS\b", "T T S"), (r"\bAPIs\b", "A P Is"), (r"\bAPI\b", "A P I"), (r"\bMCP\b", "M C P"),
    (r"\bCLI\b", "C L I"), (r"\bSDKs\b", "S D Ks"), (r"\bSDK\b", "S D K"), (r"\bJSON\b", "Jason"), (r"\bURLs\b", "U R Ls"),
    (r"\bURL\b", "U R L"), (r"\bUUIDs?\b", "U U I D"), (r"\bn8n\b", "n eight n"), (r"\bCal\.com\b", "Cal dot com"),
    (r"\bMake\.com\b", "Make dot com"), (r"\bAiSensy\b", "A I Sensy"), (r"\bBYOT\b", "B Y O T"), (r"\bBYOK\b", "B Y O K"),
    (r"\bRAG\b", "rag"), (r"\bASR\b", "A S R"), (r"\bE\.164\b", "E one six four"), (r"\bTTFA\b", "T T F A"),
    (r"\bPDFs\b", "P D Fs"), (r"\bPDF\b", "P D F"), (r"\bCSVs?\b", "C S V"), (r"\bHTTPS\b", "H T T P S"), (r"\bHTTP\b", "H T T P"),
    (r"\bSIP\b", "sip"), (r"\bOpenAI\b", "Open A I"), (r"\bElevenLabs\b", "Eleven Labs"), (r"\bAssemblyAI\b", "Assembly A I"),
    (r"\bDeepSeek\b", "Deep Seek"), (r"\bOpenRouter\b", "Open Router"), (r"\bGPT\b", "G P T"), (r"\bAWS\b", "A W S"),
    (r"\bCRMs\b", "C R Ms"), (r"\bCRM\b", "C R M"), (r"\bIPs\b", "I Ps"), (r"\bIP\b", "I P"), (r"\bIDs\b", "I Ds"), (r"\bID\b", "I D"),
    (r"\bUI\b", "U I"), (r"\bAI\b", "A I"), (r"\bOTP\b", "O T P"), (r"\bSMS\b", "S M S"), (r"\bTUI\b", "T U I"), (r"\bREST\b", "rest"),
    (r"\bCOD\b", "C O D"), (r"\bBFSI\b", "B F S I"), (r"\bVAD\b", "V A D"), (r"\bPSTN\b", "P S T N"), (r"\bDNC\b", "D N C"),
    (r"\bTRAI\b", "Try"), (r"\bms\b", "milliseconds"), (r"\bGhate\b", "Ghaatay"), (r"\bvs\.?\b", "versus"), (r"\bQA\b", "Q A"),
    (r"\bKPIs?\b", "K P I"), (r"\bOAuth\b", "O Auth"), (r"\bSSO\b", "S S O"), (r"\bTLS\b", "T L S"), (r"\bUTC\b", "U T C"),
    (r"\bISO\b", "I S O"), (r"\bDLT\b", "D L T"), (r"\bKYC\b", "K Y C"), (r"\bGST\b", "G S T"), (r"\bPAN\b", "pan"),
    (r"\bAPI's\b", "A P I's"), (r"\bWebRTC\b", "Web R T C"), (r"\bJS\b", "J S"), (r"\bnpm\b", "N P M"), (r"\bUSD\b", "U S D"),
    (r"\bINR\b", "I N R"), (r"\bSaaS\b", "sass"), (r"\bS2S\b", "speech to speech"), (r"\bPOST\b", "post"), (r"\bGET\b", "get"),
    (r"\bPATCH\b", "patch"), (r"\bPUT\b", "put"), (r"\bDELETE\b", "delete"), (r"\bv2\b", "v two"), (r"\bv1\b", "v one"),
    (r"\bTCPA\b", "T C P A"), (r"\bGDPR\b", "G D P R"), (r"\bHIPAA\b", "hippa"), (r"\bSOC\b", "sock"), (r"\bEC2\b", "E C two"),
    (r"\bVPC\b", "V P C"), (r"\bK8s\b", "kubernetes"), (r"\bCPU\b", "C P U"), (r"\bGPU\b", "G P U"),
    (r"\bCIN\b", "C I N"), (r"\bURN\b", "U R N"), (r"\bRBI\b", "R B I"), (r"\bSEBI\b", "Sebi"), (r"\bCOI\b", "C O I"),
    (r"\bLOA\b", "L O A"), (r"\bMOA\b", "M O A"), (r"\bPE\b", "P E"), (r"\bTM\b", "T M"), (r"\bXML\b", "X M L"),
    (r"\bGCP\b", "G C P"), (r"\bCI\b", "C I"), (r"\bjq\b", "J Q"), (r"\bTUI\b", "T U I"), (r"\bP90\b", "P ninety"), (r"\bExoPhone\b", "Exo phone"), (r"\bVobiz\b", "Vo biz"),
]


def spoken(text):
    t = text
    for a, b in PRON:
        t = re.sub(a, b, t)
    t = t.replace("_", " ").replace("`", "").replace("→", "to").replace("›", "then")
    return t
