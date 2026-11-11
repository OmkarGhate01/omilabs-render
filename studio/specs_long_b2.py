# Comparison batch 2 (11 Nov 2026): trending chat / search / coding / open models.
# Facts only from official pages read on 11 Nov 2026 (listed per video in `sources`, mirrored into long_v2.json).
from specs_long import B, CH, L

# ─────────────── cmp020: ChatGPT vs Gemini ───────────────
# Sources: chatgpt.com/pricing ; learn.chatgpt.com/docs/pricing ; help.openai.com (ChatGPT Go, Pro tiers) ;
#          gemini.google/subscriptions ; one.google.com/about/google-ai-plans
L["cmp020"] = dict(
  series="AI COMPARISON", title="ChatGPT vs Gemini: 2026 Mein Kaunsa Lein?", search_kw="ChatGPT vs Gemini", music="ELEVENLABS V4",
  thumb=dict(a="ChatGPT", b="Gemini", top="AI CHAT 2026", hook="₹ KAHAN LAGAAO?", accent="#F2542D", colorA="#111111", colorB="#2F6BFF"),
  tags=["chatgpt vs gemini", "gpt-6 vs gemini 4", "chatgpt plus vs google ai pro", "gemini 4 argon", "gpt 6 astra", "ai chatbot hindi"],
  beats=[
  B("HOOK", "hook", dict(brand="ChatGPT vs Gemini", pill="AI CHAT 2026", stat="$20", sub="दोनों का paid plan"),
    "ChatGPT या Gemini? दोनों बीस dollar के आसपास, पर आपके काम के लिए कौनसा सही?", ["ChatGPT", "Gemini", "सही"], "सही"),
  B("STAKES", "versus", dict(bad="गलत plan = पैसे और time दोनों waste", good="सही plan = आपके काम के tools"),
    "गलत plan लिया तो पैसे भी जाएंगे, और जो feature चाहिए वो मिलेगा भी नहीं।", ["गलत", "पैसे"], "गलत"),
  CH(1, "Plans और price", "Chapter एक: plans और price।", ["price"], "price"),
  B("PRICE", "table", dict(title="Price per month (USD)", cols=["ChatGPT", "Gemini"], rows=[
      dict(k="Free", v=["GPT-6 Luna", "Flash-Lite model"]),
      dict(k="सस्ता plan", v=["Go: $8*", "AI Plus"]),
      dict(k="Main plan", v=["Plus: $20", "AI Pro: $19.99"]),
      dict(k="Top plan", v=["Pro: $100 से", "Ultra: $99.99 से"])]),
    "ChatGPT Plus बीस dollar, Google AI Pro उन्नीस निन्यानवे। Top plans दोनों के सौ dollar से शुरू।", ["बीस", "सौ"], "Plus"),
  B("NOTE", "card", dict(icon="wallet", title="India price", rows=[["ChatGPT Go", "local price"], ["Check", "app में देखो"]]),
    "Go का price कुछ देशों में local होता है, इसलिए India का price अपने app में check करो।", ["local", "check"], "check"),
  CH(2, "Models", "Chapter दो: models।", ["models"], "models"),
  B("MODELS", "duo", dict(a=dict(icon="chat", title="ChatGPT Plus", rows=[["Models", "GPT-6 Astra, GPT-6.1 Sol"], ["Reasoning context", "256K"]]),
                          b=dict(icon="star", title="Google AI Pro", rows=[["Model", "Gemini 4 Argon"], ["Context", "1 million tokens"]]), accentB="#2F6BFF"),
    "Plus में GPT-6 Astra और GPT-6.1 Sol मिलते हैं। AI Pro में Gemini 4 Argon, और दस लाख tokens का context।", ["GPT-6", "Argon"], "Argon"),
  B("LONG", "versus", dict(bad="बहुत लंबी files, छोटा context", good="Gemini: 1,500 pages तक upload"),
    "बहुत लंबे documents हैं? Gemini पंद्रह सौ pages तक की files पढ़ सकता है।", ["पंद्रह", "pages"], "pages"),
  CH(3, "Extra फायदे", "Chapter तीन: plan के साथ क्या extra मिलता है।", ["extra"], "extra"),
  B("CHATGPT", "list", dict(items=["Codex (coding agent)", "Deep research", "Projects + scheduled tasks", "ChatGPT Work"]),
    "ChatGPT Plus: Codex coding agent, deep research, projects, scheduled tasks, और ChatGPT Work।", ["Codex", "research"], "Codex"),
  B("GEMINI", "list", dict(items=["5 TB cloud storage", "Gemini in Gmail, Docs", "1,000 Flow credits (video)", "Gemini Notebook"]),
    "Google AI Pro: पाँच TB storage, Gmail और Docs में Gemini, और video के लिए Flow credits।", ["storage", "Gmail"], "storage"),
  CH(4, "Verdict", "तो किसके लिए कौन?", ["कौन"], "कौन"),
  B("VERDICT", "verdict", dict(items=[dict(who="ChatGPT Plus", when="Coding (Codex), agents, deep research"),
                                       dict(who="Google AI Pro", when="Gmail/Docs users, लंबी files, storage"),
                                       dict(who="Free plans", when="पहले दोनों free try करो")]),
    "Coding और agents के लिए ChatGPT, Google apps और लंबी files के लिए Gemini। पहले दोनों free में try करो।", ["ChatGPT", "Gemini", "free"], "free"),
  B("CTA", "cta", dict(title="Comment करो", follow="Omilabs"),
    "आप कौनसा use करते हो? Comment करो, और ऐसे comparisons के लिए Omilabs subscribe करो।", ["Comment", "subscribe"], "Comment"),
  ])

# ─────────────── cmp021: ChatGPT vs Claude ───────────────
# Sources: chatgpt.com/pricing ; help.openai.com (Pro tiers) ; claude.com/pricing ; support.claude.com (Pro, Max plans)
L["cmp021"] = dict(
  series="AI COMPARISON", title="ChatGPT vs Claude: Kaam Ke Liye Kaunsa Best?", search_kw="ChatGPT vs Claude", music="CLAUDE MOTION",
  thumb=dict(a="ChatGPT", b="Claude", top="AI CHAT 2026", hook="SACH JAANO!", accent="#F2542D", colorA="#111111", colorB="#C2410C"),
  tags=["chatgpt vs claude", "claude vs chatgpt", "claude pro vs chatgpt plus", "claude code", "codex", "ai for work hindi"],
  beats=[
  B("HOOK", "hook", dict(brand="ChatGPT vs Claude", pill="AI FOR WORK", stat="$20", sub="दोनों का Pro/Plus"),
    "ChatGPT या Claude, काम के लिए कौनसा? दोनों बीस dollar, पर फर्क बड़ा है।", ["ChatGPT", "Claude", "फर्क"], "फर्क"),
  CH(1, "Plans", "Chapter एक: plans।", ["plans"], "plans"),
  B("PLANS", "table", dict(title="Price per month (USD)", cols=["ChatGPT", "Claude"], rows=[
      dict(k="Main plan", v=["Plus: $20", "Pro: $20 ($17 yearly)"]),
      dict(k="Heavy use", v=["Pro 100: $100", "Max: $100"]),
      dict(k="Power user", v=["Pro 200: $200", "Ultra: $200"]),
      dict(k="Top", v=["Pro 500: $500", "Team, Enterprise"])]),
    "दोनों का main plan बीस dollar, और सौ और दो सौ dollar के बड़े plans भी।", ["बीस", "सौ"], "बीस"),
  B("LIMITS", "card", dict(icon="lock", title="Claude limits", rows=[["Reset", "हर 5 घंटे + हर हफ्ते"], ["Max", "Pro का 5x"], ["Ultra", "10x, no 5-hr limit"]]),
    "Claude की limit हर पाँच घंटे और हर हफ्ते reset होती है। Max में पाँच गुना, Ultra में दस गुना।", ["पाँच", "दस"], "limit"),
  CH(2, "Models", "Chapter दो: models।", ["models"], "models"),
  B("MODELS", "duo", dict(a=dict(icon="chat", title="ChatGPT", rows=[["Free", "GPT-6 Luna"], ["Plus", "GPT-6 Astra, 6.1 Sol"]]),
                          b=dict(icon="star", title="Claude", rows=[["Free", "Sonnet, Haiku"], ["Pro", "+ Opus"], ["Top model", "Fable"]]), accentB="#C2410C"),
    "ChatGPT Plus में GPT-6 Astra। Claude Pro में Opus, और top model Fable Pro में usage credits से।", ["Astra", "Opus", "Fable"], "Fable"),
  CH(3, "Coding", "Chapter तीन: coding।", ["coding"], "coding"),
  B("CODE", "versus", dict(bad="अलग coding tool का अलग bill", good="दोनों में coding agent plan में शामिल"),
    "अच्छी बात: ChatGPT में Codex और Claude में Claude Code, दोनों paid plan में शामिल।", ["Codex", "Claude", "Code"], "Code"),
  B("CODE2", "table", dict(title="Coding agent", cols=["ChatGPT", "Claude"], rows=[
      dict(k="Agent", v=["Codex", "Claude Code"]),
      dict(k="Plan", v=["Plus में", "Pro में"]),
      dict(k="Limit", v=["plan की limit", "chat के साथ same pool"])]),
    "ध्यान दो: Claude Code और chat एक ही usage pool से चलते हैं।", ["same", "pool"], "pool"),
  CH(4, "Work tools", "Chapter चार: office का काम।", ["office"], "office"),
  B("WORK", "duo", dict(a=dict(icon="edit", title="ChatGPT Plus", rows=[["Office", "Excel, Word, PPT"], ["Extra", "Deep research"]]),
                        b=dict(icon="book", title="Claude Pro", rows=[["Office", "Microsoft 365"], ["Extra", "Research, Chrome"]]), accentB="#C2410C"),
    "दोनों office में आते हैं: ChatGPT के Excel और Word extensions, Claude for Microsoft 365।", ["Excel", "Microsoft"], "office"),
  CH(5, "Verdict", "तो किसके लिए कौन?", ["कौन"], "कौन"),
  B("VERDICT", "verdict", dict(items=[dict(who="ChatGPT", when="Image बनाना, voice, सबसे ज़्यादा features"),
                                       dict(who="Claude", when="लंबी writing, documents, Claude Code"),
                                       dict(who="दोनों", when="अपने काम पे free में test करो")]),
    "सबसे बड़ी बात: अपना असली काम दोनों के free plan पे test करो, फिर पैसे लगाओ।", ["test", "free"], "test"),
  B("CTA", "cta", dict(title="Comment करो", follow="Omilabs"),
    "आपका favourite कौन है? Comment करो, और Omilabs subscribe करो।", ["Comment", "subscribe"], "Comment"),
  ])

# ─────────────── cmp022: ChatGPT Search vs Google AI Mode ───────────────
# Sources: help.openai.com "Searching the web with ChatGPT", "Deep research in ChatGPT" ;
#          support.google.com/websearch/answer/16011537 (AI Mode), /answer/17104441 (local availability)
L["cmp022"] = dict(
  series="AI COMPARISON", title="ChatGPT Search vs Google AI Mode: Kaun Jeeta?", search_kw="ChatGPT Search vs Google AI Mode", music="ELEVENLABS V4",
  thumb=dict(a="ChatGPT Search", b="AI Mode", top="AI SEARCH 2026", hook="SEARCH BADAL GAYA?", accent="#F2542D", colorA="#111111", colorB="#2F6BFF"),
  tags=["chatgpt search vs google ai mode", "google ai mode", "chatgpt search", "ai search", "google ai mode india", "deep research"],
  beats=[
  B("HOOK", "hook", dict(brand="ChatGPT Search vs AI Mode", pill="AI SEARCH", stat="2", sub="तरीके Google करने के"),
    "Google पे search करो या ChatGPT से पूछो? दोनों AI search में कौन आगे है?", ["Google", "ChatGPT", "आगे"], "आगे"),
  CH(1, "कैसे काम करता है", "Chapter एक: दोनों काम कैसे करते हैं।", ["कैसे"], "कैसे"),
  B("HOW", "duo", dict(a=dict(icon="chat", title="ChatGPT Search", rows=[["Method", "queries बनाकर search"], ["Sources", "search partners"]]),
                       b=dict(icon="globe", title="Google AI Mode", rows=[["Method", "query fan-out"], ["Sources", "Google Search"]]), accentB="#2F6BFF"),
    "ChatGPT आपके सवाल को search queries में बदलता है। AI Mode सवाल को subtopics में तोड़कर सबको एक साथ search करता है।", ["queries", "subtopics"], "subtopics"),
  B("ACCESS", "table", dict(title="कहाँ मिलता है", cols=["ChatGPT Search", "AI Mode"], rows=[
      dict(k="Free?", v=["हाँ, बिना login भी", "हाँ"]),
      dict(k="कहाँ", v=["chatgpt.com, apps", "google.com/ai, Google app"]),
      dict(k="Upload", v=["files, images", "images, PDF, files"])]),
    "दोनों free हैं। ChatGPT search तो बिना login के भी चलता है। AI Mode google dot com slash ai पे।", ["free", "login"], "free"),
  CH(2, "Deep research", "Chapter दो: गहरी research।", ["research"], "research"),
  B("DEEP", "duo", dict(a=dict(icon="book", title="ChatGPT deep research", rows=[["Plan", "पहले plan दिखाता"], ["Output", "Word, PDF report"]]),
                        b=dict(icon="globe", title="AI Mode Deep Search", rows=[["Reach", "सैकड़ों sites"], ["Access", "Pro/Ultra, US"]]), accentB="#2F6BFF"),
    "ChatGPT deep research पहले plan दिखाता है, फिर Word या PDF report देता है। Google का Deep Search अभी US में Pro और Ultra users के लिए।", ["report", "US"], "report"),
  CH(3, "Local काम", "Chapter तीन: रोज़ के local काम।", ["local"], "local"),
  B("LOCAL", "list", dict(items=["Appointments, prices, stock check", "ज़रूरत हो तो business को call", "Dining reservations: India में English + Hindi"]),
    "AI Mode local काम में तेज़ है: price, stock, appointment check, और ज़रूरत हो तो business को call भी।", ["local", "call"], "call"),
  B("PERSONAL", "versus", dict(bad="हर बार अपनी पूरी बात समझाना", good="AI Mode: Gmail, Photos connect (optional)"),
    "AI Mode को Gmail और Photos से connect कर सकते हो, ये पूरी तरह आपकी मर्ज़ी पे है।", ["Gmail", "मर्ज़ी"], "Gmail"),
  CH(4, "Verdict", "तो कब कौनसा?", ["कब"], "कब"),
  B("VERDICT", "verdict", dict(items=[dict(who="Google AI Mode", when="Local, shopping, Google apps, interactive visuals"),
                                       dict(who="ChatGPT Search", when="बातचीत में follow-ups, deep research report"),
                                       dict(who="दोनों", when="ज़रूरी बात हो तो source खोलकर check करो")]),
    "Local और shopping के लिए AI Mode, बातचीत और reports के लिए ChatGPT। और ज़रूरी बात का source हमेशा खोलकर check करो।", ["AI", "Mode", "source"], "source"),
  B("CTA", "cta", dict(title="Comment करो", follow="Omilabs"),
    "आप अब Google ज़्यादा करते हो या ChatGPT? Comment करो, और Omilabs subscribe करो।", ["Comment", "subscribe"], "Comment"),
  ])

# ─────────────── cmp023: Claude Code vs Cursor vs GitHub Copilot ───────────────
# Sources: claude.com/pricing (Claude Code in paid plans) ; cursor.com/docs/models-and-pricing ; cursor.com/help pricing (legacy plans) ;
#          github.com/features/copilot/plans ; docs.github.com/en/copilot/get-started/plans
L["cmp023"] = dict(
  series="AI COMPARISON", title="Claude Code vs Cursor vs Copilot: Kaunsa Lein?", search_kw="Claude Code vs Cursor", music="CLAUDE MOTION",
  thumb=dict(a="Claude Code", b="Cursor", top="AI CODING 2026", hook="$10 YA $200?", accent="#F2542D", colorA="#C2410C", colorB="#111111"),
  tags=["claude code vs cursor", "cursor vs copilot", "github copilot", "claude code", "ai coding tools", "best ai for coding hindi"],
  beats=[
  B("HOOK", "hook", dict(brand="Claude Code vs Cursor vs Copilot", pill="AI CODING", stat="3", sub="tools, 1 budget"),
    "Coding के लिए Claude Code, Cursor या Copilot? गलत चुना तो हर महीने पैसे डूबेंगे।", ["Claude", "Cursor", "Copilot"], "गलत"),
  CH(1, "तीनों क्या हैं", "Chapter एक: तीनों हैं क्या।", ["क्या"], "क्या"),
  B("WHAT", "list", dict(items=["Claude Code: Claude plan वाला coding agent", "Cursor: AI code editor", "Copilot: GitHub का AI, editors + CLI में"]),
    "Claude Code, Claude के plan वाला coding agent है। Cursor एक AI editor है। Copilot, GitHub का AI है।", ["agent", "editor"], "editor"),
  CH(2, "Price", "Chapter दो: price।", ["price"], "price"),
  B("PRICE", "table", dict(title="Price per month (USD)", cols=["Claude Code", "Cursor", "Copilot"], rows=[
      dict(k="Free", v=["नहीं", "Free (limited)", "2,000 completions"], win=2),
      dict(k="Entry", v=["Pro: $20", "Plus: $8", "Pro: $10"]),
      dict(k="Mid", v=["Max: $100", "Premium: $30", "Pro+: $39"]),
      dict(k="Top", v=["Ultra: $200", "Ultra: $200", "Max: $100"])]),
    "Copilot का free plan है, दो हज़ार completions हर महीने। Claude Code बीस dollar के Pro से शुरू।", ["free", "बीस"], "free"),
  B("CURSOR", "card", dict(icon="key", title="Cursor का नया plan", rows=[["अब", "X Subscription"], ["साथ में", "Grok + X"], ["Other models", "Premium+, API price"]]),
    "ध्यान दो: Cursor अब X Subscription का हिस्सा है, Grok और X के साथ। दूसरे companies के models Premium से ऊपर, API price पे।", ["Grok", "API"], "X"),
  CH(3, "Usage कैसे गिनते हैं", "Chapter तीन: usage कैसे गिना जाता है।", ["usage"], "usage"),
  B("USAGE", "table", dict(title="Usage", cols=["Claude Code", "Cursor", "Copilot"], rows=[
      dict(k="गिनती", v=["chat के साथ same pool", "weekly pool, Grok के साथ", "AI credits"]),
      dict(k="Reset", v=["5 घंटे + हफ्ता", "हर हफ्ते", "हर महीने"])]),
    "Claude Code, chat की limit share करता है। Cursor का weekly pool है। Copilot AI credits से चलता है।", ["pool", "credits"], "credits"),
  B("STUDENT", "versus", dict(bad="Student हो और पैसे नहीं?", good="Copilot Student: verified students के लिए free"),
    "Student हो? Verified students के लिए Copilot Student free है।", ["Student", "free"], "free"),
  CH(4, "Verdict", "तो किसे कौनसा?", ["किसे"], "किसे"),
  B("VERDICT", "verdict", dict(items=[dict(who="Copilot", when="Students, कम budget, GitHub पे काम"),
                                       dict(who="Claude Code", when="Terminal agent + Claude chat एक ही plan में"),
                                       dict(who="Cursor", when="AI editor चाहिए, Grok/X भी use करते हो")]),
    "कम budget या student: Copilot। Terminal agent और chat एक plan में: Claude Code। Editor के साथ Grok भी: Cursor।", ["Copilot", "Claude", "Cursor"], "budget"),
  B("CTA", "cta", dict(title="Comment करो", follow="Omilabs"),
    "आप कौनसा use करते हो? Comment करो, और Omilabs subscribe करो।", ["Comment", "subscribe"], "Comment"),
  ])

# ─────────────── cmp024: Kimi K3.1 Pro vs DeepSeek V4.1 Flash ───────────────
# Sources: huggingface.co/moonshotai/Kimi-K3.1-Pro (model card) ; forum.moonshot.ai (K3.1 Pro launch) ;
#          api-docs.deepseek.com (Models & Pricing, Change Log, V4.1-Flash and V4.1-Flash-1017 news) ; deepseek.com/en/platform
L["cmp024"] = dict(
  series="AI COMPARISON", title="Kimi K3.1 vs DeepSeek: Open AI Ka King Kaun?", search_kw="Kimi K3.1 vs DeepSeek", music="KLING 4.0",
  thumb=dict(a="Kimi K3.1", b="DeepSeek", top="OPEN MODELS 2026", hook="2.8 TRILLION!", accent="#F2542D", colorA="#00B4D8", colorB="#2F6BFF"),
  tags=["kimi k3.1 vs deepseek", "kimi k3.1 pro", "deepseek v4.1 flash", "open source ai model", "open weights", "cheap ai api"],
  beats=[
  B("HOOK", "hook", dict(brand="Kimi K3.1 vs DeepSeek", pill="OPEN MODELS", stat="2.8T", sub="parameters, open weights"),
    "Kimi का 2.8 trillion parameter model download के लिए खुला। तो DeepSeek से बेहतर कौन?", ["Kimi", "DeepSeek", "कौन"], "कौन"),
  CH(1, "Model size", "Chapter एक: model कितना बड़ा है।", ["बड़ा"], "बड़ा"),
  B("SIZE", "table", dict(title="Model", cols=["Kimi K3.1 Pro", "DeepSeek V4.1 Flash"], rows=[
      dict(k="Type", v=["MoE, open weights", "नए architecture का सबसे छोटा model"]),
      dict(k="Parameters", v=["2.8T total, 104B active", "Flash family"]),
      dict(k="Context", v=["1M tokens", "1M tokens तक"]),
      dict(k="Input", v=["Text + Image", "Text + Image"])]),
    "Kimi K3.1 Pro: 2.8 trillion total, हर token पे 104 billion active। दोनों में दस लाख tokens का context।", ["trillion", "context"], "trillion"),
  B("MOE", "versus", dict(bad="Total parameters = speed", good="Active parameters = speed, total = memory"),
    "याद रखो: speed active parameters से तय होती है, और memory total से।", ["active", "memory"], "active"),
  CH(2, "Price", "Chapter दो: API price।", ["price"], "price"),
  B("DSPRICE", "card", dict(icon="wallet", title="DeepSeek Flash (per 1M tokens)", rows=[["Input (off-peak)", "$0.15"], ["Output (off-peak)", "$0.60"], ["Peak", "double"]]),
    "DeepSeek Flash बहुत सस्ता है: off-peak में input पंद्रह cent, output साठ cent per million tokens। Peak में double।", ["सस्ता", "off-peak"], "सस्ता"),
  B("OFFPEAK", "versus", dict(bad="हर काम peak time पे", good="Off-peak में चलाओ = आधा price"),
    "Trick: जो काम रुक सकता है, उसे off-peak में चलाओ, price आधा।", ["off-peak", "आधा"], "आधा"),
  CH(3, "Self-host", "Chapter तीन: खुद के server पे चलाना।", ["server"], "server"),
  B("SELF", "duo", dict(a=dict(icon="cpu", title="Kimi K3.1 Pro", rows=[["Weights", "Hugging Face पे open"], ["Format", "MXFP4 weights"], ["Serve", "vLLM, SGLang"]]),
                        b=dict(icon="globe", title="DeepSeek", rows=[["API", "deepseek-flash"], ["Extra", "Search + Fetch API"], ["Apps", "web और app पे भी"]]), accentB="#2F6BFF"),
    "Kimi के weights Hugging Face पे खुले हैं, पर इतना बड़ा model चलाने के लिए बहुत बड़ा GPU setup चाहिए।", ["Hugging", "GPU"], "GPU"),
  B("LICENSE", "list", dict(items=["Benchmarks company खुद बताती है", "अपने काम पे test करो", "Commercial use से पहले license पढ़ो"]),
    "दोनों के benchmarks company के अपने हैं। अपने काम पे test करो, और business में लगाने से पहले license पढ़ो।", ["test", "license"], "license"),
  CH(4, "Verdict", "तो किसके लिए कौन?", ["कौन"], "कौन"),
  B("VERDICT", "verdict", dict(items=[dict(who="DeepSeek Flash", when="सस्ता API, ज़्यादा volume, off-peak jobs"),
                                       dict(who="Kimi K3.1 Pro", when="बड़ा open model, self-host, fine-tune"),
                                       dict(who="दोनों", when="छोटा test पहले, फिर scale")]),
    "सस्ते API और ज़्यादा volume के लिए DeepSeek, सबसे बड़े open model के लिए Kimi। पहले छोटा test, फिर scale।", ["DeepSeek", "Kimi", "test"], "test"),
  B("CTA", "cta", dict(title="Comment करो", follow="Omilabs"),
    "Open models पे और video चाहिए? Comment करो, और Omilabs subscribe करो।", ["Comment", "subscribe"], "Comment"),
  ])

B2 = ["cmp020", "cmp021", "cmp022", "cmp023", "cmp024"]


if __name__ == "__main__":
    import json, os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))
    import qa_rules as Q
    root = os.path.dirname(os.path.abspath(__file__))
    bad = 0
    for vid in B2:
        sp = dict(L[vid]); music = sp.pop("music", "ELEVENLABS V4")
        spec = dict(id=vid, format="long", voice="hi-IN-MadhurNeural", rate="+6%", accent="#F2542D", watermark="omilabs",
                    music=music, rules="v3", **sp)
        errs = Q.check(spec)
        print(vid, len(spec["title"]), "chars", "OK" if not errs else errs)
        bad += bool(errs)
        d = os.path.join(root, "edit", vid); os.makedirs(d, exist_ok=True)
        json.dump(spec, open(os.path.join(d, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.exit(1 if bad else 0)
