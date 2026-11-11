# Long comparison videos (16:9, Hinglish, Madhur). Facts only from the sources listed per video.
import json, os, sys

def B(tag, v, d, say, hl=(), chip=""): return dict(tag=tag, v=v, d=d, say=say, hl=list(hl), chip=chip)
def CH(n, title, say, hl=(), chip=""): return B("CH%d" % n, "chapter", dict(num=n, title=title), say, hl, chip)

L = {}

# ─────────────── cmp001: ElevenLabs (ElevenAgents) vs Bolna ───────────────
# Sources: Bolna docs packets (agents overview, what-it-costs, choosing-providers, choosing-telephony, security,
#          language switching, open-source README) ; ElevenLabs docs (ElevenAgents overview, cost FAQ, tools,
#          language detection, telephony) ; elevenlabs.io/blog/eleven-v4 (v4 Turbo latency, 90+ languages).
L["cmp001"] = dict(
  series="AI COMPARISON", title="ElevenLabs vs Bolna: Voice AI Agent Ke Liye Kaunsa Best? (2026)",
  thumb=dict(a="ElevenLabs", b="Bolna", top="VOICE AI 2026", hook="INDIA ke liye KAUN?", accent="#F2542D", colorA="#111111", colorB="#2F6BFF"),
  tags=["elevenlabs vs bolna", "bolna ai", "elevenlabs agents", "voice ai agent", "ai calling agent india", "elevenagents"],
  beats=[
  B("HOOK", "hook", dict(brand="ElevenLabs vs Bolna", pill="VOICE AI AGENTS", stat="2", sub="platforms, 1 फैसला"),
    "Voice AI agent बनाना है, पर ElevenLabs लें या Bolna? आज साफ़ जवाब मिलेगा।", ["ElevenLabs", "Bolna", "जवाब"], "जवाब"),
  B("HOOK", "versus", dict(bad="गलत platform = बार-बार migration", good="सही platform = पहले दिन से सही setup"),
    "गलत platform चुना, तो बाद में पूरा setup दोबारा बनाना पड़ता है।", ["गलत", "दोबारा"], "गलत"),
  B("HOOK", "list", dict(items=["Building", "Phone calls", "Languages", "Pricing", "Privacy", "Open source"]),
    "हम छह चीज़ें compare करेंगे: building, calls, languages, pricing, privacy और open source।", ["छह", "compare"], "compare"),

  CH(1, "दोनों क्या हैं?", "पहले समझते हैं, दोनों असल में क्या हैं।", ["क्या"], "क्या"),
  B("WHAT", "duo", dict(a=dict(icon="wave", title="ElevenAgents", rows=[["By", "ElevenLabs"], ["Type", "agents platform"], ["Channels", "voice, text, multimodal"]]),
                         b=dict(icon="chat", title="Bolna", rows=[["Type", "voice AI agents"], ["Calls", "inbound, outbound, batch"], ["Focus", "phone + web"]]), accentB="#2F6BFF"),
    "ElevenAgents, ElevenLabs का agents platform है। Bolna एक voice AI agents platform है, phone और web calls के लिए।", ["ElevenAgents", "Bolna"], "Bolna"),
  B("WHAT", "flow", dict(nodes=["Build", "Deploy", "Monitor"]),
    "दोनों का flow same है: agent build करो, deploy करो, और calls monitor करो।", ["build", "deploy", "monitor"], "monitor"),
  B("TWIST", "versus", dict(bad="ElevenLabs या Bolna — एक ही", good="Bolna में ElevenLabs voice भी चुन सकते हो"),
    "मज़ेदार बात: Bolna के अंदर synthesizer में ElevenLabs की voice भी चुन सकते हो।", ["ElevenLabs", "voice"], "भी"),

  CH(2, "Agent बनाना", "Chapter दो: agent बनाना कितना आसान है।", ["आसान"], "आसान"),
  B("BOLNA BUILD", "card", dict(icon="bolt", title="Bolna Agent Studio", rows=[["Auto build", "use case बताओ"], ["Time", "5–8 min में call-ready"], ["Advanced", "graph agents"]]),
    "Bolna में Agent Studio है: use case बताओ, पाँच से आठ minute में call-ready agent।", ["Agent", "Studio", "पाँच"], "Studio"),
  B("BOLNA GRAPH", "flow", dict(nodes=["Node", "Routing rule", "Next node"]),
    "Complex calls के लिए graph agents: एक लंबे prompt की जगह nodes और routing rules।", ["graph", "nodes"], "graph"),
  B("EL BUILD", "card", dict(icon="cpu", title="ElevenAgents", rows=[["Builder", "dashboard + toolkit"], ["Flows", "visual workflow builder"], ["LLM", "choose या custom"]]),
    "ElevenAgents में dashboard, developer toolkit, और visual workflow builder मिलता है।", ["workflow", "builder"], "workflow"),
  B("EL KB", "list", dict(items=["Knowledge base + RAG", "Dynamic variables", "Testing और evals"]),
    "साथ में knowledge base with RAG, dynamic variables, और built-in testing।", ["knowledge", "RAG", "testing"], "RAG"),
  B("SCORE", "table", dict(title="Building", cols=["ElevenLabs", "Bolna"], rows=[
      dict(k="Quick start", v=["dashboard", "auto-build 5–8 min"], win=1),
      dict(k="Multi-step flows", v=["workflows", "graph agents"]),
      dict(k="Knowledge base", v=["RAG", "knowledge base"]),
      dict(k="Testing", v=["tests + evals", "test calls"], win=0)]),
    "Building में दोनों strong हैं। Bolna का auto-build तेज़ है, ElevenLabs का testing और evals गहरा है।", ["auto-build", "evals"], "evals"),

  CH(3, "Phone calls", "Chapter तीन: असली phone calls।", ["phone"], "phone"),
  B("BOLNA PHONE", "card", dict(icon="globe", title="Bolna telephony", rows=[["Plivo", "India + global (default)"], ["Exotel", "India, DLT built in"], ["Twilio", "US / global"], ["Vobiz", "India"]]),
    "Bolna में Plivo default है, साथ में Exotel, Twilio, Vobiz, और अपना SIP trunk भी।", ["Plivo", "Exotel", "SIP"], "Exotel"),
  B("BOLNA INDIA", "card", dict(icon="check", title="India extras", rows=[["Numbers", "140/160 series guide"], ["Batch", "CSV campaigns"], ["Transfer", "live human handoff"]]),
    "India के लिए 140 और 160 series numbers का guide, CSV से batch calls, और human transfer।", ["India", "batch"], "India"),
  B("EL PHONE", "card", dict(icon="globe", title="ElevenAgents telephony", rows=[["Twilio", "native integration"], ["SIP", "trunking"], ["Batch", "batch calls"]]),
    "ElevenAgents में Twilio native integration, SIP trunking, और batch calls हैं।", ["Twilio", "SIP"], "Twilio"),
  B("EL TOOLS", "list", dict(items=["Transfer to number", "Voicemail detection", "End call", "Language detection"]),
    "System tools भी हैं: transfer, voicemail detection, end call, और language detection।", ["voicemail", "transfer"], "voicemail"),
  B("SCORE", "table", dict(title="Phone calls", cols=["ElevenLabs", "Bolna"], rows=[
      dict(k="Indian carriers", v=["SIP / Twilio", "Plivo, Exotel, Vobiz"], win=1),
      dict(k="Own SIP trunk", v=["yes", "yes (BYOT)"]),
      dict(k="Batch calling", v=["yes", "yes (CSV)"]),
      dict(k="Human transfer", v=["system tool", "yes"])]),
    "India की phone calls में Bolna आगे है, क्योंकि Indian carriers सीधे मिलते हैं।", ["India", "Bolna"], "Bolna"),

  CH(4, "Languages और voice", "Chapter चार: languages और voice quality।", ["languages"], "languages"),
  B("EL VOICE", "stat", dict(value="90+", label="languages — Eleven v4 / v4 Turbo"),
    "ElevenLabs का नया v4 Turbo, नब्बे से ज़्यादा languages support करता है।", ["नब्बे", "v4"], "v4"),
  B("EL TURBO", "stat", dict(value="~100ms", label="v4 Turbo median inference"),
    "और v4 Turbo की median latency लगभग सौ milliseconds, voice agents के लिए बना है।", ["सौ", "milliseconds"], "Turbo"),
  B("BOLNA LANG", "stat", dict(value="40+", label="languages — Bolna agents"),
    "Bolna चालीस से ज़्यादा languages में calls करता है, और call के बीच language switch भी।", ["चालीस", "switch"], "switch"),
  B("BOLNA PROVIDERS", "card", dict(icon="cpu", title="Indian languages setup", rows=[["Transcriber", "Sarvam"], ["LLM", "gpt-5.4-mini"], ["Voice", "Sarvam"]]),
    "Bolna के docs Indian languages के लिए Sarvam transcriber और Sarvam voice suggest करते हैं।", ["Sarvam"], "Sarvam"),
  B("SCORE", "versus", dict(bad="Voice quality ही सब कुछ नहीं", good="Language + latency + provider choice देखो"),
    "Voice quality में ElevenLabs की पहचान है, provider choice में Bolna flexible है।", ["ElevenLabs", "flexible"], "flexible"),

  CH(5, "Pricing", "Chapter पाँच: पैसा कैसे कटता है।", ["पैसा"], "पैसा"),
  B("BOLNA PRICE", "card", dict(icon="wallet", title="Bolna pricing", rows=[["Voice AI", "flat per-minute (preferred models)"], ["Telephony", "carrier per minute"], ["Platform", "per-minute fee"], ["Wallet", "prepaid"]]),
    "Bolna में preferred models पे flat per-minute rate, ऊपर से telephony और platform fee, prepaid wallet से।", ["flat", "per-minute", "wallet"], "flat"),
  B("BOLNA COST", "list", dict(items=["Non-preferred model → variable rate", "लंबी calls", "Verbose LLM output", "Premium voices"]),
    "Cost बढ़ता है जब preferred list से बाहर का model चुनो, या calls लंबी हों।", ["preferred", "लंबी"], "preferred"),
  B("EL PRICE", "card", dict(icon="wallet", title="ElevenAgents pricing", rows=[["Agent बनाना", "free"], ["Voice calls", "per duration"], ["Silence >10s", "95% discount"], ["LLM", "अलग pass-through"]]),
    "ElevenLabs में agent बनाना free है, calls duration से charge होती हैं, और दस second से लंबी silence पे पचानवे percent discount।", ["free", "पचानवे"], "पचानवे"),
  B("PRICE TIP", "versus", dict(bad="सिर्फ per-minute rate देखना", good="Telephony + LLM + silence भी जोड़ो"),
    "Compare करते वक्त सिर्फ rate नहीं, telephony और LLM cost भी जोड़ो।", ["telephony", "LLM"], "LLM"),

  CH(6, "Privacy और open source", "Chapter छह: data कहाँ रहता है।", ["data"], "data"),
  B("BOLNA DATA", "card", dict(icon="lock", title="Bolna data residency", rows=[["Default", "US (us-east-1)"], ["India option", "Mumbai (ap-south-1)"], ["Enterprise", "on-premise"]]),
    "Bolna default में US में चलता है, पर Indian data residency, Mumbai servers पे, available है।", ["Mumbai", "India"], "Mumbai"),
  B("BOLNA OSS", "card", dict(icon="code", title="Bolna open source", rows=[["License", "MIT"], ["Run", "खुद host करो"], ["Setup", "Docker"]]),
    "और Bolna का open source version MIT license में है, Docker से खुद host कर सकते हो।", ["MIT", "Docker"], "MIT"),
  B("EL DATA", "card", dict(icon="lock", title="ElevenAgents access", rows=[["Auth", "custom authentication"], ["Deploy", "web, mobile, telephony"]]),
    "ElevenAgents में agent access के लिए custom authentication मिलता है।", ["authentication"], "authentication"),

  CH(7, "Final verdict", "अब final verdict।", ["verdict"], "verdict"),
  B("VERDICT", "verdict", dict(items=[dict(who="Bolna", when="India calling, Indian carriers, data residency, open source"),
                                       dict(who="ElevenLabs", when="Best voices, 90+ languages, web/app agents, low latency"),
                                       dict(who="दोनों", when="Bolna agent + ElevenLabs voice")]),
    "India में phone calling, Indian carriers या data residency चाहिए, तो Bolna। Global voices और web agents के लिए ElevenLabs। और चाहो तो दोनों साथ।", ["Bolna", "ElevenLabs", "दोनों"], "दोनों"),
  B("TABLE", "table", dict(title="Summary", cols=["ElevenLabs", "Bolna"], rows=[
      dict(k="India phone calls", v=["ok", "best"], win=1),
      dict(k="Voice + languages", v=["best", "provider choice"], win=0),
      dict(k="India data option", v=["check plan", "Mumbai servers"], win=1),
      dict(k="Open source", v=["no", "MIT"], win=1),
      dict(k="Testing / evals", v=["built-in", "test calls"], win=0)]),
    "ये रहा पूरा summary, screenshot ले लो।", ["screenshot"], "screenshot"),
  B("CTA", "cta", dict(title="Comment करो", follow="Omilabs"),
    "आप कौनसा use करोगे? Comment में लिखो, और ऐसे comparisons के लिए Omilabs subscribe करो।", ["Comment", "subscribe"], "Comment"),
  ])


# ─────────────── cmp004: Eleven v4 vs Eleven v3 ───────────────
# Sources: elevenlabs.io/docs overview/models (model ids, languages, latency), docs eleven-v4 page, blog eleven-v4.
L["cmp004"] = dict(
  series="AI COMPARISON", title="ElevenLabs v4 vs v3: Kya Sach Mein Upgrade Karna Chahiye? (2026)", music="ELEVENLABS V4",
  thumb=dict(a="Eleven v3", b="Eleven v4", top="ELEVENLABS 2026", hook="UPGRADE karo ya NAHI?", accent="#F2542D", colorA="#3B3B3B", colorB="#111111"),
  tags=["elevenlabs v4 vs v3", "eleven v4", "eleven v3", "elevenlabs new model", "ai voice", "text to speech"],
  beats=[
  B("HOOK", "hook", dict(brand="Eleven v4 vs v3", pill="TEXT TO SPEECH", stat="90+", sub="languages in v4"),
    "ElevenLabs v4 आ गया है। पर क्या v3 छोड़ना सही है? आज पूरा फर्क देखते हैं।", ["v4", "v3", "फर्क"], "फर्क"),
  B("HOOK", "list", dict(items=["Languages", "Voice cloning", "Accent", "Settings", "Speed"]),
    "पाँच चीज़ें compare करेंगे: languages, cloning, accent, settings और speed।", ["पाँच", "compare"], "compare"),
  CH(1, "Models", "पहले models के नाम समझो।", ["models"], "models"),
  B("IDS", "duo", dict(a=dict(icon="wave", title="Eleven v3", rows=[["Model ID", "eleven_v3"], ["Realtime", "v3 Conversational"], ["Latency", "~280 ms (conv.)"]]),
                       b=dict(icon="star", title="Eleven v4", rows=[["Model ID", "eleven_v4"], ["Realtime", "v4 Turbo"], ["Latency", "~100 ms (Turbo)"]]), accentB="#111111"),
    "v3 का realtime version v3 Conversational है, करीब दो सौ अस्सी milliseconds। v4 का realtime version v4 Turbo है, करीब सौ milliseconds।", ["Conversational", "Turbo"], "Turbo"),
  B("GEN", "card", dict(icon="star", title="Docs के मुताबिक", rows=[["v4", "नई generation का पहला model"], ["Upgrade", "almost every case में बेहतर"]]),
    "Docs कहते हैं: v4 नई generation का पहला model है, और ज़्यादातर cases में v3 से बेहतर।", ["generation", "बेहतर"], "बेहतर"),
  CH(2, "Languages", "Chapter दो: languages।", ["languages"], "languages"),
  B("LANG", "table", dict(title="Languages", cols=["Eleven v3", "Eleven v4"], rows=[
      dict(k="Model", v=["70+", "90+"], win=1), dict(k="Realtime model", v=["70+", "90+"], win=1)]),
    "Docs के मुताबिक v3 सत्तर से ज़्यादा, और v4 नब्बे से ज़्यादा languages support करता है।", ["सत्तर", "नब्बे"], "नब्बे"),
  B("ACCENT", "versus", dict(bad="v3: दूसरी language में source accent आ सकता है", good="v4: दूसरी language में fluent, native accent"),
    "v4 का बड़ा बदलाव: अगर voice किसी और language की है, तो v4 target language में native accent में बोलता है।", ["native", "accent"], "native"),
  B("ACCENT2", "card", dict(icon="globe", title="Native accent handling", rows=[["Same language", "accent वही"], ["Other language", "fluent, natural"], ["Toggle", "अभी नहीं"]]),
    "Same language में accent वही रहता है। ये अभी हमेशा on है, toggle नहीं है।", ["toggle"], "toggle"),
  CH(3, "Voice cloning", "Chapter तीन: voice cloning।", ["cloning"], "cloning"),
  B("CLONE", "card", dict(icon="mic", title="v4 cloning", rows=[["Instant clone", "ज़्यादा accurate"], ["Professional clone", "supported"], ["Source audio", "पहले से ज़्यादा important"]]),
    "v4 में instant voice clone ज़्यादा accurate है, और professional clone भी supported है।", ["accurate", "professional"], "accurate"),
  B("CLONE2", "versus", dict(bad="Noisy recording → noise भी copy", good="Clean, एक ही speaking style"),
    "पर ध्यान दो: v4 इतना accurate है कि recording की गलतियाँ भी copy कर लेता है।", ["गलतियाँ", "copy"], "copy"),
  B("CLONE3", "card", dict(icon="mic", title="Recording tip", rows=[["Audio", "clear, clean"], ["Style", "एक ही speaking style"], ["PVC", "rolling out"]]),
    "Tip: clean audio दो और एक ही speaking style रखो। Professional clone support अभी rolling out है।", ["clean", "style"], "clean"),
  CH(4, "Settings", "Chapter चार: settings में क्या बदला।", ["settings"], "settings"),
  B("SET", "card", dict(icon="edit", title="v4 settings", rows=[["Stability", "yes"], ["Similarity", "yes"], ["Style / Speed", "नहीं"], ["SSML", "नहीं"]]),
    "v4 में सिर्फ Stability और Similarity हैं। Style और Speed slider नहीं, और SSML support नहीं।", ["Stability", "Similarity", "SSML"], "SSML"),
  B("TAGS", "list", dict(items=["[whispering]", "[shouting]", "[laughing]", "Natural language direction"]),
    "Delivery के लिए audio tags use करो, जैसे whispering, shouting, laughing।", ["tags", "whispering"], "tags"),
  CH(5, "Verdict", "तो upgrade करें या नहीं?", ["upgrade"], "upgrade"),
  B("DOCS", "versus", dict(bad="बिना test किए पूरा switch", good="अपनी voice पे दोनों compare करो"),
    "ElevenLabs खुद कहता है: v4 ज़्यादातर cases में बेहतर है, पर अपनी voice पे दोनों test करो।", ["test", "बेहतर"], "test"),
  B("VERDICT", "verdict", dict(items=[dict(who="Eleven v4", when="नई languages, native accent, better clones"),
                                       dict(who="Eleven v3", when="जब पुरानी voice का sound ही चाहिए")]),
    "नया project है तो v4। पुरानी voice का exact sound चाहिए, तो v3 पे test करके decide करो।", ["v4", "v3"], "v4"),
  B("CTA", "cta", dict(title="Comment करो", follow="Omilabs"),
    "आपको कौनसा अच्छा लगा? Comment करो, और Omilabs subscribe करो।", ["Comment", "subscribe"], "Comment"),
  ])

# ─────────────── cmp005: Eleven v4 vs v4 Turbo ───────────────
L["cmp005"] = dict(
  series="AI COMPARISON", title="Eleven v4 vs v4 Turbo: Quality Ya Speed? Kaunsa Chunein (2026)", music="ELEVENLABS V4",
  thumb=dict(a="v4", b="v4 Turbo", top="ELEVENLABS 2026", hook="QUALITY ya SPEED?", accent="#F2542D", colorA="#111111", colorB="#FF5A1F"),
  tags=["eleven v4 turbo", "eleven v4", "elevenlabs turbo", "voice agent latency", "elevenlabs models", "ai voice"],
  beats=[
  B("HOOK", "hook", dict(brand="v4 vs v4 Turbo", pill="ELEVENLABS", stat="100", sub="ms median (Turbo)"),
    "Eleven v4 और v4 Turbo, नाम same, काम अलग। गलत चुना तो या quality जाएगी या speed।", ["Turbo", "quality", "speed"], "speed"),
  CH(1, "दोनों क्या हैं", "पहले दोनों को समझो।", ["समझो"], "समझो"),
  B("DUO", "duo", dict(a=dict(icon="star", title="Eleven v4", rows=[["ID", "eleven_v4"], ["Focus", "highest quality"], ["Best", "content, audiobooks"]]),
                       b=dict(icon="bolt", title="v4 Turbo", rows=[["ID", "eleven_v4_turbo"], ["Focus", "low latency"], ["Best", "voice agents"]]), accentB="#FF5A1F"),
    "v4 highest quality के लिए, content और audiobooks। v4 Turbo low latency के लिए, voice agents।", ["quality", "latency"], "latency"),
  B("SAME", "list", dict(items=["Same new architecture", "90+ languages", "Stability + Similarity", "Audio tags"]),
    "दोनों same architecture पे हैं, नब्बे plus languages, same settings।", ["same", "नब्बे"], "same"),
  CH(2, "Speed", "Chapter दो: speed।", ["speed"], "speed"),
  B("LAT", "stat", dict(value="~100ms", label="v4 Turbo median inference"),
    "Turbo की median inference latency करीब सौ milliseconds है।", ["सौ", "milliseconds"], "सौ"),
  B("AGENTS", "card", dict(icon="cpu", title="Built for real-time", rows=[["Use", "conversational agents"], ["Also", "interactive voice apps"], ["API", "Text to Dialogue websocket"]]),
    "Turbo real-time के लिए बना है: conversational agents और interactive voice apps।", ["real-time", "agents"], "real-time"),
  CH(3, "Quality", "Chapter तीन: quality।", ["quality"], "quality"),
  B("Q", "versus", dict(bad="Audiobook के लिए Turbo", good="Audiobook / voiceover के लिए v4"),
    "लंबा content, audiobook या character voiceover है, तो full v4 लो।", ["audiobook", "v4"], "v4"),
  B("Q2", "card", dict(icon="book", title="Eleven v4 best for", rows=[["Content", "creation"], ["Long-form", "audiobooks"], ["Characters", "voiceovers"]]),
    "Docs के मुताबिक full v4 highest quality model है: content, audiobooks और character voiceovers के लिए।", ["highest", "quality"], "quality"),
  CH(4, "Verdict", "Final decision।", ["decision"], "decision"),
  B("VERDICT", "verdict", dict(items=[dict(who="v4 Turbo", when="Phone calls, voice agents, live apps"),
                                       dict(who="Eleven v4", when="Videos, audiobooks, voiceovers, dubbing")]),
    "Live बात करनी है तो Turbo। Record करके publish करना है तो v4।", ["Turbo", "v4"], "Turbo"),
  B("TIP", "versus", dict(bad="एक model हर जगह", good="Agent में Turbo, content में v4"),
    "Pro tip: एक ही project में agent के लिए Turbo, और content के लिए v4 use करो।", ["Turbo", "v4"], "Pro"),
  B("CTA", "cta", dict(title="Save this", follow="Omilabs"),
    "Save करो, और ऐसे ही AI comparisons के लिए Omilabs subscribe करो।", ["Save", "subscribe"], "Save"),
  ])

# ─────────────── cmp006: Bolna Cloud vs Bolna Open Source ───────────────
# Sources: github.com/bolna-ai/bolna README (MIT, components, providers, docker local setup), Bolna docs packets.
L["cmp006"] = dict(
  series="AI COMPARISON", title="Bolna Cloud vs Bolna Open Source: Free Self-Host Ya Paid Platform? (2026)", music="ELEVENLABS V4",
  thumb=dict(a="Cloud", b="Open Source", top="BOLNA AI 2026", hook="FREE wala SAHI?", accent="#F2542D", colorA="#2F6BFF", colorB="#111111"),
  tags=["bolna open source", "bolna ai", "bolna self host", "voice ai open source", "bolna docker", "ai calling agent"],
  beats=[
  B("HOOK", "hook", dict(brand="Bolna Cloud vs OSS", pill="VOICE AI", stat="MIT", sub="open source license"),
    "Bolna का open source version free है। तो फिर लोग paid cloud क्यों use करते हैं?", ["open", "source", "free"], "free"),
  CH(1, "दोनों क्या हैं", "पहले दोनों को समझो।", ["समझो"], "समझो"),
  B("PARTS", "flow", dict(nodes=["Open source orchestration", "Hosted APIs", "No-code playground"]),
    "Bolna के तीन हिस्से हैं: open source orchestration, उसके ऊपर hosted APIs, और no-code playground।", ["open", "hosted", "playground"], "hosted"),
  B("CLOSED", "card", dict(icon="lock", title="README के मुताबिक", rows=[["Orchestration", "open source (MIT)"], ["Hosted APIs", "closed source"], ["Playground UI", "closed source"]]),
    "README के मुताबिक hosted APIs और playground अभी closed source हैं।", ["closed"], "closed"),
  CH(2, "Setup", "Chapter दो: setup कितना मुश्किल है।", ["setup"], "setup"),
  B("OSS SETUP", "list", dict(items=["Telephony server (Twilio / Plivo)", "Bolna server", "ngrok tunnel", "Redis"]),
    "Open source में Docker के चार containers चलाने होते हैं: telephony server, Bolna server, ngrok, और Redis।", ["Docker", "चार"], "Docker"),
  B("OSS KEYS", "card", dict(icon="key", title="खुद लाओ", rows=[["Telephony", "Twilio / Plivo account"], ["STT", "Deepgram, Azure…"], ["LLM", "OpenAI, DeepSeek, Llama…"], ["TTS", "ElevenLabs, Polly, Azure…"]]),
    "हर provider की key खुद लानी होती है: telephony, transcriber, LLM, और voice।", ["key", "खुद"], "खुद"),
  B("CLOUD SETUP", "card", dict(icon="bolt", title="Bolna Cloud", rows=[["Agent Studio", "minutes में call-ready"], ["Numbers", "buy या connect"], ["Bill", "एक wallet"]]),
    "Cloud में Agent Studio कुछ ही minutes में call-ready agent बना देता है, और billing एक wallet से।", ["Agent", "Studio", "wallet"], "Studio"),
  CH(3, "Features", "Chapter तीन: features।", ["features"], "features"),
  B("FEAT", "table", dict(title="Features", cols=["Cloud", "Open Source"], rows=[
      dict(k="No-code builder", v=["yes", "no"], win=0), dict(k="Graph agents / workflows", v=["yes", "—"], win=0),
      dict(k="Batch campaigns", v=["yes", "—"], win=0), dict(k="Call servers", v=["Mumbai (ap-south-1)", "जहाँ host करो"]),
      dict(k="Code-level control", v=["API", "full"], win=1)]),
    "No-code builder, graph agents, batch campaigns cloud में हैं। Open source में code पे पूरा control।", ["control", "cloud"], "control"),
  CH(4, "Cost", "Chapter चार: cost।", ["cost"], "cost"),
  B("COST", "versus", dict(bad="Open source = zero cost", good="Software free, पर providers + server का बिल"),
    "Open source software free है, पर telephony, LLM, voice और server का बिल आपका।", ["free", "बिल"], "बिल"),
  B("COST2", "card", dict(icon="wallet", title="Cloud pricing", rows=[["Voice AI", "flat per-minute (preferred)"], ["Telephony", "per minute"], ["Platform fee", "per minute"]]),
    "Cloud में preferred models पे flat per-minute rate, plus telephony और platform fee।", ["flat", "per-minute"], "flat"),
  CH(5, "Verdict", "किसके लिए कौनसा?", ["कौनसा"], "कौनसा"),
  B("VERDICT", "verdict", dict(items=[dict(who="Open Source", when="Developers, full control, अपना server"),
                                       dict(who="Bolna Cloud", when="Business, जल्दी launch, no-code, India numbers")]),
    "Developer हो और control चाहिए, तो open source। Business को जल्दी launch करना है, तो cloud।", ["Developer", "Business"], "control"),
  B("CTA", "cta", dict(title="Comment करो", follow="Omilabs"),
    "आप self-host करोगे या cloud? Comment करो, और Omilabs subscribe करो।", ["Comment", "subscribe"], "Comment"),
  ])

# ─────────────── cmp009: Kling 4.0 vs Kling 3.0 ───────────────
# Sources: kling.ai/blog/kling-4-vs-3 ; Kuaishou launch (15 Oct 2026); Kling 4.0 Flash specs.
L["cmp009"] = dict(
  series="AI COMPARISON", title="Kling 4.0 vs Kling 3.0: Kya Badla? 30 Second Video, 10 Keyframes (2026)", music="KLING 4.0",
  thumb=dict(a="Kling 3.0", b="Kling 4.0", top="AI VIDEO 2026", hook="DOUBLE LENGTH!", accent="#F2542D", colorA="#3B3B3B", colorB="#0B8F5A"),
  tags=["kling 4.0 vs 3.0", "kling 4.0", "kling ai", "ai video generator", "kling keyframes", "kling omni reference"],
  beats=[
  B("HOOK", "hook", dict(brand="Kling 4.0 vs 3.0", pill="AI VIDEO", stat="30", sub="seconds per generation"),
    "Kling 4.0 आ गया। 3.0 से क्या सच में बेहतर है? पूरा फर्क देखो।", ["Kling", "4.0", "फर्क"], "फर्क"),
  CH(1, "Length", "Chapter एक: video length।", ["length"], "length"),
  B("LEN", "table", dict(title="Video length", cols=["Kling 3.0", "Kling 4.0"], rows=[dict(k="Per generation", v=["3–15 sec", "3–30 sec"], win=1)]),
    "Kling 3.0 पंद्रह second तक, Kling 4.0 एक ही pass में तीस second तक।", ["पंद्रह", "तीस"], "तीस"),
  B("WHY", "versus", dict(bad="15 sec clips जोड़ना", good="30 sec का पूरा scene एक बार में"),
    "मतलब पूरा ad या scene बिना जोड़-तोड़ के एक ही बार में।", ["पूरा", "scene"], "scene"),
  CH(2, "Control", "Chapter दो: control।", ["control"], "control"),
  B("KEY", "table", dict(title="Control", cols=["Kling 3.0", "Kling 4.0"], rows=[
      dict(k="Keyframes", v=["start + end frame", "10 keyframes तक"], win=1),
      dict(k="References", v=["image, subject, video", "15 combined"], win=1)]),
    "3.0 में start और end frame थे, 4.0 में दस keyframes तक, और पंद्रह references।", ["दस", "keyframes", "पंद्रह"], "keyframes"),
  B("OMNI", "list", dict(items=["10 images तक", "5 videos (30 sec total)", "7 elements", "15 combined total"]),
    "Omni Reference में दस images, पाँच videos, सात elements, कुल पंद्रह references।", ["Omni", "Reference"], "Omni"),
  CH(3, "Audio और editing", "Chapter तीन: audio और editing।", ["audio"], "audio"),
  B("AUDIO", "list", dict(items=["Stereo audio", "Multilingual lip sync", "Video editing"]),
    "4.0 में stereo audio, multilingual lip sync, और video editing भी।", ["stereo", "lip", "sync"], "stereo"),
  B("FLASH", "duo", dict(a=dict(icon="video", title="Kling 4.0", rows=[["Length", "3–30 sec"], ["Keyframes", "10 तक"]]),
                         b=dict(icon="bolt", title="4.0 Flash", rows=[["Length", "3–20 sec"], ["Keyframes", "first frame only"]]), accentB="#0B8F5A"),
    "और 4.0 Flash तेज़ version है: बीस second तक, पर सिर्फ first frame।", ["Flash", "बीस"], "Flash"),
  CH(4, "Verdict", "Upgrade करें?", ["Upgrade"], "Upgrade"),
  B("VERDICT", "verdict", dict(items=[dict(who="Kling 4.0", when="लंबे scenes, storyboard control, ads"),
                                       dict(who="4.0 Flash", when="जल्दी drafts, छोटे clips")]),
    "लंबे scenes और control के लिए 4.0, जल्दी drafts के लिए Flash।", ["4.0", "Flash"], "4.0"),
  B("CTA", "cta", dict(title="Save this", follow="Omilabs"),
    "Save करो, और ऐसे ही comparisons के लिए Omilabs subscribe करो।", ["Save", "subscribe"], "Save"),
  ])

# ─────────────── cmp014: Claude Motion vs Kling 4.0 ───────────────
# Sources: support.claude.com "Get started with Claude Motion"; kling.ai Kling 4.0 vs 3.0.
L["cmp014"] = dict(
  series="AI COMPARISON", title="Claude Motion vs Kling 4.0: Animation Ya AI Video? Kaunsa Kab Use Karein (2026)", music="CLAUDE MOTION",
  thumb=dict(a="Claude Motion", b="Kling 4.0", top="AI VIDEO 2026", hook="DONO ALAG hai!", accent="#F2542D", colorA="#C2410C", colorB="#0B8F5A"),
  tags=["claude motion vs kling", "claude motion", "kling 4.0", "ai animation", "ai video generator", "anthropic claude"],
  beats=[
  B("HOOK", "hook", dict(brand="Claude Motion vs Kling", pill="AI VIDEO", stat="2", sub="बिलकुल अलग tools"),
    "Claude Motion और Kling 4.0, दोनों video बनाते हैं, पर बिलकुल अलग तरीके से।", ["Claude", "Motion", "Kling"], "अलग"),
  CH(1, "कैसे बनता है", "Chapter एक: video बनता कैसे है।", ["कैसे"], "कैसे"),
  B("HOW", "duo", dict(a=dict(icon="code", title="Claude Motion", rows=[["Method", "Claude code लिखता है"], ["Animates", "text, charts, images"], ["Video model", "नहीं"]]),
                       b=dict(icon="video", title="Kling 4.0", rows=[["Method", "video generation model"], ["Makes", "realistic footage"], ["Inputs", "text, image, keyframes"]]), accentB="#0B8F5A"),
    "Claude Motion code से animation बनाता है। Kling 4.0 एक video generation model है, realistic footage बनाता है।", ["code", "realistic"], "realistic"),
  B("PEOPLE", "versus", dict(bad="Claude Motion से असली लोग", good="Claude Motion = charts, explainers"),
    "इसलिए Claude Motion realistic लोग नहीं बनाता, वो explainers और charts के लिए है।", ["explainers", "charts"], "charts"),
  CH(2, "Use cases", "Chapter दो: use cases।", ["use"], "use"),
  B("MOTION USE", "list", dict(items=["All-hands explainer", "Board deck chart", "Onboarding walkthrough"]),
    "Claude Motion: explainer, animated chart, product walkthrough।", ["explainer", "chart"], "chart"),
  B("KLING USE", "list", dict(items=["Product ads", "Cinematic scenes", "Character shots", "30 sec single take"]),
    "Kling: product ads, cinematic scenes, और तीस second का single take।", ["ads", "cinematic"], "cinematic"),
  CH(3, "Editing", "Chapter तीन: editing।", ["editing"], "editing"),
  B("EDIT", "table", dict(title="Editing", cols=["Claude Motion", "Kling 4.0"], rows=[
      dict(k="Edit कैसे", v=["chat में Claude से", "video editing"]),
      dict(k="Shot control", v=["code animation", "10 keyframes"], win=1),
      dict(k="Export", v=["MP4", "video file"])]),
    "Motion में chat से Claude को बोलो, वो बदल देगा। Kling में shot control keyframes से।", ["chat", "keyframes"], "keyframes"),
  CH(4, "Access", "Chapter चार: कौन use कर सकता है।", ["कौन"], "कौन"),
  B("ACCESS", "duo", dict(a=dict(icon="users", title="Claude Motion", rows=[["Plans", "Team, Enterprise (beta)"], ["Cost", "plan usage में"]]),
                          b=dict(icon="globe", title="Kling 4.0", rows=[["Where", "kling.ai"], ["Flash", "3–20 sec"]]), accentB="#0B8F5A"),
    "Claude Motion अभी Team और Enterprise plans पे beta है, और plan usage में count होता है। Kling, kling dot ai पे मिलता है।", ["Team", "Enterprise"], "beta"),
  CH(5, "Verdict", "किसके लिए कौन?", ["कौन"], "कौन"),
  B("VERDICT", "verdict", dict(items=[dict(who="Claude Motion", when="Data, explainers, reports, decks"),
                                       dict(who="Kling 4.0", when="Ads, cinematic, realistic footage"),
                                       dict(who="दोनों", when="Kling shot + Motion chart overlay")]),
    "Data और explainers के लिए Claude Motion, realistic footage के लिए Kling, और दोनों साथ भी चलेंगे।", ["Motion", "Kling", "दोनों"], "दोनों"),
  B("CTA", "cta", dict(title="Comment करो", follow="Omilabs"),
    "आप कौनसा try करोगे? Comment करो, और Omilabs subscribe करो।", ["Comment", "subscribe"], "Comment"),
  ])


L["cmp001b"] = L["cmp001"]  # re-render with OmiLong fixes (new CI item id)
for _o, _n in [("cmp001", "cmp001c"), ("cmp004", "cmp004b"), ("cmp005", "cmp005b"), ("cmp006", "cmp006b"), ("cmp009", "cmp009b"), ("cmp014", "cmp014b"), ("cmp006", "cmp006c")]:
    L[_n] = L[_o]  # re-render: no caption overlap

# rendered before the 11 Nov 2026 rules; every new id must pass scripts/qa_rules.py
LEGACY = set(['cmp001', 'cmp001b', 'cmp001c', 'cmp004', 'cmp004b', 'cmp005', 'cmp005b', 'cmp006', 'cmp006b', 'cmp006c', 'cmp009', 'cmp009b', 'cmp014', 'cmp014b'])


def write(root):
    for vid, sp in L.items():
        d = os.path.join(root, "edit", vid); os.makedirs(d, exist_ok=True)
        sp = dict(sp); music = sp.pop("music", "ELEVENLABS V4")
        spec = dict(id=vid, format="long", voice="hi-IN-MadhurNeural", rate="+6%", accent="#F2542D", watermark="omilabs",
                    music=music, rules="v2" if vid in LEGACY else "v3", **sp)
        json.dump(spec, open(os.path.join(d, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(L), "long specs")


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)))
